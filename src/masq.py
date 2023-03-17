from random import choice, randint
from warnings import warn
from src.masq_warnings import *
from src.masq_errors import *
from src.masq_constant import *
from copy import deepcopy

def masq(*target_keys, masq_char='*', masq_length=3, masq_string=''):
    '''Decorate a func that returns a deep copied dictionary to mask target key's value.'''
    
    _validate_masq_char(masq_char)
    _validate_masq_length(masq_length)
    _validate_masq_string(masq_string)

    def wrapper_2(func):
        def wrapper_1():
            output = func()
            if isinstance(output, list):
                if all([isinstance(d, dict) for d in output]):
                    return [_masq_dict(target_keys, d, masq_char, masq_length, masq_string) for d in output]
            elif isinstance(output, dict):
                return _masq_dict(target_keys, output, masq_char, masq_length, masq_string)
            else:
                raise FunctionReturnTypeError(f'{func.__name__} does not return a dictionary or list of dictionaries and cannot be decorated with @masq')
        return wrapper_1
    return wrapper_2

# utility funcs

def _masq_dict(target_keys, target_dict, masq_char, masq_length, masq_string):
    
    copy_dict = deepcopy(target_dict)
    if not len(target_keys):
        return copy_dict

    for target_key in target_keys:
        _masq_key(target_key, copy_dict, masq_char, masq_length, masq_string)
        
    return copy_dict

def _masq_key(target_key, target_dict, masq_char, masq_length, masq_string):
    try:
        keys = target_key.split('.')
        if len(keys) == 1:
            key=keys[0]
            masq = _generate_masq_string(target_dict[key], masq_char, masq_length, masq_string)
            target_dict[key] = masq
        else :
            nested_dict = target_dict[keys[0]]
            next_target_key = '.'.join(keys[1:])
            _masq_key(next_target_key, nested_dict, masq_char, masq_length, masq_string)
    except:
        raise MasqKeyError()

#masq_string generation

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

# validate decorator arguments

def _validate_masq_length(masq_length):
    if not isinstance(masq_length,int):
        raise MasqLengthError("masq_length must be an integer.")
    
    if masq_length < -1:
        raise MasqLengthError("masq_length must be -1 or greater.")
    
    if masq_length > MAX_MASQ_LENGTH:
        warn(f'masq_length must be less than or equal to {MAX_MASQ_LENGTH}', MasqLengthWarning)
    
def _validate_masq_string(masq_string):
    if not isinstance(masq_string,str):
        raise MasqStringError(f'masq_string "{masq_string}" must be a string')
    
    if len(masq_string) > MAX_MASQ_LENGTH:
        raise MasqStringError(f'masq_string "{masq_string}" must have a length <= {MAX_MASQ_LENGTH}')

def _validate_masq_char(masq_char):
    if not isinstance(masq_char,str):
        raise MasqCharError(f'masq_char "{masq_char}" must be type string')
    
    if len(masq_char) > 1 and masq_char not in masq_char_specials():
        raise MasqCharError(f'masq_char "{masq_char}" must be a str of length 1 or one of the following special strings:\n{masq_char_specials()}')


