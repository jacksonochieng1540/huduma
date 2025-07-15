from django.urls import path
from .views import (
    TicketCreateView,
    TicketListView,
    StaffDashboardView,
    TicketDetailView,
)

urlpatterns = [
    # 🗂️ Ticket listing
    path('new/', TicketListView.as_view(), name='ticket-list'),

    # ➕ Create a ticket for a specific service (pk = Service ID)
    path('new/<int:pk>/', TicketCreateView.as_view(), name='queue-ticket'),

    # 🔍 View details of a specific ticket (pk = Ticket ID)
    path('<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),

    # 👨‍💼 Staff dashboard
    path('staff/', StaffDashboardView.as_view(), name='staff-dashboard'),
]
