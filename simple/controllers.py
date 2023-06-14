from rest_framework.generics import GenericAPIView
from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiExample

from . import services


class SimpleAPI(GenericAPIView):
    # request, response 의 json data 를 필터링 합니다.
    class DurationRequestSerializer(serializers.Serializer):
        start = serializers.DateTimeField(allow_null=False)
        end = serializers.DateTimeField(required=False)

    class DurationResponseSerializer(serializers.Serializer):
        duration = serializers.DurationField()

    serializer_class = DurationRequestSerializer

    @extend_schema(
        tags=["simple"],
        request=DurationRequestSerializer,
        responses={200: DurationResponseSerializer},
        examples=[
            OpenApiExample(
                name="Example 01",
                value={
                    "start": "2023-06-01T00:00:00+0900",
                    "end": "2023-06-01T06:00:00+0900",
                },
            )
        ],
    )
    def post(self, request: Request, *args, **kwargs):
        serializer = self.DurationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response_data = services.calculate_duration(
            start=serializer.validated_data["start"],
            end=serializer.validated_data.get("end", None),
        )
        response_serializer = self.DurationResponseSerializer(response_data)

        return Response(response_serializer.data, status=status.HTTP_200_OK)
