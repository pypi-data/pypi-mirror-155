"""
Basic Mapping of persidio entities and fides default taxonomy

TODO: convert this to yaml file so customized mappings can be appended

"""

ENTITIES = {
    "CREDIT_CARD": [
        "account.payment.financial_account_number",
        "user.provided.identifiable.financial.account_number",
    ],
    "CRYPTO": [
        "account.payment.financial_account_number",
        "user.provided.identifiable.financial.account_number",
    ],
    "DATE_TIME": ["user.provided.identifiable.date_of_birth"],
    "EMAIL_ADDRESS": [
        "account.contact.email",
        "user.provided.identifiable.contact.email",
    ],
    "IBAN_CODE": [
        "account.payment.financial_account_number",
        "user.provided.identifiable.financial.account_number",
    ],
    "IP_ADDRESS": ["user.derived.identifiable.device.ip_address"],
    "NRP": [
        "user.provided.identifiable.political_opinion",
        "user.provided.identifiable.religious_belief",
        "user.derived.identifiable.race",
    ],
    "LOCATION": [
        "account.contact.street",
        "account.contact.city",
        "account.contact.state",
        "account.contact.country",
        "account.contact.postal_code",
        "user.provided.identifiable.contact.street",
        "user.provided.identifiable.contact.city",
        "user.provided.identifiable.contact.state",
        "user.provided.identifiable.contact.country",
        "user.provided.identifiable.contact.postal_code"
        "user.derived.identifiable.location",
    ],
    "PERSON": ["user.provided.identifiable.name"],
    "PHONE_NUMBER": [
        "account.contact.phone_number",
        "user.provided.identifiable.contact.phone_number",
    ],
    "MEDICAL_LICENSE": [
        "user.provided.identifiable.health_and_medical",
        "user.provided.identifiable.government_id",
    ],
    "US_BANK_NUMBER": [
        "account.payment.financial_account_number",
        "user.provided.identifiable.financial.account_number",
    ],
    "US_DRIVER_LICENSE": [
        "user.provided.identifiable.government_id.drivers_license_number"
    ],
    "US_ITIN": [
        "user.provided.identifiable.government_id.national_identification_number"
    ],
    "US_PASSPORT": ["user.provided.identifiable.government_id.passport_number"],
    "US_SSN": [
        "user.provided.identifiable.government_id.national_identification_number"
    ],
    "UK_NHS": [
        "user.provided.identifiable.government_id.national_identification_number",
        "user.provided.identifiable.health_and_medical",
    ],
    "AU_ABN": [
        "user.provided.identifiable.government_id.national_identification_number"
    ],
    "AU_ACN": [
        "user.provided.identifiable.government_id.national_identification_number"
    ],
    "AU_TFN": [
        "user.provided.identifiable.government_id.national_identification_number"
    ],
    "AU_MEDICARE": [
        "user.provided.identifiable.government_id.national_identification_number",
        "user.provided.identifiable.health_and_medical",
    ],
}
