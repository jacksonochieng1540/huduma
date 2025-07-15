from django.views.generic import ListView, DetailView, CreateView,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Ticket
from services.models import Service
from core.mixins import StaffRequiredMixin
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from core.models import User
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib import messages
from django.db import models


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    fields = []
    template_name = 'queue1/create_ticket.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.service = Service.objects.get(pk=self.kwargs['pk'])
        form.instance.priority = self.request.POST.get('priority')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('ticket-detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service'] = Service.objects.get(pk=self.kwargs['pk'])
        return context


class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'queue1/ticket_list.html'
    
    def get_queryset(self):
        if self.request.user.role == User.STAFF:
            return Ticket.objects.all().order_by('-created_at')
        return Ticket.objects.filter(user=self.request.user).order_by('-created_at')

class StaffDashboardView(StaffRequiredMixin, TemplateView):
    template_name = 'queue1/staff_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🟡 Handle ticket filters
        priority = self.request.GET.get('priority')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        # 🎯 Default to last 7 days if not provided
        today = timezone.now().date()
        if not start_date or not end_date:
            end_date = today
            start_date = end_date - timezone.timedelta(days=7)
        else:
            start_date = timezone.datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = timezone.datetime.strptime(end_date, "%Y-%m-%d").date()

        # 🟢 Ticket filters by priority and status
        pending_qs = Ticket.objects.filter(status=Ticket.PENDING)
        if priority in ['H', 'N']:
            pending_qs = pending_qs.filter(priority=priority)

        context['pending_tickets'] = pending_qs.order_by('created_at')
        context['processing_tickets'] = Ticket.objects.filter(status=Ticket.PROCESSING).order_by('processing_start')
        context['current_time'] = timezone.now()

        # 🟣 ANALYTICS SECTION
        analytics_qs = Ticket.objects.filter(created_at__date__range=(start_date, end_date))

        # Status Pie Chart
        status_data = analytics_qs.values('status').annotate(count=models.Count('id'))
        context['status_labels'] = [item['status'] for item in status_data]
        context['status_counts'] = [item['count'] for item in status_data]

        # Service Bar Chart
        service_data = analytics_qs.values('service__name').annotate(count=models.Count('id'))
        context['service_labels'] = [item['service__name'] for item in service_data]
        context['service_counts'] = [item['count'] for item in service_data]

        # Other analytics
        context['recent_tickets_count'] = analytics_qs.count()
        context['start_date'] = start_date
        context['end_date'] = end_date

        return context

    def post(self, request, *args, **kwargs):
        ticket_id = request.POST.get('ticket_id')
        action = request.POST.get('action')

        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            messages.error(request, "Ticket not found.")
            return redirect('staff-dashboard')

        if action == 'process' and ticket.status == Ticket.PENDING:
            ticket.status = Ticket.PROCESSING
            ticket.processing_start = timezone.now()
        elif action == 'complete' and ticket.status == Ticket.PROCESSING:
            ticket.status = Ticket.COMPLETED
            ticket.completed_at = timezone.now()

        ticket.save()
        return redirect('staff-dashboard')


def generate_pdf_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    template = get_template('queue1/ticket_pdf.html')
    context = {'ticket': ticket}
    html = template.render(context)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{ticket.ticket_number}.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('PDF generation error')
    return response

class TicketDetailView(DetailView):
    model = Ticket
    template_name = 'queue1/ticket_detail.html'
    context_object_name = 'ticket'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        action = request.POST.get('action')

        if action == 'process' and self.object.status == 'P':
            self.object.status = 'G'
            self.object.processing_start = timezone.now()
            self.object.save()

        elif action == 'complete' and self.object.status == 'G':
            self.object.status = 'C'
            self.object.completed_at = timezone.now()
            self.object.save()

        elif action == 'cancel' and request.user == self.object.user:
            self.object.delete()  
            return redirect('ticket-list')  

        return redirect('ticket-detail', pk=self.object.pk)