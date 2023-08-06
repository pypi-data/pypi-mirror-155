from itertools import product

import torch
from botorch.utils.multi_objective.box_decompositions.non_dominated import FastNondominatedPartitioning
from torch import Tensor
from torch.distributions import Normal


class ExpectedHypervolumeImprovement:
    def __init__(self, ref_point: Tensor, Y: Tensor):
        self.ref_point = ref_point
        self.partitioning = FastNondominatedPartitioning(
            ref_point=self.ref_point,
            Y=Y,
        )

        cell_bounds = self.partitioning.get_hypercell_bounds()
        self.cell_lower_bounds = cell_bounds[0]
        self.cell_upper_bounds = cell_bounds[1]

        # create indexing tensor of shape `2^m x m`
        self._cross_product_indices = torch.tensor(
            list(product(*[[0, 1] for _ in range(ref_point.shape[0])])),
            dtype=torch.long,
            device=ref_point.device,
        )

    def psi(self, lower: Tensor, upper: Tensor, mu: Tensor, sigma: Tensor) -> Tensor:
        r"""Compute Psi function.

        For each cell i and outcome k:

            Psi(lower_{i,k}, upper_{i,k}, mu_k, sigma_k) = (
            sigma_k * PDF((upper_{i,k} - mu_k) / sigma_k) + (
            mu_k - lower_{i,k}
            ) * (1 - CDF(upper_{i,k} - mu_k) / sigma_k)
            )

        See Equation 19 in [Yang2019]_ for more details.

        Args:
            lower: A `num_cells x m`-dim tensor of lower cell bounds
            upper: A `num_cells x m`-dim tensor of upper cell bounds
            mu: A `batch_shape x 1 x m`-dim tensor of means
            sigma: A `batch_shape x 1 x m`-dim tensor of standard deviations (clamped).

        Returns:
            A `batch_shape x num_cells x m`-dim tensor of values.
        """
        u = (upper - mu) / sigma
        return sigma * Normal(0, 1).log_prob(u).exp() + (mu - lower) * (1 - Normal(0, 1).cdf(u))

    def nu(self, lower: Tensor, upper: Tensor, mu: Tensor, sigma: Tensor) -> Tensor:
        r"""Compute Nu function.

        For each cell i and outcome k:

            nu(lower_{i,k}, upper_{i,k}, mu_k, sigma_k) = (
            upper_{i,k} - lower_{i,k}
            ) * (1 - CDF((upper_{i,k} - mu_k) / sigma_k))

        See Equation 25 in [Yang2019]_ for more details.

        Args:
            lower: A `num_cells x m`-dim tensor of lower cell bounds
            upper: A `num_cells x m`-dim tensor of upper cell bounds
            mu: A `batch_shape x 1 x m`-dim tensor of means
            sigma: A `batch_shape x 1 x m`-dim tensor of standard deviations (clamped).

        Returns:
            A `batch_shape x num_cells x m`-dim tensor of values.
        """
        return (upper - lower) * (1 - Normal(0, 1).cdf((upper - mu) / sigma))

    def ehvi_calc(self, Y_new: Tensor, Y_new_stddev: Tensor) -> Tensor:
        # Reshaped to batch_size number of rows in the tensors
        Y_new = Y_new.reshape(Y_new.shape[0], 1, Y_new.shape[1])
        Y_new_stddev = Y_new_stddev.reshape(Y_new_stddev.shape[0], 1, Y_new_stddev.shape[1])

        # clamp here, since upper_bounds will contain `inf`s, which are not differentiable
        cell_upper_bounds = self.cell_upper_bounds.clamp_max(1e10 if Y_new.dtype == torch.double else 1e8)

        # Compute psi(lower_i, upper_i, mu_i, sigma_i) for i=0, ... m-2
        psi_lu = self.psi(
            lower=self.cell_lower_bounds,
            upper=cell_upper_bounds,
            mu=Y_new,
            sigma=Y_new_stddev,
        )
        # Compute psi(lower_m, lower_m, mu_m, sigma_m)
        psi_ll = self.psi(
            lower=self.cell_lower_bounds,
            upper=self.cell_lower_bounds,
            mu=Y_new,
            sigma=Y_new_stddev,
        )

        # Compute nu(lower_m, upper_m, mu_m, sigma_m)
        nu = self.nu(
            lower=self.cell_lower_bounds,
            upper=cell_upper_bounds,
            mu=Y_new,
            sigma=Y_new_stddev,
        )

        # compute the difference psi_ll - psi_lu
        psi_diff = psi_ll - psi_lu

        # this is batch_shape x num_cells x 2 x (m-1)
        stacked_factors = torch.stack([psi_diff, nu], dim=-2)

        # Take the cross product of psi_diff and nu across all outcomes
        # e.g. for m = 2
        # for each batch and cell, compute
        # [psi_diff_0, psi_diff_1]
        # [nu_0, psi_diff_1]
        # [psi_diff_0, nu_1]
        # [nu_0, nu_1]
        # this tensor has shape: `batch_shape x num_cells x 2^m x m`
        all_factors_up_to_last = stacked_factors.gather(
            dim=-2,
            index=self._cross_product_indices.expand(stacked_factors.shape[:-2] + self._cross_product_indices.shape),
        )

        # compute product for all 2^m terms,
        # sum across all terms and hypercells
        ehvi = all_factors_up_to_last.prod(dim=-1).sum()

        return ehvi
