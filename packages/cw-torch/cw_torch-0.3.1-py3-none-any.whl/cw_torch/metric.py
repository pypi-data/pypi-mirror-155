import torch

def cw_normality(sample: torch.Tensor, gamma: torch.Tensor) -> torch.Tensor:
    """The function measures a Cramer-Wold distance of a sample from the standard multivariate normal distribution. 
    The implementation follows the formula from Theorem 3 in: https://jmlr.org/papers/volume21/19-560/19-560.pdf

    Args:
        sample (torch.Tensor): sample to evaluate. Sample must be a 2D tensor N x D.
        gamma (torch.Tensor, optional): value of gamma coefficient. 

    Returns:
        torch.Tensor: One dimensional nonnegative tensor storing a distance of the sample from standard multidimensional normal distribution.
    """
    assert sample.ndim == 2, f"{sample} must be a two dimensional tensor"
    assert gamma.ndim == 0, f"{gamma} must be a zero dimensional tensor"

    D = sample.size(1)

    K = 1.0/(2.0*D-3.0)

    A1 = torch.cdist(sample, sample)**2
    A = torch.rsqrt(gamma + K*A1).mean()

    B1 = torch.linalg.norm(sample, 2, axis=1)**2 
    B = 2*(torch.rsqrt(gamma + 0.5 + K*B1)).mean()

    return torch.rsqrt(1+gamma) + A - B

