'''Functions used to return a dictionary or list of dictionaries for testing.'''
def dummy_dict():
    '''Returns a dict for simplifed testing setup.'''
    return {
        'name': 'Jane Smith',
        'email': 'jane@coolmail.com',
        'telephones': {
            'mobile': '07999 987654'
        },
        'status': 'excellent'
    }

def dummy_dicts_list():
    '''Returns a list of dicts for simplifed testing setup.'''
    return [
        {
        'name': 'Jane Smith',
        'email': 'jane@coolmail.com',
        'telephones': {
            'mobile': '07999 987654'
        },
        'status': 'excellent'
        },
        {
        'name': 'David Jones',
        'email': 'dave@wahoo.com',
        'telephones': {
            'mobile': '07787 123456'
        },
        'status': 'poor'
        }
    ]