
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
                    new_dict[key]=masq_char*int(masq_length)
                else: new_dict[key]=target_dict[key]
            return new_dict
        return wrapper_1
    return wrapper_2
