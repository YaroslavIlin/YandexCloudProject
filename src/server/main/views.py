from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView
from django.urls import reverse_lazy
from .models import Reservation
from django.views.generic import DetailView
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from auto.models import Auto
from tenant.models import Tenant


class CustomReservationForm(forms.ModelForm):
    
    class Meta:
        model = Reservation
        fields = '__all__'
        widgets = {
            'rent_start_date': forms.DateInput(attrs={'type': 'date'}),
            'rent_end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class DashboardView(View):
    
    def get(self, request):
        total_auto = Auto.objects.all().count()
        total_tenant = Tenant.objects.all().count()
        total_reservation = Reservation.objects.all().count()
        context = {
            'total_auto': total_auto,
            'total_tenant': total_tenant,
            'total_reservation': total_reservation,
        }
        return render(request, 'dashboard.html', context)


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    template_name = "form.html"
    form_class = CustomReservationForm

    def get_initial(self):
        initial = super().get_initial()
        tenant_id = self.request.GET.get('tenant_id')
        if tenant_id:
            initial['tenant'] = tenant_id
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавить бронирование"
        return context

    def form_valid(self, form):
        auto = form.cleaned_data['auto']
        rent_start_date = form.cleaned_data['rent_start_date']
        rent_end_date = form.cleaned_data['rent_end_date']
        existing_reservations = Reservation.objects.filter(
            auto=auto,
            rent_start_date__lt=rent_end_date,
            rent_end_date__gt=rent_start_date
        )

        if existing_reservations.exists():
            form.add_error('auto', 'Это авто уже арендовано на выбранные даты')
            return self.form_invalid(form)
        else:
            return super().form_valid(form)


class ReservationUpdateView(LoginRequiredMixin, UpdateView):
    model = Reservation
    template_name = "form.html"
    form_class = CustomReservationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Обновить аренду"
        return context

    def form_valid(self, form):
        auto = form.cleaned_data['auto']
        rent_start_date = form.cleaned_data['rent_start_date']
        rent_end_date = form.cleaned_data['rent_end_date']
        existing_reservations = Reservation.objects.filter(
            auto=auto,
            rent_start_date__lt=rent_end_date,
            rent_end_date__gt=rent_start_date
        )

        if existing_reservations.exists():
            form.add_error('auto', 'Это авто уже арендовано на выбранные даты')
            return self.form_invalid(form)
        else:
            return super().form_valid(form)    


class ReservationDetailView(LoginRequiredMixin, DetailView):
    model = Reservation
    template_name = "reservation_detail.html"


class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    paginate_by = 10
    context_object_name = "reservations"
    template_name = "reservation_list.html"

    def get_queryset(self):
        # Get the auto number from the query parameters
        auto_number = self.request.GET.get('auto_number')

        # Filter reservations for the specified auto number
        if auto_number:
            return Reservation.objects.filter(auto__auto_number=int(auto_number)).order_by('-id')
        else:
            return Reservation.objects.all().order_by('-id')
