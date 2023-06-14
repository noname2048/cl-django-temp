from datetime import timedelta, timezone

from django.utils import timezone

from rest_framework.exceptions import APIException
from rest_framework import status

from . import dtos


def calculate_duration(start, end):
    if not end:
        end = timezone.datetime.now(tz=timezone(offset=timedelta(hours=9)))

    if start > end:
        raise APIException(
            detail="start cannot late then end",
            code=status.HTTP_400_BAD_REQUEST,
        )

    duration = end - start
    dto = dtos.DurationValidatorInput(duration=duration)
    validate_duration(dto=dto)

    return {"duration": duration}


def validate_duration(dto: dtos.DurationValidatorInput):
    if dto.duration > timedelta(hours=2):
        raise APIException(
            detail="duration cannot greater then 2 hours",
            code=status.HTTP_400_BAD_REQUEST,
        )
