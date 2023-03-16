from src.masq import masq
from src.masq_errors import *
from test_dummies.dummies import dummy_dict
import pytest

def test_invalid_target_key_raises_InvalidMasqKeyError():
    @masq('banana')
    def foo():
        return dummy_dict()

    with pytest.raises(InvalidMasqKeyError):
        foo()