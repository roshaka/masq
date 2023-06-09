'''
Tests for @masq decorator.
'''
from src.masq import masq
from unittest.mock import patch
from test_dummies.dummies import dummy_dict, dummy_dicts_list
import pytest

def test_masq_does_not_mutate_input_of_dict():
    '''Tests that masq does not mutate input dict.'''
    input =  dummy_dict()

    @masq('name')
    def foo():
        return input
    
    output = foo()
    assert input != output

def test_masq_does_not_mutate_inputs_of_dicts_list():
    '''Tests masq does not mutate input dicts list and returns new list.'''
    input =  dummy_dicts_list()

    @masq('name')
    def foo():
        return input
    
    output = foo()
    assert input != output
    assert input[0]!=output[0]

def test_masq_masks_single_target_key_of_dict():
    '''Tests masq decorator with single target_key masks target dictionary key.'''
    @masq('name')
    def foo():
        return dummy_dict()
    
    masqed_dict = foo()
    assert masqed_dict == {
        'name': '***',
        'email': 'jane@coolmail.com',
        'telephones': {
            'mobile': '07999 987654'
        },
        'status': 'excellent'
    }

def test_masq_masks_single_target_key_of_dicts_list():
    '''Tests masq with one target_key masks target key in all dictionaries in list.'''
    @masq('name')
    def foo():
        return dummy_dicts_list()
    
    masqed_dicts = foo()
    assert masqed_dicts == [
        {
        'name': '***',
        'email': 'jane@coolmail.com',
        'telephones': {
            'mobile': '07999 987654'
        },
        'status': 'excellent'
        },
         {
        'name': '***',
        'email': 'dave@wahoo.com',
        'telephones': {
            'mobile': '07787 123456'
        },
        'status': 'poor'
        }
    ]

def test_masq_masks_single_nested_target_key_of_dict():
    '''Tests masq with single nested target_key masks target key in dictionary.'''
    @masq('telephones.mobile')
    def foo():
        return dummy_dict()
    
    masqed_dict = foo()
    assert masqed_dict == {
        'name': 'Jane Smith',
        'email': 'jane@coolmail.com',
        'telephones': {
            'mobile': '***'
        },
        'status': 'excellent'
    }

def test_masq_masks_single_nested_target_key_of_dicts_list():
    '''Tests masq with one target_key masks target key in all dictionaries in list.'''
    @masq('telephones.mobile')
    def foo():
        return dummy_dicts_list()
    
    masqed_dict = foo()
    assert masqed_dict == [
        {
        'name': 'Jane Smith',
        'email': 'jane@coolmail.com',
        'telephones': {
            'mobile': '***'
        },
        'status': 'excellent'
        },
        {
        'name': 'David Jones',
        'email': 'dave@wahoo.com',
        'telephones': {
            'mobile': '***'
        },
        'status': 'poor'
        }
    ]
    
def test_masq_masks_multiple_target_keys_of_dict():
    '''Tests masq with multiple target_keys masks all target keys in dictionary.'''
    @masq('name','email')
    def foo():
        return dummy_dict()
    
    masqed_dict = foo()
    assert masqed_dict == {
        'name': '***',
        'email': '***',
        'telephones': {
            'mobile': '07999 987654'
        },
        'status': 'excellent'
    }

def test_masq_masks_multiple_target_keys_of_dicts_list():
    '''Tests masq with multiple target_keys masks target keys of each dict in list.'''
    @masq('name','email')
    def foo():
        return dummy_dicts_list()
    
    masqed_dict = foo()
    assert masqed_dict == [
        {
        'name': '***',
        'email': '***',
        'telephones': {
            'mobile': '07999 987654'
        },
        'status': 'excellent'
        },
        {
        'name': '***',
        'email': '***',
        'telephones': {
            'mobile': '07787 123456'
        },
        'status': 'poor'
        }
    ]

def test_masq_char_keyword_arg_on_dict():
    '''Tests len(masq_char)==1 generates masq_string of masq_char for dict value.'''
    @masq('name', masq_char='?')
    def foo():
        return dummy_dict()
    
    masqed_dict = foo()
    assert masqed_dict == {
        'name': '???',
        'email': 'jane@coolmail.com',
        'telephones': {
            'mobile': '07999 987654'
        },
        'status': 'excellent'
    }

def test_masq_char_keyword_arg_on_dicts_list():
    '''Tests len(masq_char)==1 generates masq_string of masq_char for dict value.'''
    @masq('name', masq_char='?')
    def foo():
        return dummy_dicts_list()
    
    masqed_dict = foo()
    assert masqed_dict == [
        {
        'name': '???',
        'email': 'jane@coolmail.com',
        'telephones': {
            'mobile': '07999 987654'
        },
        'status': 'excellent'
        },
        {
        'name': '???',
        'email': 'dave@wahoo.com',
        'telephones': {
            'mobile': '07787 123456'
        },
        'status': 'poor'
        }
    ]

def test_masq_length_keyword_arg_on_dict():
    '''Tests that masq_length controls length of masq_string for dict.'''
    @masq('name', masq_length=7)
    def foo():
        return dummy_dict()
    
    masqed_dict = foo()
    assert masqed_dict == {
        'name': '*******',
        'email': 'jane@coolmail.com',
        'telephones': {
            'mobile': '07999 987654'
        },
        'status': 'excellent'
    }

def test_masq_length_keyword_arg_on_dicts_list():
    '''Tests that masq_length controls length of masq_string for dicts list.'''
    @masq('name', masq_length=7)
    def foo():
        return dummy_dicts_list()
    
    masqed_dict = foo()
    assert masqed_dict == [
        {
        'name': '*******',
        'email': 'jane@coolmail.com',
        'telephones': {
            'mobile': '07999 987654'
        },
        'status': 'excellent'
        },
        {
        'name': '*******',
        'email': 'dave@wahoo.com',
        'telephones': {
            'mobile': '07787 123456'
        },
        'status': 'poor'
        }
    ]

def test_masq_length_maintains_length_of_original_key_if_minus_1_for_dict():
    '''Tests masq_length=-1 makes masq_length=len(value) for dicts.'''
    @masq('name', masq_length=-1)
    def foo():
        return dummy_dict()
    
    masqed_dict = foo()

    assert masqed_dict == {
        'name': '**********',
        'email': 'jane@coolmail.com',
        'telephones': {
            'mobile': '07999 987654'
        },
        'status': 'excellent'
    }

def test_masq_length_maintains_length_of_original_key_if_minus_1_for_dicts_list():
    '''Tests masq_length=-1 makes masq_length=len(value) for dicts in list.'''
    @masq('name', masq_length=-1)
    def foo():
        return dummy_dicts_list()
    
    masqed_dict = foo()

    assert masqed_dict == [
        {
        'name': '**********',
        'email': 'jane@coolmail.com',
        'telephones': {
            'mobile': '07999 987654'
        },
        'status': 'excellent'
        },
        {
        'name': '***********',
        'email': 'dave@wahoo.com',
        'telephones': {
            'mobile': '07787 123456'
        },
        'status': 'poor'
        }
    ]

@patch('src.masq._get_random_grawlix_char', return_value ='#')
def test_masq_char_equals_grawlix_dict(func):
    '''Tests masq_char="grawlix" sets target key of dict to random grawlix string.'''
    @masq('name', masq_char='grawlix')
    def foo():
        return dummy_dict()
    
    masqed_dict = foo()

    assert masqed_dict == {
        'name': '###',
        'email': 'jane@coolmail.com',
        'telephones': {
            'mobile': '07999 987654'
        },
        'status': 'excellent'
    }

@patch('src.masq._get_random_grawlix_char', return_value ='#')
def test_masq_char_equals_grawlix_dicts_list(func):
    '''Tests masq_char="grawlix" sets target key to grawlix for dicts in list.'''
    @masq('name', masq_char='grawlix')
    def foo():
        return dummy_dicts_list()
    
    masqed_dict = foo()

    assert masqed_dict == [
        {
        'name': '###',
        'email': 'jane@coolmail.com',
        'telephones': {
            'mobile': '07999 987654'
        },
        'status': 'excellent'
        },
        {
        'name': '###',
        'email': 'dave@wahoo.com',
        'telephones': {
            'mobile': '07787 123456'
        },
        'status': 'poor'
        }
    ]

@patch('src.masq._get_random_int_char', return_value ='4')
def test_masq_char_equals_numerics_dict(func):
    '''Tests masq_char="numerics" sets target key of dict to string of random ints.'''
    @masq('name', masq_char='numerics')
    def foo():
        return dummy_dict()
    
    masqed_dict = foo()

    assert masqed_dict == {
        'name': '444',
        'email': 'jane@coolmail.com',
        'telephones': {
            'mobile': '07999 987654'
        },
        'status': 'excellent'
    }

@patch('src.masq._get_random_int_char', return_value ='4')
def test_masq_char_equals_numerics_dicts_list(func):
    '''Tests masq_char="numerics" sets target keys of dicts to random int string.'''
    @masq('name', masq_char='numerics')
    def foo():
        return dummy_dicts_list()
    
    masqed_dict = foo()

    assert masqed_dict == [
        {
            'name': '444',
            'email': 'jane@coolmail.com',
            'telephones': {
                'mobile': '07999 987654'
            },
            'status': 'excellent'
        },
            {
            'name': '444',
            'email': 'dave@wahoo.com',
            'telephones': {
                'mobile': '07787 123456'
            },
            'status': 'poor'
        }
    ]

@patch('src.masq._get_random_alpha_char', return_value ='X')
def test_masq_char_equals_alphas_dict(func):
    '''Tests masq_char="alphas" sets target key of dict to random string of alphas.'''
    @masq('name', masq_char='alphas')
    def foo():
        return dummy_dict()
    
    masqed_dict = foo()

    assert masqed_dict == {
        'name': 'XXX',
        'email': 'jane@coolmail.com',
        'telephones': {
            'mobile': '07999 987654'
        },
        'status': 'excellent'
    }

@patch('src.masq._get_random_alpha_char', return_value ='X')
def test_masq_char_equals_alphas_dicts_list(func):
    '''Tests masq_char="alphas" sets target key of dicts in list to random alphas.'''
    @masq('name', masq_char='alphas')
    def foo():
        return dummy_dicts_list()
    
    masqed_dict = foo()

    assert masqed_dict == [
        {
        'name': 'XXX',
        'email': 'jane@coolmail.com',
        'telephones': {
            'mobile': '07999 987654'
        },
        'status': 'excellent'
        },
        {
        'name': 'XXX',
        'email': 'dave@wahoo.com',
        'telephones': {
            'mobile': '07787 123456'
        },
        'status': 'poor'
        }
    ]

def test_mask_string_overwrites_other_params_and_sets_value_equal_to_mask_string():
    '''Tests masq_string!="" sets target_key=masq_string.'''
    @masq('name', 'email', masq_string='REDACTED')
    def foo():
        return dummy_dict()
    
    masqed_dict = foo()

    assert masqed_dict == {
        'name': 'REDACTED',
        'email': 'REDACTED',
        'telephones': {
            'mobile': '07999 987654'
        },
        'status': 'excellent'
    }

def test_masq_max_length_limits_masq_string_dict():
    '''Tests max_length is limited to max_masq_length for key in dict.'''
    with pytest.warns(Warning):
        @masq('name', masq_length=100, emit_warnings=False )
        def foo():
            return dummy_dict()
    
    masqed_dict = foo()

    assert masqed_dict == {
        'name': '********************************',
        'email': 'jane@coolmail.com',
        'telephones': {
            'mobile': '07999 987654'
        },
        'status': 'excellent'
    }

def test_masq_max_length_limits_masq_string_dicts_list():
    '''Tests max_length is limited to max_masq_length for key in dicts list.'''
    with pytest.warns(Warning):
        @masq('name', masq_length=100, emit_warnings=False)
        def foo():
            return dummy_dicts_list()
    
    masqed_dict = foo()

    assert masqed_dict == [
        {
            'name': '********************************',
            'email': 'jane@coolmail.com',
            'telephones': {
                'mobile': '07999 987654'
            },
            'status': 'excellent'
        },
        {
            'name': '********************************',
            'email': 'dave@wahoo.com',
            'telephones': {
                'mobile': '07787 123456'
            },
            'status': 'poor'
        }
    ]

def test_masq_value_that_is_dict():
    '''Tests keys with non string values/objects are set to masq_string.'''
    @masq('telephones')
    def foo():
        return dummy_dict()
    
    output = foo()

    assert output == {
        'name': 'Jane Smith',
        'email': 'jane@coolmail.com',
        'telephones': '***',
        'status': 'excellent'
    }

def test_for_multiple_deeply_nested_values_():
    '''Tests masqing of deeply nested keys for dicts.'''
    @masq('telephones.mobiles.home', 'hobbies.more coding', 'name', masq_length=-1)
    def foo():
        return {
        'name' : 'Dan',
        'hobbies' : {
            'coding': 'yes',
            'more coding' : 'also yes'
        },
        'telephones': {
            'mobiles': {
                'work' : '0123456789',
                'home' : 9876543210
            },
            'landline' : '1122334455'
        }
    }

    actual = foo()

    assert actual == {
        'name' : '***',
        'hobbies' : {
            'coding': 'yes',
            'more coding' : '********'
        },
        'telephones': {
            'mobiles': {
                'work' : '0123456789',
                'home' : '***'
            },
            'landline' : '1122334455'
        }
    }

def test_for_non_string_keys_dict():
    '''Tests non string keys can be masqed for single dict.'''
    input = {
            'name': 'Jane Smith',
            5: 6,
            'email': 'jane@coolmail.com',
            True : '1234567890',
            3.14: 1.0
        }

    @masq(5,'name',True,3.14, masq_char='?', masq_length=-1)
    def foo():
        return input

    output = foo()
    assert output == {
            'name': '??????????',
            5: '???',
            'email': 'jane@coolmail.com',
            True: '??????????',
            3.14: '???'
        }
    
def test_for_non_string_keys_dicts_list():
    '''Tests non string keys can be masqed for single dict.'''
    input = {
            'name': 'Jane Smith',
            5: 6,
            'email': 'jane@coolmail.com',
            True : '1234567890',
            3.14: 1.0
        }

    @masq(5,'name',True,3.14, masq_char='?', masq_length=-1)
    def foo():
        return input

    output = foo()
    assert output == {
            'name': '??????????',
            5: '???',
            'email': 'jane@coolmail.com',
            True: '??????????',
            3.14: '???'
        }
