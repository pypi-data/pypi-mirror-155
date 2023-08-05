import logging

from django.utils.translation import gettext_lazy as _

import requests
from rest_framework import serializers

from wagtaildonate.settings import donate_settings

logger = logging.getLogger(__name__)

RECAPTCHA_VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"


def validate_recaptcha(recaptcha_token):
    try:
        response = requests.post(
            RECAPTCHA_VERIFY_URL,
            data={
                "secret": donate_settings.RECAPTCHA_PRIVATE_KEY,
                "response": recaptcha_token,
            },
        )
    except requests.exceptions.ConnectionError:
        logger.info("Error validating reCAPTCHA token")
        raise serializers.ValidationError(_("Error validating reCAPTCHA token"))
    if not response.ok:
        logger.info("Error validating reCAPTCHA token")
        raise serializers.ValidationError(_("Error validating reCAPTCHA token"))

    response_data = response.json()
    if not response_data.get("success"):
        logger.info("reCAPTCHA token not valid")
        raise serializers.ValidationError(_("reCAPTCHA token not valid"))

    minimum_score = float(donate_settings.RECAPTCHA_MINIMUM_SCORE)
    if response_data.get("score") < minimum_score:
        logger.info(
            "reCAPTCHA token not valid, score below allowed minimum: %f < %f",
            response_data.get("score"),
            minimum_score,
        )
        raise serializers.ValidationError(_("reCAPTCHA token not valid"))


class RecaptchaField(serializers.CharField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.write_only = True
        self.validators.append(validate_recaptcha)
