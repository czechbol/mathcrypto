import pytest

from mathcrypto.math.groups import MultiplicativeGroup


@pytest.mark.parametrize("mod,expected", [(9, 6), (11, 10), (22, 10)])
def test_group_generation_order(mod, expected):
    group = MultiplicativeGroup(mod)
    assert group.order == expected


@pytest.mark.parametrize(
    "mod,expected",
    [
        (9, [1, 2, 4, 5, 7, 8]),
        (11, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        (22, [1, 3, 5, 7, 9, 13, 15, 17, 19, 21]),
    ],
)
def test_group_generation_elements(mod, expected):
    group = MultiplicativeGroup(mod)
    assert group.elements == expected


@pytest.mark.parametrize("mod,expected", [(9, [2, 5]), (11, [2, 6, 7, 8]), (22, [7, 13, 17, 19])])
def test_group_generation_generators(mod, expected):
    group = MultiplicativeGroup(mod)
    assert group.generators == expected


@pytest.mark.parametrize("mod,element,expected", [(13, 7, 12), (29, 16, 7), (17, 6, 16)])
def test_get_element_order(mod, element, expected):
    group = MultiplicativeGroup(mod)
    assert group.get_element_order(element) == expected


@pytest.mark.parametrize(
    "mod,element,expected",
    [
        (13, 7, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]),
        (13, 5, [8, 1, 12, 5]),
        (17, 13, [16, 1, 4, 13]),
    ],
)
def test_get_element_subgroup(mod, element, expected):
    group = MultiplicativeGroup(mod)
    assert group.get_element_subgroup(element) == expected


@pytest.mark.parametrize("mod,element,expected", [(13, 7, 2), (24, 5, 5), (7, 3, 5)])
def test_get_inverse_element(mod, element, expected):
    group = MultiplicativeGroup(mod)
    assert group.get_inverse_element(element) == expected
