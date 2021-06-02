from typing import List
from core.F import F

def gcd(scores: List[float], weights: List[float], alpha: float, alpha_t: float, n: int) -> float:
    if alpha >= 0.5:
        return F(scores, weights, alpha, alpha_t, n)
    else:
        compl_scores = [1.0 - score for score in scores]
        return 1.0 - F(compl_scores, weights, 1.0 - alpha, alpha_t, n)

def cpa(innerWeight1: float, innerWeight2: float, mandatoryScore: float, optionalScore: float) -> float:
    compl_innerWeight1 = 1.0 - innerWeight1
    compl_innerWeight2 = 1.0 - innerWeight2
    t = (innerWeight1 * mandatoryScore) + (compl_innerWeight1 * optionalScore)
    return 1.0 / ((innerWeight2 / mandatoryScore) + (compl_innerWeight2 / t)) if mandatoryScore != 0.0 else 0.0

def dpa(innerWeight1: float, innerWeight2: float, sufficientScore: float, optionalScore: float) -> float:
    compl_innerWeight1 = 1.0 - innerWeight1
    compl_innerWeight2 = 1.0 - innerWeight2
    t = (innerWeight1 * sufficientScore) + (compl_innerWeight1 * optionalScore)
    compl_sufficientScore = 1.0 - sufficientScore
    compl_t = 1.0 - t
    return 1.0 - (1.0 / ((innerWeight2 / compl_sufficientScore) + (compl_innerWeight2 / compl_t))) if sufficientScore != 1.0 else 1.0