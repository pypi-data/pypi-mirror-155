from uuid import uuid4

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from leapchain.constants.network import (
    ACCEPTED_FEE_CHOICES,
    MAX_POINT_VALUE,
    MEMO_MAX_LENGTH,
    MIN_POINT_VALUE,
    VERIFY_KEY_LENGTH
)


class NetworkTransaction(models.Model):
    id = models.UUIDField(default=uuid4, editable=False, primary_key=True)  # noqa: A003
    amount = models.PositiveBigIntegerField(
        validators=[
            MaxValueValidator(MAX_POINT_VALUE),
            MinValueValidator(MIN_POINT_VALUE),
        ]
    )
    fee = models.CharField(blank=True, choices=ACCEPTED_FEE_CHOICES, max_length=17)
    memo = models.CharField(blank=True, max_length=MEMO_MAX_LENGTH)
    recipient = models.CharField(max_length=VERIFY_KEY_LENGTH)

    class Meta:
        abstract = True
