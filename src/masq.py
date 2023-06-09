"""
This module can mask the values of dictionaries by using the @masq decorator.
Keys passed to @masq will replace their paired value with a masq string.
@masq can decorate functions that return a dictionary of list of dictionaries. 

To generate HTML documentation for this module issue commands with pydoc
"""
from random import choice, randint
from warnings import warn
from src.masq_warnings import MasqLengthWarning, NonStringWarning, MasqKeywordConflict
from src.masq_errors import MasqLengthError,  MasqStringError, MasqCharError
from src.masq_errors import FunctionReturnTypeError, MasqKeyError
from src.masq_constant import MAX_MASQ_LENGTH, DEFAULT_MASQ_LENGTH, masq_char_specials
from copy import deepcopy

def masq(
        *target_keys, 
        masq_char='*',
        masq_length=3,
        masq_string='',
        emit_warnings=False
    ):
    '''
    Decorate a function that returns a dict or list of dicts to mask selected values.

    Parameters:

        *target_keys: The keys of the dictionary to be masked.
            @masg can take any number of *args.
            Valid inputs are of type:
                - string
                - int
                - float
                - bool
            
            Use dot notation to access nested keys if all eg "deep.nested.key".
            All nested keys must be strings.

        masq_char: The char to be used in the generated masq_string.
            default = '*'
            Valid inputs are:
                - a string of length 1 eg. 'x', '?', '0', '-'
                - 'grawlax' returns random string eg. '!$?&*#'
                - 'alphas' returns random string eg. 'khJLIpxvQs'
                - 'numerics' returns random string eg. '091248191'

        masq_length: The length of the generated_masq string.
            default = 3
            Valid lengths are:
                - 0 <= len <=32
                - -1 sets masq_length equal to the len(value) if type(value) i string

        masq_string: A custom masq string to be applied.
            default = ''
            Ignored if default. len(masq_string) must be <= 32.s
            Setting a custom masq_string will override other @masq arguments.

        emit_warnings: Controls whether warnings are logged to the console.
            default = False
            Warnings are emitted when conflicting args could cause unexpected results.

    Returns:

        If decorating a function that returns a dict:
            dict: The values are replaced with the masq_string
        If decorating a function that returns a list of dicts:
            list of dicts: The values of each dict are replaced with the masq_string
    '''
    if not isinstance(masq_length,int):
        raise MasqLengthError('masq_length must be an integer')
    
    if masq_length < -1:
        raise MasqLengthError('masq_length must be -1 or greater')
    
    if masq_length > MAX_MASQ_LENGTH:
        warn(f'masq_length must be >= to {MAX_MASQ_LENGTH}', MasqLengthWarning)

    if not isinstance(masq_string,str):
        raise MasqStringError(f'masq_string "{masq_string}" must be a string')
    
    if len(masq_string) > MAX_MASQ_LENGTH:
        raise MasqStringError(f'len("{masq_string}") must be <= {MAX_MASQ_LENGTH}')

    if not isinstance(masq_char,str):
        raise MasqCharError(f'masq_char "{masq_char}" must be type string')
    
    if len(masq_char) > 1 and masq_char not in masq_char_specials():
        raise MasqCharError(f'"{masq_char}" is an invalid masq_char')

    def wrapper_2(func):
        def wrapper_1():
            output = func()
            if isinstance(output, list):
                if all([isinstance(d, dict) for d in output]):
                    return [
                        _masq_dict(
                            target_keys, 
                            d, 
                            masq_char,
                            masq_length, 
                            masq_string,
                            emit_warnings
                        )
                        for d in output]
            elif isinstance(output, dict):
                return _masq_dict(
                    target_keys, 
                    output, 
                    masq_char,
                    masq_length,
                    masq_string,
                    emit_warnings
                )
            else:
                raise FunctionReturnTypeError(f'{func.__name__} cannot be masqed')
        return wrapper_1
    return wrapper_2

# utility funcs

def _masq_dict(
        target_keys,
        target_dict,
        masq_char,
        masq_length, 
        masq_string,
        hide_warnings
    ):
    copy_dict = deepcopy(target_dict)
    if not len(target_keys):
        return copy_dict

    for target_key in target_keys:
        _masq_key(
            target_key,
            copy_dict,
            masq_char,
            masq_length,
            masq_string,
            hide_warnings
        )
    return copy_dict

def _masq_key(
        target_key,
        target_dict,
        masq_char,
        masq_length,
        masq_string,
        hide_warnings
    ):
    try:
        if isinstance(target_key, str):
            keys = target_key.split('.')
        else:
            keys=[target_key]
        if len(keys) == 1:
            key=keys[0]
            masq = _generate_masq_string(
                target_dict[key],
                masq_char,
                masq_length,
                masq_string,
                hide_warnings
            )
            target_dict[key] = masq
        else :
            nested_dict = target_dict[keys[0]]
            next_target_key = '.'.join(keys[1:])
            _masq_key(
                next_target_key, 
                nested_dict, 
                masq_char, 
                masq_length, 
                masq_string,
                hide_warnings
            )
    except Exception:
        raise MasqKeyError(f'{target_key} is not a valid dict key in this dictionary')

#masq_string generation

def _generate_masq_string(
        value_to_masq,
        masq_char,
        masq_length,
        masq_string,
        emit_warnings
    ):
    if masq_string != '':
        if masq_char!='*' or masq_length!=3:
            if emit_warnings:
                warn('masq_string overrides other args', MasqKeywordConflict)
        return masq_string
    
    def _masq_char():
        return masq_char
    
    if len(masq_char)==1 :
        masq_func = _masq_char
    elif masq_char == 'grawlix':
        masq_func = _get_random_grawlix_char
    elif masq_char == 'numerics':
        masq_func = _get_random_int_char
    elif masq_char == 'alphas':
        masq_func = _get_random_alpha_char
    else: 
        raise MasqCharError(f'{masq_char} is not a valid masq_char value')

    masqed_value_chars=[]

    if not isinstance(value_to_masq, str) and masq_length == -1:
        masq_length = DEFAULT_MASQ_LENGTH
        if emit_warnings:
            warn(f'"{value_to_masq}" is not a string', NonStringWarning)
    else:
        masq_length = masq_length if masq_length >=0 else len(value_to_masq)
        masq_length = MAX_MASQ_LENGTH if masq_length > MAX_MASQ_LENGTH else masq_length

    for i in range(masq_length):
         masqed_value_chars.append(masq_func())

    return ''.join(masqed_value_chars)

def _get_random_grawlix_char():
    return choice(['!','@','£','$','%','&','*','?','#','~'])

def _get_random_int_char():
    return randint(0,9)

def _get_random_alpha_char():
    ascii=list(range(67,91))+(list(range(97,123)))
    return chr(choice(ascii))
