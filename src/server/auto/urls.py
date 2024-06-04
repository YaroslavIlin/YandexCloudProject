from django.urls import path
from .views import AutoListView, AutoDetailView, AutoCreateView

urlpatterns = [
    path('auto/create/', AutoCreateView.as_view(), name="auto_create"),
    path('auto/', AutoListView.as_view(), name='auto_list'),
    path('auto/<int:pk>/', AutoDetailView.as_view(), name='auto_detail'),
]
