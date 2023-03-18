from random import choice, randint
from warnings import warn
from src.masq_warnings import *
from src.masq_errors import *
from src.masq_constant import *
from copy import deepcopy

def masq(*target_keys, masq_char='*', masq_length=3, masq_string=''):
    '''Decorate a func that returns a deep copied dictionary to mask target key's value.'''
    if not isinstance(masq_length,int):
        raise MasqLengthError(ERR_01())
    
    if masq_length < -1:
        raise MasqLengthError(ERR_02())
    
    if masq_length > MAX_MASQ_LENGTH:
        warn(WARN_01, MasqLengthWarning)

    if not isinstance(masq_string,str):
        raise MasqStringError(ERR_03(masq_string))
    
    if len(masq_string) > MAX_MASQ_LENGTH:
        raise MasqStringError(ERR_04(masq_string))

    if not isinstance(masq_char,str):
        raise MasqCharError(ERR_03(masq_char))
    
    if len(masq_char) > 1 and masq_char not in masq_char_specials():
        raise MasqCharError(ERR_05(masq_char))

    def wrapper_2(func):
        def wrapper_1():
            output = func()
            if isinstance(output, list):
                if all([isinstance(d, dict) for d in output]):
                    return [_masq_dict(target_keys, d, masq_char, masq_length, masq_string) for d in output]
            elif isinstance(output, dict):
                return _masq_dict(target_keys, output, masq_char, masq_length, masq_string)
            else:
                raise FunctionReturnTypeError(ERR_06(func.__name__))
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
    
    if len(masq_char)==1 :
        masq_func = lambda : masq_char
    elif masq_char == 'grawlix':
        masq_func = _get_random_grawlix_char
    elif masq_char == 'numerics':
        masq_func = _get_random_int_char
    elif masq_char == 'alphas':
        masq_func = _get_random_alpha_char
    else: raise Exception

    masqed_value_chars=[]

    if not isinstance(value_to_masq, str) and masq_length == -1:
        masq_length = DEFAULT_MASQ_LENGTH
        warn(f'hey', NonStringWarning)
    else:
        masq_length = masq_length if masq_length >=0 else len(value_to_masq)
        masq_length = MAX_MASQ_LENGTH if masq_length > MAX_MASQ_LENGTH else masq_length

    for i in range(masq_length):
         masqed_value_chars.append(masq_func())

    return ''.join(masqed_value_chars)

def _get_random_grawlix_char():
    return choice(['!','@','£',"$",'%','&','*','?','#','~'])

def _get_random_int_char():
    return randint(0,9)

def _get_random_alpha_char():
    ascii=list(range(67,91))+(list(range(97,123)))
    return chr(choice(ascii))
