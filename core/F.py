from typing import List
from core.rwpm import rwpm
from error import ScoresAndWeightsDoesNotMatchError

def F(scores: List[float], weights: List[float], alpha: float, alpha_t: float, n: int) -> float:
    if len(scores) != len(weights):
        raise ScoresAndWeightsDoesNotMatchError()
    f_score = 0.0
    if alpha == 1.0:
        f_score = min(scores)
    elif alpha_t <= alpha < 1:
        for i in range(0, len(scores)):
            f_score += (weights[i] * pow(scores[i], rwpm(alpha, n)))
        f_score = pow(f_score, 1.0 / rwpm(alpha, n))
    elif 0.5 < alpha < alpha_t:
        f_score1 = 0.0
        f_score2 = 0.0
        for i in range(0, len(scores)):
            f_score1 += (weights[i] * scores[i])
        for i in range(0, len(scores)):
            f_score2 += (weights[i] * pow(scores[i], rwpm(alpha_t, n)))
        f_score2 = pow(f_score2, 1.0 / rwpm(alpha_t, n))
        f_score = ((alpha_t - alpha) / (alpha_t - 0.5) * f_score1) + ((alpha - 0.5) / (alpha_t - 0.5) * f_score2)
    elif alpha == 0.5:
        for i in range(0, len(scores)):
            f_score += (weights[i] * scores[i])
    return f_score