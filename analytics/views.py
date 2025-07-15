from django.shortcuts import render
from django.db.models import Count
from queue1.models import Ticket
from django.http import HttpResponse
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.models import User
from datetime import datetime
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import openpyxl
from io import BytesIO


def dashboard(request):
    # Get filters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if not start_date or not end_date:
        end_date = timezone.now().date()
        start_date = end_date - timezone.timedelta(days=7)
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    tickets = Ticket.objects.filter(created_at__date__range=(start_date, end_date))

    status_data = tickets.values('status').annotate(count=Count('id'))
    status_labels = [item['status'] for item in status_data]
    status_counts = [item['count'] for item in status_data]

    service_data = tickets.values('service__name').annotate(count=Count('id'))
    service_labels = [item['service__name'] for item in service_data]
    service_counts = [item['count'] for item in service_data]

    context = {
        'status_labels': status_labels,
        'status_counts': status_counts,
        'service_labels': service_labels,
        'service_counts': service_counts,
        'recent_tickets_count': tickets.count(),
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'analytics/dashboard.html', context)


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="analytics_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Service', 'Status', 'Created At'])

    tickets = Ticket.objects.all()
    for t in tickets:
        writer.writerow([t.service.name, t.status, t.created_at])
    return response


def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="analytics_report.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, height - 50, "Huduma Analytics Report")

    p.setFont("Helvetica", 10)
    y = height - 100
    tickets = Ticket.objects.all()

    for ticket in tickets:
        p.drawString(40, y, f"{ticket.service.name} | {ticket.status} | {ticket.created_at.strftime('%Y-%m-%d %H:%M')}")
        y -= 15
        if y < 50:
            p.showPage()
            y = height - 50

    p.save()
    return response


def export_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Analytics Data"

    ws.append(['Service', 'Status', 'Created At'])

    tickets = Ticket.objects.all()
    for t in tickets:
        ws.append([t.service.name, t.status, t.created_at.strftime('%Y-%m-%d %H:%M')])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="analytics_report.xlsx"'

    wb.save(response)
    return response


# Weekly email summary (call via cron/scheduler)
def send_weekly_report():
    last_week = timezone.now().date() - timezone.timedelta(days=7)
    tickets = Ticket.objects.filter(created_at__date__gte=last_week)
    count = tickets.count()
    top_services = tickets.values('service__name').annotate(c=Count('id')).order_by('-c')[:5]

    body = f"🗓 Weekly Analytics Report\n\nTotal Tickets: {count}\nTop Services:\n"
    for s in top_services:
        body += f"- {s['service__name']}: {s['c']}\n"

    # Get staff emails (you may customize this)
    staff_emails = User.objects.filter(is_staff=True).values_list('email', flat=True)

    send_mail(
        subject="📊 Huduma Weekly Report",
        message=body,
        from_email="huduma@example.com",
        recipient_list=staff_emails,
        fail_silently=False
    )
