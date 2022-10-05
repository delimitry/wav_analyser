from cmath import exp, pi


def fft(data: list) -> list:
    """Cooley-Turkey FFT algorithm.
    Reference: https://en.wikipedia.org/wiki/Cooley–Tukey_FFT_algorithm#Pseudocode"""
    n = len(data)
    if n <= 1:
        return data
    even = fft(data[0::2])
    odd = fft(data[1::2])
    result = [0] * n
    mid = n // 2
    coefficient = -2j * pi / n
    for k in range(mid):
        p = even[k]
        q = exp(coefficient * k) * odd[k]
        result[k] = p + q
        result[k + mid] = p - q
    return result
