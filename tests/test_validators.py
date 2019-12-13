import pytest

from statham.validators import has_format, NotPassed


def test_format_checker_warns_if_passed_unknown_format():
    with pytest.warns(RuntimeWarning):
        # False positive
        # pylint: disable=no-value-for-parameter
        has_format("unknown-format")(None, None, "foo")


class TestNotPassed:
    @staticmethod
    def test_not_passed_bool_value():
        assert not NotPassed()

    @staticmethod
    def test_not_passed_singleton():
        assert NotPassed() is NotPassed()

    @staticmethod
    def test_not_passed_repr():
        assert repr(NotPassed()) == "NotPassed"