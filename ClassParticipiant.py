import parser_prot


class Participiant:
    def get_inn(self, application):
        d = parser_prot.get_el(application, 'appParticipant', 'inn') or parser_prot.get_el(application,
                                                                                           'appParticipant',
                                                                                           'idNumber') or parser_prot.get_el(
                application, 'appParticipants', 'appParticipant', 'idNumber') or parser_prot.get_el(application,
                                                                                                    'appParticipants',
                                                                                                    'appParticipant',
                                                                                                    'inn') or parser_prot.get_el(
                application,
                'appParticipantInfo',
                'individualPersonRFInfo',
                'INN') or parser_prot.get_el(
                application,
                'appParticipantInfo',
                'legalEntityRFInfo',
                'INN')
        return d

    def get_kpp(self, application):
        d = parser_prot.get_el(application, 'appParticipant', 'kpp') or parser_prot.get_el(application,
                                                                                           'appParticipants',
                                                                                           'appParticipant',
                                                                                           'kpp') or parser_prot.get_el(
                application,
                'appParticipantInfo',
                'legalEntityRFInfo',
                'KPP') or parser_prot.get_el(
                application,
                'appParticipantInfo',
                'individualPersonRFInfo',
                'KPP') or parser_prot.get_el(
                application,
                'appParticipantInfo',
                'legalEntityRFInfo',
                'KPP')
        return d

    def get_organization_name(self, application):
        d = parser_prot.get_el(application, 'appParticipant', 'organizationName') or parser_prot.get_el(application,
                                                                                                        'appParticipants',
                                                                                                        'appParticipant',
                                                                                                        'organizationName') or parser_prot.get_el(
                application,
                'appParticipantInfo',
                'legalEntityRFInfo',
                'fullName')
        if not d:
            lastName = parser_prot.get_el(application, 'appParticipant', 'contactInfo',
                                          'lastName') or parser_prot.get_el(application, 'appParticipants',
                                                                            'appParticipant', 'contactInfo',
                                                                            'lastName') or parser_prot.get_el(
                    application, 'appParticipantInfo',
                    'individualPersonRFInfo', 'nameInfo', 'lastName')
            firstName = parser_prot.get_el(application, 'appParticipant', 'contactInfo',
                                           'firstName') or parser_prot.get_el(application, 'appParticipants',
                                                                              'appParticipant', 'contactInfo',
                                                                              'firstName') or parser_prot.get_el(
                    application, 'appParticipantInfo',
                    'individualPersonRFInfo', 'nameInfo', 'firstName')
            middleName = parser_prot.get_el(application, 'appParticipant', 'contactInfo',
                                            'middleName') or parser_prot.get_el(application, 'appParticipants',
                                                                                'appParticipant', 'contactInfo',
                                                                                'middleName') or parser_prot.get_el(
                    application, 'appParticipantInfo',
                    'individualPersonRFInfo', 'nameInfo', 'middleName')
            d = f"{lastName} {firstName} {middleName}".strip()
        return d

    def get_participant_type(self, application):
        d = parser_prot.get_el(application, 'appParticipant', 'participantType') or parser_prot.get_el(application,
                                                                                                       'appParticipants',
                                                                                                       'appParticipant',
                                                                                                       'participantType')
        return d

    def get_country_full_name(self, application):
        d = parser_prot.get_el(application, 'appParticipant', 'country', 'countryFullName') or parser_prot.get_el(
                application,
                'appParticipants',
                'appParticipant', 'country',
                'countryFullName')
        return d

    def get_post_address(self, application):
        d = parser_prot.get_el(application, 'appParticipant', 'postAddress') or parser_prot.get_el(application,
                                                                                                   'appParticipants',
                                                                                                   'appParticipant',
                                                                                                   'postAddress') or parser_prot.get_el(
                application,
                'appParticipantInfo',
                'individualPersonRFInfo',
                'postAddress')
        return d
