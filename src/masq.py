from random import choice

def masq(*target_keys, masq_char='*', masq_length=3):
    '''Decorate a func that returns a dictionary to mask target key's value'''
    def wrapper_2(func):
        def wrapper_1():
            target_dict = func()
            if not len(target_keys):
                return target_dict
            keys = target_dict.keys()
            new_dict={}
            for key in keys:
                if key in target_keys:
                    masqed_value = _generate_masq_string(
                        target_dict[key],
                        masq_char,
                        masq_length,
                    )
                    new_dict[key]= masqed_value
                else: new_dict[key]=target_dict[key]
            return new_dict
        return wrapper_1
    return wrapper_2

def _generate_masq_string(value, masq_char='*', masq_length=3):
    masq_length = masq_length if masq_length >=0 else len(value)
    
    masqed_value_chars=[]
    for i in range(masq_length):
        masqed_value_chars.append(masq_char if masq_char!='grawlix' else _get_grawlix_char())

    return ''.join(masqed_value_chars)

def _get_grawlix_char():
    return choice(['!','@','£',"$",'%','&','*','?','#','~'])

