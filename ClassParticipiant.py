import UtilsFunctions


class Participiant:
    def get_inn(self, application):
        d = UtilsFunctions.get_el(application, 'appParticipant', 'inn') or UtilsFunctions.get_el(application,
                                                                                           'appParticipant',
                                                                                                 'idNumber') or UtilsFunctions.get_el(
                application, 'appParticipants', 'appParticipant', 'idNumber') or UtilsFunctions.get_el(application,
                                                                                                    'appParticipants',
                                                                                                    'appParticipant',
                                                                                                       'inn') or UtilsFunctions.get_el(
                application,
                'appParticipantInfo',
                'individualPersonRFInfo',
                'INN') or UtilsFunctions.get_el(
                application,
                'appParticipantInfo',
                'legalEntityRFInfo',
                'INN')
        return d

    def get_kpp(self, application):
        d = UtilsFunctions.get_el(application, 'appParticipant', 'kpp') or UtilsFunctions.get_el(application,
                                                                                           'appParticipants',
                                                                                           'appParticipant',
                                                                                                 'kpp') or UtilsFunctions.get_el(
                application,
                'appParticipantInfo',
                'legalEntityRFInfo',
                'KPP') or UtilsFunctions.get_el(
                application,
                'appParticipantInfo',
                'individualPersonRFInfo',
                'KPP') or UtilsFunctions.get_el(
                application,
                'appParticipantInfo',
                'legalEntityRFInfo',
                'KPP')
        return d

    def get_organization_name(self, application):
        d = UtilsFunctions.get_el(application, 'appParticipant', 'organizationName') or UtilsFunctions.get_el(
            application,
                                                                                                        'appParticipants',
                                                                                                        'appParticipant',
            'organizationName') or UtilsFunctions.get_el(
                application,
                'appParticipantInfo',
                'legalEntityRFInfo',
                'fullName')
        if not d:
            lastName = UtilsFunctions.get_el(application, 'appParticipant', 'contactInfo',
                                             'lastName') or UtilsFunctions.get_el(application, 'appParticipants',
                                                                            'appParticipant', 'contactInfo',
                                                                                  'lastName') or UtilsFunctions.get_el(
                    application, 'appParticipantInfo',
                    'individualPersonRFInfo', 'nameInfo', 'lastName')
            firstName = UtilsFunctions.get_el(application, 'appParticipant', 'contactInfo',
                                              'firstName') or UtilsFunctions.get_el(application, 'appParticipants',
                                                                              'appParticipant', 'contactInfo',
                                                                                    'firstName') or UtilsFunctions.get_el(
                    application, 'appParticipantInfo',
                    'individualPersonRFInfo', 'nameInfo', 'firstName')
            middleName = UtilsFunctions.get_el(application, 'appParticipant', 'contactInfo',
                                               'middleName') or UtilsFunctions.get_el(application, 'appParticipants',
                                                                                'appParticipant', 'contactInfo',
                                                                                      'middleName') or UtilsFunctions.get_el(
                    application, 'appParticipantInfo',
                    'individualPersonRFInfo', 'nameInfo', 'middleName')
            d = f"{lastName} {firstName} {middleName}".strip()
        return d

    def get_participant_type(self, application):
        d = UtilsFunctions.get_el(application, 'appParticipant', 'participantType') or UtilsFunctions.get_el(
            application,
                                                                                                       'appParticipants',
                                                                                                       'appParticipant',
                                                                                                       'participantType')
        return d

    def get_country_full_name(self, application):
        d = UtilsFunctions.get_el(application, 'appParticipant', 'country', 'countryFullName') or UtilsFunctions.get_el(
                application,
                'appParticipants',
                'appParticipant', 'country',
                'countryFullName')
        return d

    def get_post_address(self, application):
        d = UtilsFunctions.get_el(application, 'appParticipant', 'postAddress') or UtilsFunctions.get_el(application,
                                                                                                         'appParticipants',
                                                                                                         'appParticipant',
                                                                                                         'postAddress') or UtilsFunctions.get_el(
                application,
                'appParticipantInfo',
                'individualPersonRFInfo',
                'postAddress') or UtilsFunctions.get_el(
                application,
                'appParticipantInfo',
                'legalEntityRFInfo',
                'contactInfo', 'orgFactAddress')
        return d
