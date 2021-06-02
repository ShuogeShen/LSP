def rwpm(alpha: float, n: int) -> float:
    if n == 2:
        rwpm = (0.25 + (1.65811 if alpha >= 0.5 else 1.62481) * (0.5 - alpha)
                +(2.15388 if alpha >= 0.5 else 1.26214) * pow(0.5 - alpha, 2)
                +(8.2844 if alpha >= 0.5 else 0.144343) * pow(0.5 - alpha, 3)
                +(6.16764 if alpha >= 0.5 else -0.144343) * pow(0.5 - alpha, 4)) / (alpha - alpha * alpha)
    elif n == 3:
        rwpm = (0.25 + (1.95419 if alpha >= 0.5 else 1.85971) * (0.5 - alpha)
                + (3.69032 if alpha >= 0.5 else 1.9532) * pow(0.5 - alpha, 2)
                + (10.7073 if alpha >= 0.5 else -0.17274) * pow(0.5 - alpha, 3)
                + (9.46921 if alpha >= 0.5 else 0.0213069) * pow(0.5 - alpha, 4)) / (alpha - alpha * alpha)
    elif n == 4:
        rwpm = (0.25 + (2.11034 if alpha >= 0.5 else 2.06781) * (0.5 - alpha)
                + (4.4749 if alpha >= 0.5 else 1.83246) * pow(0.5 - alpha, 2)
                + (11.4962 if alpha >= 0.5 else 1.99365) * pow(0.5 - alpha, 3)
                + (10.5552 if alpha >= 0.5 else -2.30786) * pow(0.5 - alpha, 4)) / (alpha - alpha * alpha)
    else:
        rwpm = (0.25 + (2.21868 if alpha >= 0.5 else 2.09567) * (0.5 - alpha)
                + (5.0574 if alpha >= 0.5 else 3.04673) * pow(0.5 - alpha, 2)
                + (12.0866 if alpha >= 0.5 else -0.388745) * pow(0.5 - alpha, 3)
                + (11.2383 if alpha >= 0.5 else 0.0110307) * pow(0.5 - alpha, 4)) / (alpha - alpha * alpha)
    return rwpm