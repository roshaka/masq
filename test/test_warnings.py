from src.masq import masq, masqs
from unittest.mock import patch
from src.utils.dummies import dummy_dict
import pytest

def test_conflicting_masq_decorator_params_raise_warning():
    @masq('name', 'email', masq_string='REDACTED', masq_char='s')
    def foo():
        return dummy_dict()

    with pytest.warns():
        foo()