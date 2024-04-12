# Service file that contains logic
# for transactions
import pyotp
from core.models import Profile, CashToCrytpoClaims, CryptoToCashClaims
from django.contrib.auth import get_user_model
from rest_framework import serializers
from core.utility import notify_mail
from .mail_templates import ( 
    SEND_TRANSACTION_OTP,
    NOTIFY_SETTLEMENT_TEAM_OF_CRYPTO_TO_CASH,
    NOTIFY_SETTLEMENT_TEAM_OF_CASH_TO_CRYPTO,
    CUSTOMER_RECEIPT_MAIL
)
from django.core.exceptions import ValidationError
import datetime
import uuid


User = get_user_model()


def generate_unique_invoice_id():
    timestamp = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
    random_uuid = uuid.uuid4().hex[:8]
    invoice_id = f"{timestamp}-{random_uuid}"
    return invoice_id



def generate_otp_code():
    """
    Generate an OTP code

    return OTP_CODE, OTP_BASE_32 
    """
    # Create a new TOTP (Time-Based One-Time Password) instance
    otp_base_32 = pyotp.random_base32()
   
    totp = pyotp.TOTP(otp_base_32, interval=600)  # You can adjust the interval as needed

    # Generate the OTP
    otp = totp.now()

    return otp, otp_base_32


def verify_otp(otp_base_32: str, otp_code: str):
    """
    Verify the OTP code
    """
    totp = pyotp.TOTP(otp_base_32, interval=600)  # You can adjust the interval as needed
    return totp.verify(otp_code)


def send_otp_email(email:str):
    """
    
    """
    user = User.objects.filter(email=email).first()
    otp, otp_32 = generate_otp_code()

    profile = user.profile
    profile.otp_base_32 = otp_32
    profile.save()

    # send email with otp
    transaction_otp_html = ( 
            SEND_TRANSACTION_OTP.replace(
                "{{ otp_code }}", otp
            )
        )

    # Send verification mail only 
    notify_mail(
            subject="xanderfx Transaction OTP",
            to=[user.email],
            html_message=transaction_otp_html,
        )
    

def consumate_crypto_to_cash(email, dto):
    
    # validate the OTP
    user = User.objects.filter(email=email).first()
    profile = user.profile

    try:
        amount = float(dto.get("amount"))
        if amount <= 0:
            raise ValidationError("Invalid Amount: Amount must be greater than zero.")
    except ValueError:
        raise ValidationError("Invalid Amount: Amount must be a valid number.")

    
    
    if not verify_otp(profile.otp_base_32, dto.get("otp_code")):
        raise ValidationError("Invalid OTP Code, The code may have expired or was not entered correctly.")
    
    # create the CryptoToCash Claim 
    ctc_claim = CryptoToCashClaims.objects.create(
        user=user,
        region=dto.get("region"),
        address=dto.get("recipientAddress", ""),
        amount=dto.get("amount"),
        crypto_type=dto.get("cryptoType", ""),
        status="pending",
        account_number=dto.get("accountNumber", ""),
        bank_name=dto.get("bankName", ""),
        routing_number=dto.get("routingNumber", ""),
        iban=dto.get("iban", ""),
        bic_swift_code=dto.get("bic", ""),
        account_name=dto.get("accountName", ""),
        invoice_number=generate_unique_invoice_id(),
        created_by=email
    )
    
    # send a mail notifying settlement tema
    html_message = ( 
            NOTIFY_SETTLEMENT_TEAM_OF_CRYPTO_TO_CASH.replace(
                "{{ email }}", email
            ).replace("{{ transaction_date }}", str(ctc_claim.created_at))
            .replace("{{ name }}", f"{user.last_name} {user.first_name}")
            .replace("{{ amount }}", ctc_claim.amount)
            .replace("{{ crypto_type }}", ctc_claim.crypto_type)
            .replace("{{ bank_name }}", ctc_claim.bank_name)
            .replace("{{ account_name }}", ctc_claim.account_name)
            .replace("{{ account_number }}", ctc_claim.account_number)
            .replace("{{ invoice_number }}", ctc_claim.invoice_number)
            .replace("{{ swift_bic }}", ctc_claim.bic_swift_code)
            .replace("{{ iban }}", ctc_claim.iban)
            .replace("{{ routing_number }}", ctc_claim.routing_number)
        )
    
    notify_mail(
            subject="Credit: Crypto to Cash",
            to=[], # send to the settlement team
            html_message=html_message,
        )

    # send an acknowledgement mail to the customer
    html_message = ( 
            CUSTOMER_RECEIPT_MAIL .replace(
                "{{ email }}", email
            ).replace("{{ transaction_date }}", str(ctc_claim.created_at))
            .replace("{{ amount }}", ctc_claim.amount)
            .replace("{{ crypto_type }}", ctc_claim.crypto_type)
            .replace("{{ invoice_number }}", ctc_claim.invoice_number)
        )

    notify_mail(
            subject="Transaction Receipt",
            to=[user.email],
            html_message=html_message,
        )


def consumate_cash_to_crypto(email, dto):

    # validate the OTP 
    user = User.objects.filter(email=email).first()
    profile = user.profile
    
    
    if not verify_otp(profile.otp_base_32, dto.get("otp_code")):
        raise ValidationError("Invalid OTP Code, The code may have expired or was not entered correctly.")
    
    try:
        amount = float(dto.get("amount"))
        if amount <= 0:
            raise ValidationError("Invalid Amount: Amount must be greater than zero.")
    except ValueError:
        raise ValidationError("Invalid Amount: Amount must be a valid number.")

    # create the CryptoToCash Claim 
    ctc_claim = CashToCrytpoClaims.objects.create(
        user=user,
        amount=dto.get("amount"),
        crypto_type=dto.get("cryptoType", ""),
        invoice_number=generate_unique_invoice_id(),
        created_by=email,
        currency=dto.get("currency", ""),
        description=dto.get("description", ""),
        status="pending",
        account_name=dto.get("accountName", ""),
        account_number=dto.get("accountNumber", ""),
        wallet_address=dto.get("cryptoWallet", ""),
    )

    # send a mail notifying settlement tema
    html_message = ( 
            NOTIFY_SETTLEMENT_TEAM_OF_CASH_TO_CRYPTO.replace(
                "{{ email }}", email
            ).replace("{{ transaction_date }}", str(ctc_claim.created_at))
            .replace("{{ name }}", f"{user.last_name} {user.first_name}")
            .replace("{{ amount }}", ctc_claim.amount)
            .replace("{{ crypto_type }}", ctc_claim.crypto_type)
            .replace("{{ currency }}", ctc_claim.currency)
            .replace("{{ wallet_address }}", ctc_claim.wallet_address)
            .replace("{{ account_name }}", ctc_claim.account_name)
            .replace("{{ account_number }}", ctc_claim.account_number)
            .replace("{{ invoice_number }}", ctc_claim.invoice_number)
        )
    
    notify_mail(
            subject="Credit: Cash to Crypto",
            to=[], # send to the settlement team
            html_message=html_message,
        )

    # send an acknowledgement mail to the customer
    html_message = ( 
            CUSTOMER_RECEIPT_MAIL .replace(
                "{{ email }}", email
            ).replace("{{ transaction_date }}", str(ctc_claim.created_at))
            .replace("{{ amount }}", ctc_claim.amount)
            .replace("{{ crypto_type }}", ctc_claim.crypto_type)
            .replace("{{ invoice_number }}", ctc_claim.invoice_number)
        )

    # send customer receipt
    notify_mail(
            subject="Transaction Receipt",
            to=[user.email],
            html_message=html_message,
        )

