from django.utils.translation import gettext as _

import braintree
from braintree import ErrorCodes

from wagtaildonate.models.utils import get_single_donation_model


def filter_user_card_errors(result):
    client_errors = {
        ErrorCodes.CreditCard.CreditCardTypeIsNotAccepted: _(
            "The type of card you used is not accepted."
        ),
        ErrorCodes.Transaction.PaymentMethodNonceCardTypeIsNotAccepted: _(
            "The type of card you used is not accepted."
        ),
        ErrorCodes.CreditCard.CvvIsInvalid: _("The CVV code you entered was invalid."),
        ErrorCodes.CreditCard.CvvIsRequired: _("The CVV code is required."),
        ErrorCodes.CreditCard.CvvVerificationFailed: _(
            "The CVV code you entered was invalid."
        ),
        ErrorCodes.CreditCard.ExpirationDateIsRequired: _(
            "Expiration date is required"
        ),
        ErrorCodes.CreditCard.ExpirationDateIsInvalid: _(
            "The expiration date you entered was invalid."
        ),
        ErrorCodes.CreditCard.NumberIsInvalid: _(
            "The credit card number you entered was invalid."
        ),
        ErrorCodes.ApplePay.ApplePayCardsAreNotAccepted: _(
            "Apple Pay cards are not accepted."
        ),
        ErrorCodes.ApplePay.PaymentMethodNonceCardTypeIsNotAccepted: _(
            "The type of card you used is not accepted."
        ),
    }
    error_messages = [
        client_errors[error.code]
        for error in result.errors.deep_errors
        if error.code in client_errors.keys()
    ]
    return error_messages


def filter_postal_code_errors(result):
    client_errors = {
        ErrorCodes.Address.PostalCodeInvalidCharacters: _(
            "The postal code you provided contains invalid characters."
        ),
        ErrorCodes.Address.PostalCodeIsTooLong: _(
            "The postal code you provided is too long."
        ),
        ErrorCodes.Address.PostalCodeIsInvalid: _(
            "The postal code you provided is not valid."
        ),
        ErrorCodes.CreditCard.PostalCodeVerificationFailed: _(
            "The postal code provided does not match the card's."
        ),
    }
    return list(
        frozenset(
            [
                client_errors[error.code]
                for error in result.errors.deep_errors
                if error.code in client_errors
            ]
        )
    )


def filter_street_address_errors(result):
    client_errors = {
        ErrorCodes.Address.StreetAddressIsInvalid: _(
            "The street address you provided is invalid."
        ),
        ErrorCodes.Address.StreetAddressIsTooLong: _(
            "The street address you provided is too long."
        ),
    }
    return list(
        frozenset(
            [
                client_errors[error.code]
                for error in result.errors.deep_errors
                if error.code in client_errors
            ]
        )
    )


def filter_country_errors(result):
    client_errors = {
        ErrorCodes.Address.CountryCodeAlpha2IsNotAccepted: _(
            "Country provided is not supported."
        ),
        ErrorCodes.Address.CountryCodeAlpha3IsNotAccepted: _(
            "Country provided is not supported."
        ),
        ErrorCodes.Address.CountryCodeNumericIsNotAccepted: _(
            "Country provided is not supported."
        ),
        ErrorCodes.Address.CountryNameIsNotAccepted: _(
            "Country provided is not supported."
        ),
    }
    return list(
        frozenset(
            [
                client_errors[error.code]
                for error in result.errors.deep_errors
                if error.code in client_errors
            ]
        )
    )


Status = braintree.Transaction.Status


def map_status(braintree_status):
    """
    Maps the given braintree status into one of the values in get_single_donation_model().STATUS_CHOICES.
    """
    if braintree_status == Status.Settled:
        return get_single_donation_model().STATUS_SETTLED

    elif braintree_status in {
        Status.Settling,
        Status.SubmittedForSettlement,
        Status.SettlementPending,
    }:
        return get_single_donation_model().STATUS_SETTLING

    elif braintree_status in {
        Status.Failed,
        Status.ProcessorDeclined,
        Status.GatewayRejected,
        Status.Voided,
        Status.SettlementDeclined,
    }:
        return get_single_donation_model().STATUS_FAILED

    else:
        return get_single_donation_model().STATUS_UNKNOWN
