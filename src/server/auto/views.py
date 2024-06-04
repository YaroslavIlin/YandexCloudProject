from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import CreateView, ListView
from .models import Auto
from .forms import BookingForm
from django.urls import reverse_lazy
from main.models import Reservation
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin


class AutoCreateView(LoginRequiredMixin, CreateView):
    model = Auto
    template_name = "form.html"
    fields = "__all__"
    success_url = reverse_lazy('auto_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Добавить авто'
        return context


class AutoListView(LoginRequiredMixin, ListView):
    model = Auto
    context_object_name = "autos"
    paginate_by = 10
    template_name = "auto_list.html"
    def get_queryset(self):
        aaa = self.request.GET.get('auto_number')
        if aaa:
            return Auto.objects.filter(auto_number=int(auto_number)).order_by('-id')
        else:
            return Auto.objects.all().order_by('-id')

#class ReservationListView(LoginRequiredMixin, ListView):
#    model = Reservation
#    paginate_by = 10
#    context_object_name = "reservations"
#    template_name = "reservation_list.html"
#
#    def get_queryset(self):
#        # Get the auto number from the query parameters
#        auto_number = self.request.GET.get('auto_number')
#
#        # Filter reservations for the specified auto number
#        if auto_number:
#            return Reservation.objects.filter(auto__auto_number=int(auto_number)).order_by('-id'
#        else:
#            return Reservation.objects.all().order_by('-id')                                    


class AutoDetailView(LoginRequiredMixin, View):

    def get(self, request, pk):
        auto = get_object_or_404(Auto, pk=pk)
        current_datetime = timezone.now()
        reservations = auto.reservation_set.filter(rent_start_date__gte=current_datetime.date()).order_by('rent_start_date')
        return render(request, 'auto_detail.html', {'auto': auto, 'reservations': reservations, })


