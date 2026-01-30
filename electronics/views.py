from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import NetworkNode
from .serializers import NetworkNodeSerializer


class IsActiveEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_active


class NetworkNodeViewSet(viewsets.ModelViewSet):
    queryset = NetworkNode.objects.all().select_related('supplier').prefetch_related('products')
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveEmployee]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['country']
    search_fields = ['name', 'email', 'city']
    ordering_fields = ['name', 'created_at', 'debt']
    ordering = ['-created_at']

    def perform_update(self, serializer):
        serializer.save(debt=self.get_object().debt)
