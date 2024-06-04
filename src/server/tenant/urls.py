from django.urls import path
from .views import TenantListView, TenantDetailView, TenantCreateView

urlpatterns = [
    path('tenant/create/', TenantCreateView.as_view(), name="tenant_create"),
    path('tenant/', TenantListView.as_view(), name='tenant_list'),
    path('tenant/<int:pk>/', TenantDetailView.as_view(), name='tenant_detail'),
    # Add other URLs as needed
]
