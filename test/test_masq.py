from src.masq import masq


def test_masq_decorator_returns_original_dictionary_if_no_target_keys():
    '''Tests that the original dictionary object is returned if no target_keys sepecified in the masq'''
    input =  dummy_dict()

    @masq()
    def foo():
        return input
    
    output = foo()
    assert input == output

def test_masq_decorator_masks_single_target_key():
    '''Tests that masq decorator with single target_key masks target dictionary key'''
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
    
def test_masq_decorator_masks_multiple_target_keys():
    '''Tests that masq decorator with multiple target_keys masks all target dictionary keys'''
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

def test_masq_char_keyword_param():
    '''Tests that the masked value is created by the masq_char'''
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

# Utility functions for testing
def dummy_dict():
    '''Returns a dict for simplifed testing setup'''
    return {
        'name': 'Jane Smith',
        'email': 'jane@coolmail.com',
        'telephones': {
            'mobile': '07999 987654'
        },
        'status': 'excellent'
    }