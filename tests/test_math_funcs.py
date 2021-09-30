import pytest

from mathcrypto.math.funcs import MathFunctions


@pytest.mark.parametrize("num,expected", [(65, 48), (240, 64), (17, 16)])
def test_phi(num, expected):
    assert MathFunctions.phi(num) == expected


@pytest.mark.parametrize("num_a,num_b,expected", [(135, 186, 3), (132, 84, 12), (1701, 3768, 3)])
def test_euclid_gcd(num_a, num_b, expected):
    assert MathFunctions.euclid_gcd(num_a, num_b) == expected


@pytest.mark.parametrize(
    "problem,expected",
    [
        ([[8, 9], [3, 5]], 8),
        ([[7, 9], [4, 6]], 2),
        ([[7, 9], [3, 5]], 43),
    ],
)
def test_crt(problem, expected):
    assert MathFunctions.crt(problem) == expected


@pytest.mark.parametrize("modulus,number,expected", [(13, 7, 2), (24, 5, 5), (7, 3, 5)])
def test_eea(modulus, number, expected):
    assert MathFunctions.eea(modulus, number) == expected
