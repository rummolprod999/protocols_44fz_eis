import UtilsFunctions
import parser_prot


class Participiant504:
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
                'legalEntityRFInfo',
                'INN') or UtilsFunctions.get_el(
                application,
                'appParticipantInfo',
                'individualPersonRFInfo',
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
                'fullName') or UtilsFunctions.get_el(
                application,
                'appParticipantInfo',
                'individualPersonRFInfo',
                'fullName')
        if not d:
            lastName = UtilsFunctions.get_el(application, 'appParticipant', 'contactInfo',
                                             'lastName') or UtilsFunctions.get_el(application, 'appParticipants',
                                                                            'appParticipant', 'contactInfo',
                                                                                  'lastName') or UtilsFunctions.get_el(
                    application, 'appParticipantInfo',
                    'legalEntityRFInfo', 'contactInfo', 'lastName') or UtilsFunctions.get_el(
                    application, 'appParticipantInfo',
                    'individualPersonRFInfo', 'nameInfo', 'lastName')
            firstName = UtilsFunctions.get_el(application, 'appParticipant', 'contactInfo',
                                              'firstName') or UtilsFunctions.get_el(application, 'appParticipants',
                                                                              'appParticipant', 'contactInfo',
                                                                                    'firstName') or UtilsFunctions.get_el(
                    application, 'appParticipantInfo',
                    'legalEntityRFInfo', 'contactInfo', 'firstName') or UtilsFunctions.get_el(
                    application, 'appParticipantInfo',
                    'individualPersonRFInfo', 'nameInfo', 'firstName')
            middleName = UtilsFunctions.get_el(application, 'appParticipant', 'contactInfo',
                                               'middleName') or UtilsFunctions.get_el(application, 'appParticipants',
                                                                                'appParticipant', 'contactInfo',
                                                                                      'middleName') or UtilsFunctions.get_el(
                    application, 'appParticipantInfo',
                    'legalEntityRFInfo', 'contactInfo', 'middleName') or UtilsFunctions.get_el(
                    application, 'appParticipantInfo',
                    'individualPersonRFInfo', 'nameInfo', 'middleName')
            d = f"{lastName} {firstName} {middleName}".strip()
        return d

    def get_participant_type(self, application):
        d = UtilsFunctions.get_el(application, 'appParticipant', 'participantType') or UtilsFunctions.get_el(
            application,
                                                                                                       'appParticipants',
                                                                                                       'appParticipant',
            'participantType') or UtilsFunctions.get_el(
                application,
                'appParticipantInfo',
                'legalEntityRFInfo',
                'participantType')
        return d

    def get_country_full_name(self, application):
        d = UtilsFunctions.get_el(application, 'appParticipant', 'country', 'countryFullName') or UtilsFunctions.get_el(
                application,
                'appParticipants',
                'appParticipant', 'country',
                'countryFullName') or UtilsFunctions.get_el(
                application,
                'appParticipantInfo',
                'legalEntityRFInfo', 'country',
                'countryFullName')
        return d

    def get_post_address(self, application):
        d = UtilsFunctions.get_el(application, 'appParticipant', 'postAddress') or UtilsFunctions.get_el(application,
                                                                                                   'appParticipants',
                                                                                                   'appParticipant',
                                                                                                         'postAddress') or UtilsFunctions.get_el(
                application,
                'appParticipantInfo',
                'legalEntityRFInfo',
                'contactInfo', 'orgPostAddress') or UtilsFunctions.get_el(
                application,
                'appParticipantInfo',
                'individualPersonRFInfo',
                'postAddress')
        return d
