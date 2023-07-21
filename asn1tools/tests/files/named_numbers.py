EXPECTED = {'Foo': {'extensibility-implied': False,
         'imports': {},
         'object-classes': {},
         'object-sets': {},
         'tags': 'AUTOMATIC',
         'types': {'A': {'restricted-to': [('min', 'max')],
                         'type': 'Constants'},
                   'B': {'restricted-to': ['unknown'], 'type': 'Constants'},
                   'C': {'restricted-to': [('zero', 'max')],
                         'type': 'Constants'},
                   'Constants': {'named-numbers': {'max': 1,
                                                   'min': -1,
                                                   'unknown': 2},
                                 'restricted-to': [(-1, 2)],
                                 'type': 'INTEGER'}},
         'values': {'min': {'type': 'INTEGER', 'value': 3},
                    'zero': {'type': 'INTEGER', 'value': 0}}}}