from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin
)
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from payment.models import Payment
from payment.serializers import (
    PaymentSerializer,
    PaymentListSerializer,
    PaymentCreateSerializer
)
from payment.stripe import get_stripe_session


class PaymentViewSet(
    viewsets.GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin
):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return PaymentListSerializer
        elif self.action == "create":
            return PaymentCreateSerializer
        return self.serializer_class

    @action(
        detail=False,
        methods=["get"],
        url_path="success",
    )
    def success(self, request, pk=None):
        session_id = request.GET.get("session_id")

        if not session_id:
            return Response(
                {"error": "Session ID is missing!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        payment = self.queryset.filter(session_id=session_id).first()
        session = get_stripe_session(session_id)

        if isinstance(session, Response):
            return Response(session.data, status=session.status_code)

        if session.payment_status == "paid":
            payment.status = Payment.Status.PAID
            payment.save()

            return Response(
                {"message": "Payment was successful"},
                status=status.HTTP_200_OK
            )
        return Response(
            {"message": "Payment wasn't successful"},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=False,
        methods=["get"],
        url_path="cancel",
    )
    def cancel(self, request, pk=None):
        session_id = request.GET.get("session_id")

        if not session_id:
            return Response(
                {"error": "Session ID is missing!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        session = get_stripe_session(session_id)

        if isinstance(session, Response):
            return Response(session.data, status=session.status_code)

        if session.payment_status == "unpaid":
            return Response(
                {"message": (
                    "Payment canceled. Session will be "
                    "available for the next 24 hours"
                )}, status=status.HTTP_200_OK
            )
        return Response(
            {"message": "Payment wasn't canceled successful"},
            status=status.HTTP_400_BAD_REQUEST
        )

    @extend_schema(
        responses=PaymentListSerializer,
        description="Get list of all payments."
    )
    def list(self, request, *args, **kwargs):
        """Get list of payments."""
        return super().list(request, *args, **kwargs)

    @extend_schema(
        responses=PaymentSerializer,
        description="Retrieve details of a specific payment by its ID."
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a payment."""
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        request=PaymentCreateSerializer,
        responses=PaymentCreateSerializer,
        description=(
            "Create a new payment record."
            " Only authenticated users can create payments."
        )
    )
    def create(self, request, *args, **kwargs):
        """Create a new payment."""
        return super().create(request, *args, **kwargs)
