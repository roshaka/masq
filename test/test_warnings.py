from src.masq import masq
from test_dummies.dummies import dummy_dict
import pytest

def test_conflicting_masq_decorator_params_raise_warning():
    @masq('name', 'email', masq_string='REDACTED', masq_char='s')
    def foo():
        return dummy_dict()

    with pytest.warns():
        foo()