from random import choice, randint
from warnings import warn
from src.masq_warnings import *
from src.masq_errors import *
from src.masq_constant import *

def masq(*target_keys, masq_char='*', masq_length=3, masq_string=''):
    '''Decorate a func that returns a dictionary to mask target key's value.'''
    
    #validate decorator inputs
    _validate_masq_length(masq_length)

    def wrapper_2(func):
        def wrapper_1():
            dictionary = func()
            if type(dictionary) is not dict:
                raise FunctionReturnTypeError(f'{func.__name__} does not return a dictionary and cannot be decorated with @masq')
            return _masq_dict(target_keys, dictionary, masq_char, masq_length, masq_string)
        return wrapper_1
    return wrapper_2

def masqs(*target_keys, masq_char='*', masq_length=3, masq_string=''):
    '''Returns a list of shallow copied dictionaries with masked target_keys values.'''
    def wrapper_2(func):
        def wrapper_1():
            dicts = func()
            if not isinstance(dicts, list):
                e = f'{func.__name__} does not return a list of dictionaries and cannot be decorated with @masqs'
                raise FunctionReturnTypeError(e)
            if not all(isinstance(d, dict) for d in dicts):
                raise FunctionReturnTypeError(f'{d} is not a dictionary and so {func.__name__} cannot be decorated with @masqs')
            return [_masq_dict(target_keys, d, masq_char, masq_length, masq_string) for d in dicts]
        return wrapper_1
    return wrapper_2

# utility funcs

def _masq_dict(target_keys, target_dict, masq_char='*', masq_length=3, masq_string=''):
    if not len(target_keys):
        return target_dict
    
    keys = target_dict.keys()
    new_dict={}

    for target_key in target_keys:
        if target_key not in keys:
            raise MasqKeyError()

    for key in keys:
        if key in target_keys:
            masqed_value = _generate_masq_string(
                target_dict[key],
                masq_char,
                masq_length,
                masq_string
            )
            new_dict[key]= masqed_value
        else: new_dict[key]=target_dict[key]
    return new_dict

def _generate_masq_string(value_to_masq, masq_char='*', masq_length=3, masq_string=''):
    
    if masq_string != '':
        if masq_char!='*' or masq_length!=3:
            warn('masq_string overrides the other parameters in the masq decorator so may lead to unexpected masqing', MasqKeywordArgumentConflict )
        return masq_string
    
    masq_length = masq_length if masq_length >=0 else len(value_to_masq)
    masq_length = MAX_MASQ_LENGTH if masq_length > MAX_MASQ_LENGTH else masq_length

    masqed_value_chars=[]
    masq_func= None
    
    if len(masq_char)==1 :
        masq_func = lambda : masq_char
    elif masq_char == 'grawlix':
        masq_func = _get_random_grawlix_char
    elif masq_char == 'numerics':
        masq_func = _get_random_int_char
    elif masq_char == 'alphas':
        masq_func = _get_random_alpha_char
    else: raise Exception

    for i in range(masq_length):
         masqed_value_chars.append(masq_func())

    return ''.join(masqed_value_chars)

def _get_random_grawlix_char():
    return choice(['!','@','£',"$",'%','&','*','?','#','~'])

def _get_random_int_char():
    return randint(0,9)

def _get_random_alpha_char():
    ascii_alphas = list(range(67,91))
    ascii_alphas.extend(list(range(97,123)))
    return chr(choice(ascii_alphas))

# validate decorator input
def _validate_masq_length(masq_length):
    if type(masq_length) is not int:
        raise MasqLengthError("masq_length must be an integer.")
    
    if masq_length < -1:
        raise MasqLengthError("masq_length must be -1 or greater.")
    
    if masq_length > MAX_MASQ_LENGTH:
        warn(f'masq_length must be less than or equal to {MAX_MASQ_LENGTH}', MasqLengthWarning)
