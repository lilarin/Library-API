from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from borrowing.models import Borrowing
from .serializers import BorrowingSerializer


class BorrowingCreateView(generics.CreateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
