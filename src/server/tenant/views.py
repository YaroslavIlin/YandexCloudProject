from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Tenant
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class TenantCreateView(LoginRequiredMixin, CreateView):
    model = Tenant
    template_name = "form.html"
    fields = "__all__"
    success_url = reverse_lazy('tenant_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавить арендатора"
        return context


class TenantListView(LoginRequiredMixin, ListView):
    model = Tenant
    context_object_name = "tenants"
    paginate_by = 10
    template_name = "tenant_list.html"

    def get_queryset(self):
        return Tenant.objects.all().order_by('-id')


class TenantDetailView(LoginRequiredMixin, DetailView):
    model = Tenant
    template_name = "tenant_detail.html"
    context_object_name = "tenant"
