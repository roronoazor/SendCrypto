from django.db import models
from django.contrib.auth.models import User
import uuid


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    name = models.CharField(max_length=2000)
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    currency = models.CharField(max_length=3)
    annual_income = models.CharField(max_length=100)
    referral = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.name} profile"


class Transaction(models.Model):
    STATUS_CHOICES = (
        ("failed", "Failed"),
        ("pending", "Pending"),
        ("success", "Success"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    source = models.CharField(max_length=255, null=True)
    currency = models.CharField(max_length=100, null=True)
    invoice_id = models.CharField(max_length=255, null=True)
    amount = models.CharField(max_length=1000, null=True)
    payload = models.JSONField(default=dict, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000, null=True)
    description = models.CharField(max_length=1000, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Transaction Id: {self.invoice_id}"
