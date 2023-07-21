EXPECTED = {'PKCS-10': {'extensibility-implied': False,
             'imports': {'AuthenticationFramework': ['ALGORITHM'],
                         'InformationFramework': ['ATTRIBUTE', 'Name'],
                         'UsefulDefinitions': ['authenticationFramework',
                                               'informationFramework']},
             'object-classes': {},
             'object-sets': {'CRIAttributes': {'class': 'ATTRIBUTE',
                                               'members': ['.']},
                             'PKInfoAlgorithms': {'class': 'ALGORITHM',
                                                  'members': ['.']},
                             'SignatureAlgorithms': {'class': 'ALGORITHM',
                                                     'members': ['.']}},
             'tags': 'IMPLICIT',
             'types': {'AlgorithmIdentifier': {'members': [{'name': 'algorithm',
                                                            'table': {'type': 'IOSet'},
                                                            'type': 'ALGORITHM.&id'},
                                                           {'name': 'parameters',
                                                            'optional': True,
                                                            'table': ['IOSet',
                                                                      ['algorithm']],
                                                            'type': 'ALGORITHM.&Type'}],
                                               'parameters': ['IOSet'],
                                               'type': 'SEQUENCE'},
                       'Attribute': {'members': [{'name': 'type',
                                                  'table': {'type': 'IOSet'},
                                                  'type': 'ATTRIBUTE.&id'},
                                                 {'element': {'table': ['IOSet',
                                                                        ['type']],
                                                              'type': 'ATTRIBUTE.&Type'},
                                                  'name': 'values',
                                                  'size': [(1, 'MAX')],
                                                  'type': 'SET OF'}],
                                     'parameters': ['IOSet'],
                                     'type': 'SEQUENCE'},
                       'Attributes': {'element': {'actual-parameters': ['{'],
                                                  'type': 'Attribute'},
                                      'parameters': ['IOSet'],
                                      'type': 'SET OF'},
                       'CertificationRequest': {'members': [{'name': 'certificationRequestInfo',
                                                             'type': 'CertificationRequestInfo'},
                                                            {'actual-parameters': ['{'],
                                                             'name': 'signatureAlgorithm',
                                                             'type': 'AlgorithmIdentifier'},
                                                            {'name': 'signature',
                                                             'type': 'BIT '
                                                                     'STRING'}],
                                                'type': 'SEQUENCE'},
                       'CertificationRequestInfo': {'members': [{'name': 'version',
                                                                 'named-numbers': {'v1': 0},
                                                                 'restricted-to': ['v1',
                                                                                   None],
                                                                 'type': 'INTEGER'},
                                                                {'name': 'subject',
                                                                 'type': 'Name'},
                                                                {'actual-parameters': ['{'],
                                                                 'name': 'subjectPKInfo',
                                                                 'type': 'SubjectPublicKeyInfo'},
                                                                {'actual-parameters': ['{'],
                                                                 'name': 'attributes',
                                                                 'tag': {'number': 0},
                                                                 'type': 'Attributes'}],
                                                    'type': 'SEQUENCE'},
                       'SubjectPublicKeyInfo': {'members': [{'actual-parameters': ['{'],
                                                             'name': 'algorithm',
                                                             'type': 'AlgorithmIdentifier'},
                                                            {'name': 'subjectPublicKey',
                                                             'type': 'BIT '
                                                                     'STRING'}],
                                                'parameters': ['IOSet'],
                                                'type': 'SEQUENCE'}},
             'values': {}}}