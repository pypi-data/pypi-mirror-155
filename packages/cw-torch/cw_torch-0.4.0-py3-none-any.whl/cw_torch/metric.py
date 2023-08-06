import torch

cw_normality_scale_factor = 0.28209479177

def cw_normality_no_scale(sample: torch.Tensor, gamma: torch.Tensor) -> torch.Tensor:
    """The function measures a Cramer-Wold distance of a sample from the standard multivariate normal distribution. 
    The implementation follows the formula from Theorem 3 in: https://jmlr.org/papers/volume21/19-560/19-560.pdf
    This function skips scaling of the computed distance by $ \frac{1}{2*sqrt()\pi) }$. 
    It is effectively the formula from page 14 which is the formula used by original CWAE implementation.

    Args:
        sample (torch.Tensor): sample to evaluate. Sample must be a 2D tensor N x D.
        gamma (torch.Tensor): value of gamma coefficient. 

    Returns:
        torch.Tensor: One dimensional nonnegative tensor storing a distance of the sample from standard multidimensional normal distribution.
    """
    assert sample.ndim == 2, f"{sample} must be a two dimensional tensor"
    assert gamma.ndim == 0, f"{gamma} must be a zero dimensional tensor"

    N, D = sample.size()

    K = 1.0/(2.0*D-3.0)

    A1 = torch.pdist(sample)**2
    A = 2.0 * torch.rsqrt(gamma + K*A1).sum() / N**2 + torch.rsqrt(gamma) / N

    B1 = torch.linalg.norm(sample, 2, axis=1)**2 
    B = torch.rsqrt(gamma + 0.5 + K*B1).mean()

    result = A + torch.rsqrt(1+gamma) - 2.0 * B

    return result

def cw_normality(sample: torch.Tensor, gamma: torch.Tensor) -> torch.Tensor:
    """The function measures a Cramer-Wold distance of a sample from the standard multivariate normal distribution. 
    The implementation follows the formula from Theorem 3 in: https://jmlr.org/papers/volume21/19-560/19-560.pdf

    Args:
        sample (torch.Tensor): sample to evaluate. Sample must be a 2D tensor N x D.
        gamma (torch.Tensor): value of gamma coefficient. 

    Returns:
        torch.Tensor: One dimensional nonnegative tensor storing a distance of the sample from standard multidimensional normal distribution.
    """
    
    result = cw_normality_no_scale(sample, gamma)   

    return result * cw_normality_scale_factor

