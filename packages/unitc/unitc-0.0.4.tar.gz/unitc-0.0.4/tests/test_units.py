import pytest
import numpy as np

from unitc import unit_conversion


def test_mass():
    assert pytest.approx(unit_conversion(1, 'kg', 'lb')) == 2.204623
    assert pytest.approx(unit_conversion(30, 'g', 'oz')) == 1.058219
    assert pytest.approx(unit_conversion(1, 'g', 'kg')) == 1e-3


def test_pressure():
    assert pytest.approx(unit_conversion(123, 'Pa', 'lbf/ft²'), 1e-6) \
        == 2.568908


def test_speed():
    assert pytest.approx(unit_conversion(10, 'kt', 'm/s'), rel=1e-3) \
        == 5.1444444


def test_force():
    assert unit_conversion(1, 'N', 'lbf') == 0.22480898166040394


def test_input():
    assert unit_conversion(1.3) == 1.3
    assert unit_conversion(1.3, "kg") == 1.3
    assert unit_conversion(1.3, "t") == 1300
    assert unit_conversion(1.3, None, "g") == 1300
    assert unit_conversion(1.3, to_unit="g") == 1300
    assert (unit_conversion([1.3, 2.4], "t") == [1300, 2400]).all()
    assert (unit_conversion(np.array([1.3, 2.4]), "t") ==
            np.array([1300, 2400])).all()


def test_string_units():
    pytest.approx(unit_conversion("10 m", to_unit="ft")) == 32.8084
    pytest.approx(unit_conversion("10 m", from_unit="m", to_unit="ft")) == \
        32.8084


def test_errors():
    with pytest.raises(ValueError):
        unit_conversion(1, from_unit='kjashdjashd')
    with pytest.raises(ValueError):
        unit_conversion(1, to_unit='kjashdjashd')
    with pytest.raises(ValueError):
        unit_conversion(1, 'kg', 'm')
    with pytest.raises(ValueError):
        unit_conversion("10 m", from_unit="mm", to_unit="ft")
    with pytest.raises(NotImplementedError):
        unit_conversion(["10 m", "20 mm"], to_unit="ft")
