EXPECTED = {'X691-A2': {'extensibility-implied': False,
             'imports': {},
             'object-classes': {},
             'object-sets': {},
             'types': {'ChildInformation': {'members': [{'name': 'name',
                                                         'type': 'Name'},
                                                        {'name': 'dateOfBirth',
                                                         'tag': {'number': 0},
                                                         'type': 'Date'}],
                                            'type': 'SET'},
                       'Date': {'from': [('0', '9')],
                                'size': [8],
                                'tag': {'class': 'APPLICATION',
                                        'kind': 'IMPLICIT',
                                        'number': 3},
                                'type': 'VisibleString'},
                       'EmployeeNumber': {'tag': {'class': 'APPLICATION',
                                                  'kind': 'IMPLICIT',
                                                  'number': 2},
                                          'type': 'INTEGER'},
                       'Name': {'members': [{'name': 'givenName',
                                             'type': 'NameString'},
                                            {'name': 'initial',
                                             'size': [1],
                                             'type': 'NameString'},
                                            {'name': 'familyName',
                                             'type': 'NameString'}],
                                'tag': {'class': 'APPLICATION',
                                        'kind': 'IMPLICIT',
                                        'number': 1},
                                'type': 'SEQUENCE'},
                       'NameString': {'from': [('a', 'z'),
                                               ('A', 'Z'),
                                               ('-', '-'),
                                               ('.', '.')],
                                      'size': [(1, 64)],
                                      'type': 'VisibleString'},
                       'PersonnelRecord': {'members': [{'name': 'name',
                                                        'type': 'Name'},
                                                       {'name': 'title',
                                                        'tag': {'number': 0},
                                                        'type': 'VisibleString'},
                                                       {'name': 'number',
                                                        'type': 'EmployeeNumber'},
                                                       {'name': 'dateOfHire',
                                                        'tag': {'number': 1},
                                                        'type': 'Date'},
                                                       {'name': 'nameOfSpouse',
                                                        'tag': {'number': 2},
                                                        'type': 'Name'},
                                                       {'default': [],
                                                        'element': {'type': 'ChildInformation'},
                                                        'name': 'children',
                                                        'tag': {'kind': 'IMPLICIT',
                                                                'number': 3},
                                                        'type': 'SEQUENCE OF'}],
                                           'tag': {'class': 'APPLICATION',
                                                   'kind': 'IMPLICIT',
                                                   'number': 0},
                                           'type': 'SET'}},
             'values': {}}}