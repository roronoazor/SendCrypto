from django.db import models
from django.contrib.auth.models import User
import uuid


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    name = models.CharField(max_length=2000)
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    passport_number = models.CharField(max_length=30, null=True, blank=True)
    currency = models.CharField(max_length=3)
    annual_income = models.CharField(max_length=100)
    referral = models.CharField(max_length=100)
    status = models.CharField(max_length=1000, null=True, blank=True)
    otp_base_32 = models.CharField(null=True, blank=True, max_length=1000)


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


class BTCWallet(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wallet_address = models.CharField(max_length=1000)
    crypto_name = models.CharField(max_length=1000)
    crypto_short_name = models.CharField(max_length=1000, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=1000, null=True)


class BankAccount(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bank_name = models.CharField(max_length=1000)
    currency = models.CharField(max_length=1000)
    bank_account_name = models.CharField(max_length=1000, null=True, blank=True)
    bank_account_number = models.CharField(max_length=1000, null=True, blank=True)
    swift_code = models.CharField(max_length=1000, null=True, blank=True)
    bic_code = models.CharField(max_length=1000, null=True, blank=True)
    iban = models.CharField(max_length=1000, null=True, blank=True)
    routing_number = models.CharField(max_length=1000, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=1000, null=True)


class CryptoToCashClaims(models.Model):

    STATUS_CHOICES = (
        ('confirmed', 'Confirmed'),
        ('settled', 'Settled'),
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
        ('review', 'Reviewing')
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, null=True, related_name="crypto_to_cash_claims", on_delete=models.CASCADE)
    region = models.CharField(max_length=1000, null=True, blank=True)
    address = models.CharField(max_length=1000, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    crypto_type = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, null=True, blank=True)
    account_number = models.CharField(max_length=1000, null=True, blank=True)
    bank_name = models.CharField(max_length=1000, null=True, blank=True)
    routing_number = models.CharField(max_length=1000, null=True, blank=True)
    iban = models.CharField(max_length=1000, null=True, blank=True)
    bic_swift_code = models.CharField(max_length=1000, null=True, blank=True)
    account_name = models.CharField(max_length=1000, null=True, blank=True)
    invoice_number = models.CharField(null=True, blank=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=1000, null=True)



class CashToCrytpoClaims(models.Model):

    STATUS_CHOICES = (
        ('confirmed', 'Confirmed'),
        ('settled', 'Settled'),
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
        ('review', 'Reviewing')
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, null=True, related_name="cash_to_crypto_claims", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=100,  null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, null=True, blank=True)
    wallet_address = models.CharField(max_length=100, null=True, blank=True)
    crypto_type = models.CharField(max_length=100, null=True, blank=True)
    invoice_number = models.CharField(null=True, blank=True, max_length=100)
    account_number = models.CharField(null=True, blank=True, max_length=100) 
    account_name = models.CharField(null=True, blank=True, max_length=100) 
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=1000, null=True)

    