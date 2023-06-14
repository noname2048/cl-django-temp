from datetime import datetime, timedelta, timezone

from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from unittest import mock

KST = timezone(offset=timedelta(hours=9))


class SimpleAPITests(APITestCase):
    def test_simple_api_success(self):
        # 일반적인 request 에 적절하게 response로 대응하는지 테스트합니다.
        with mock.patch("simple.services.timezone") as mock_timezone:
            mock_timezone.datetime.now.return_value = datetime.strptime(
                "2023-06-01T12:00:00+09:00",
                "%Y-%m-%dT%H:%M:%S%z",
            )

            path = reverse("simple")
            res = self.client.post(
                path=path,
                format="json",
                data={
                    "start": datetime.strptime(
                        "2023-06-01T11:00:00+09:00",
                        "%Y-%m-%dT%H:%M:%S%z",
                    ),
                },
            )

        self.assertEquals(res.status_code, status.HTTP_200_OK, res.content)

    @mock.patch("simple.services.timezone")
    def test_simpel_api_fail(self, timezone_mock):
        timezone_mock.datetime.now.return_value = datetime.strptime(
            "2023-06-01T12:00:00+09:00",
            "%Y-%m-%dT%H:%M:%S%z",
        )

        # 비정상적인 request 에 대해 exception 이 작동하는지 테스트합니다.
        path = reverse("simple")

        # start > end
        res = self.client.post(
            path=path,
            format="json",
            data={
                "start": datetime.strptime(
                    "2023-06-01T13:00:00+09:00",
                    "%Y-%m-%dT%H:%M:%S%z",
                ),
            },
        )
        self.assertNotEquals(res.status_code, status.HTTP_200_OK)

        # hours < 2
        res = self.client.post(
            path=path,
            format="json",
            data={
                "start": datetime.strptime(
                    "2023-06-01T09:00:00+09:00",
                    "%Y-%m-%dT%H:%M:%S%z",
                ),
            },
        )
        self.assertNotEquals(res.status_code, status.HTTP_200_OK)

        # no start params (assertWithRaise cannot detect validation error)
        res = self.client.post(
            path=path,
            format="json",
            data={},
        )
        self.assertNotEquals(res.status_code, status.HTTP_200_OK)
