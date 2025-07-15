from django.db import models
from core.models import User
from services.models import Service
from django.utils import timezone
from django.core.validators import FileExtensionValidator

class Ticket(models.Model):
    PENDING = 'P'
    PROCESSING = 'G'
    COMPLETED = 'C'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (COMPLETED, 'Completed')
    ]

    HIGH = 'H'
    NORMAL = 'N'
    PRIORITY_CHOICES = [
        (HIGH, 'High'),
        (NORMAL, 'Normal')
    ]

    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default=NORMAL)
    ticket_number = models.CharField(max_length=10, unique=True)

    # ✅ Add these two fields:
    processing_start = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.ticket_number:
            last_ticket = Ticket.objects.order_by('-id').first()
            new_num = (last_ticket.id + 1) if last_ticket else 1
            self.ticket_number = f"T{new_num:05d}"
        super().save(*args, **kwargs)

    @property
    def wait_time(self):
        return (timezone.now() - self.created_at).seconds // 60

    @property
    def progress(self):
        if self.status == self.PROCESSING:
            return 50
        elif self.status == self.COMPLETED:
            return 100
        return 0



def document_upload_path(instance, filename):
    return f'documents/ticket_{instance.ticket.ticket_number}/{filename}'

class TicketDocument(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='documents')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to=document_upload_path,
        validators=[FileExtensionValidator(['pdf', 'png', 'jpg', 'jpeg', 'docx'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
