from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from core.models import *
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from core.country import countries
from core.plans import DEPOSIT_PLANS
from core.helpers import generate_invoice_number
#from coinbase_commerce import Client
from coinsend import settings

import logging

#from coinbase_commerce.error import SignatureVerificationError, WebhookInvalidPayload
#from coinbase_commerce.webhook import Webhook
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


def index(request):
    return render(request, "index.html")


def investment_plan(request):
    return render(request, "investment-plans.html")


def affiliate_marketing(request):
    return render(request, "affiliate-marketing.html")


def news(request):
    return render(request, "news.html")


def contact(request):
    return render(request, "contact.html")


def thesis(request):
    return render(request, "thesis.html")


def portfolio(request):
    return render(request, "portfolio.html")


def about(request):
    return render(request, "about.html")


def nfp(request):
    return render(request, "nfp.html")


def escrow(request):
    return render(request, "escrow.html")


def forex(request):
    return render(request, "forex.html")


def ieo(request):
    return render(request, "ieo.html")


def erc(request):
    return render(request, "erc-20-portfolio.html")


def user_login(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        # Read data from request.POST
        email = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticate the user
        user = User.objects.filter(email=email).first()
        if not user:
            messages.error(request, "Invalid email or password. Please try again.")
            return redirect("user_login")  #

        if user and not user.check_password(password):
            messages.error(request, "Invalid email or password. Please try again.")
            return redirect("user_login")  #

        if user is not None:
            # Login the user
            login(request, user)
            return redirect(
                "dashboard"
            )  # Replace 'dashboard' with your actual dashboard URL
        else:
            messages.error(request, "Invalid email or password. Please try again.")
            return redirect("user_login")  #


@transaction.atomic
def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    elif request.method == "POST":
        # Read data from request.POST
        name = request.POST.get("name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        country = request.POST.get("country")
        currency = request.POST.get("currency")
        annual_income = request.POST.get("annual_income")
        referral = request.POST.get("referral")
        password = request.POST.get("password")
        password_confirmation = request.POST.get("password_confirmation")

        if password != password_confirmation:
            messages.error(request, "The password confirmation does not match.")
            return redirect("register")

        with transaction.atomic():
            if User.objects.filter(username=username).count():
                messages.error(request, "This username has been taken.")
                return redirect("register")

            if User.objects.filter(email=email).count():
                messages.error(request, "This email has been taken.")
                return redirect("register")

            if Profile.objects.filter(phone=phone).count():
                messages.error(request, "This phone has been taken.")
                return redirect("register")

            # Create the user and profile
            user = User.objects.create(
                first_name=name, last_name="", email=email, username=username
            )

            user.set_password(password)
            user.save()

            profile = Profile.objects.create(
                user=user,
                name=name,
                phone=phone,
                country=country,
                currency=currency,
                annual_income=annual_income,
                referral=referral,
            )

            # Authenticate the user after successful registration
            authenticated_user = authenticate(
                request, username=username, password=password
            )

            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect("dashboard")

            messages.error(request, "Registration failed. Please try again.")
            return redirect("register")


@login_required
def dashboard(request):
    user_deposit_balance = 0
    user_balance = 0
    user_withdrawal_balance = 0

    balance = user_balance.balance if user_balance else "0"
    withdrawals = user_withdrawal_balance.balance if user_withdrawal_balance else "0"
    deposits = user_deposit_balance.balance if user_deposit_balance else "0"
    referrals = Profile.objects.filter(referral=request.user.username).count()

    context = {
        "balance": balance.replace(",", ""),
        "deposits": deposits.replace(",", ""),
        "withdrawals": withdrawals.replace(",", ""),
        "referrals": referrals,
    }
    return render(request, "dashboard.html", context)


@transaction.atomic
@login_required
def profile(request):
    if request.method == "GET":
        page_url = request.build_absolute_uri("/")
        referral_link = f"{page_url}register?ref={request.user.username}"
        referral_code = request.user.username
        name = request.user.first_name
        email = request.user.email
        username = request.user.username
        phone = request.user.profile.phone
        country = request.user.profile.country

        context = {
            "referral_link": referral_link,
            "referral_code": referral_code,
            "name": name,
            "email": email,
            "username": username,
            "phone": phone,
            "country": country,
            "countries": countries,
        }

        return render(request, "profile.html", context)
    elif request.method == "POST":
        name = request.POST.get("name")
        country = request.POST.get("country")
        phone = request.POST.get("phone")

        profile = request.user.profile

        with transaction.atomic():
            request.user.first_name = name
            profile.country = country
            profile.phone = phone

            request.user.save()
            profile.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")


@login_required
def affiliates(request):
    referrals = Profile.objects.filter(referral=request.user.username).select_related(
        "user"
    )
    referrer = ""

    if request.user.profile.referral:
        referrer = User.objects.filter(
            username__exact=request.user.profile.referral
        ).first()
        referrer = referrer.first_name if referrer else ""

    context = {"referrals": referrals, "referrer": referrer}

    return render(request, "referrals.html", context)


@login_required
def deposits(request):
    if request.method == "GET":
        user_balance = 0
        user_deposit_balance = 0

        active_deposits = 0
        ended_deposits = 0

        balance = user_balance.balance if user_balance else "0"
        deposits = user_deposit_balance.balance if user_deposit_balance else "0"

        context = {
            "balance": balance.replace(",", ""),
            "deposits": deposits.replace(",", ""),
            "active_deposits": active_deposits,
            "ended_deposits": ended_deposits,
        }

        return render(request, "deposits.html", context)
    elif request.method == "POST":
        amount = request.POST.get("amount")
        name = request.POST.get("name")
        description = request.POST.get("description")

        if amount < 0:
            messages.error(request, f"Amount must be greater than 0.")
            return redirect("deposits")

        # Create a deposit record in your database
        txn = Transaction.objects.create(
            source="crypto",
            invoice_id=generate_invoice_number(),
            amount=amount,
            name=name,
            description=description,
        )

        # Initialize the Coinbase Commerce client
        coinbase_client = Client(api_key=settings.COINBASE_COMMERCE_API_KEY)

        # Create a Coinbase Commerce charge
        charge = coinbase_client.charge.create(
            name="Initializing a deposit",
            description=f"Coin Send - Transfer",
            local_price={
                "amount": amount,
                "currency": "USD",
            },  # Use your desired currency
            pricing_type="fixed_price",
            metadata={
                "txn_id": txn.id,
                "user_id": request.user.id if request.user else None,
                "name": name,
                "description": description,
            },  # Store the deposit ID for reference
        )

        # Redirect the user to the Coinbase Commerce payment page
        payment_url = charge.hosted_url

        return redirect(payment_url)


@login_required
def earnings(request):
    balance = 0

    approved_withdrawals = 0

    active_deposits = 0

    deposits = 0

    context = {
        "balance": balance,
        "total_deposits": deposits,
        "active_deposits": active_deposits,
        "total_withdrawals": approved_withdrawals,
        "earnings": earnings,
    }
    return render(request, "earnings.html", context)


@login_required
def investments(request):
    if request.method == "GET":
        active_deposits = 0
        ended_deposits = 0

        balance = 0
        deposits = 0

        user_deposits = 0

        context = {
            "balance": balance.replace(",", ""),
            "deposits": deposits.replace(",", ""),
            "active_deposits": active_deposits,
            "ended_deposits": ended_deposits,
            "user_deposits": user_deposits,
        }
        return render(request, "investments.html", context)
    return render(request, "investments.html")


@login_required
def withdrawals(request):
    if request.method == "GET":
        balance = 0
        withdrawals = 0

        pending_withdrawals = 0
        approved_withdrawals = 0

        context = {
            "withdrawals": withdrawals,
            "total_withdrawals": approved_withdrawals,
            "pending_withdrawals": pending_withdrawals,
            "approved_withdrawals": approved_withdrawals,
            "balance": balance,
        }

        return render(request, "withdrawals.html", context)
    elif request.method == "POST":
        amount = request.POST.get("amount")
        source = request.POST.get("source")
        description = request.POST.get("description")

        return redirect("withdrawals")


@login_required
def compounding(request):
    compounding = "0"
    deposits = "0"
    earnings = "0"
    withdrawals = "0"

    context = {
        "compounding": compounding.replace(",", ""),
        "deposits": deposits.replace(",", ""),
        "withdrawals": withdrawals.replace(",", ""),
        "earnings": earnings.replace(",", ""),
    }

    return render(request, "compounding.html", context)


@login_required
def user_logout(request):
    logout(request)
    return redirect("user_login")


def change_password(request):
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        password = request.POST.get("password")
        password_confirmation = request.POST.get("password_confirmation")

        if password != password_confirmation:
            messages.error(request, "Password confirmation does not match.")
            return redirect("profile")

        if not request.user.check_password(old_password):
            messages.error(request, "Incorrect Password Provided.")
            return redirect("profile")

        request.user.set_password(password)
        request.user.save()

        messages.success(request, "Password Updated Successfully.")

        return redirect("profile")


def investment_detail(request, id):
    context = {"user_deposit": {}, "amount_to_receive": 0}
    return render(request, "investment_detail.html", context)


def success_view(request):
    return render(request, "success.html", {})


def cancel_view(request):
    return render(request, "cancel.html", {})


def forgot_password(request):
    return render(request, "forgot_password.html", {})


@csrf_exempt
@require_http_methods(["POST"])
def coinbase_webhook(request):
    logger = logging.getLogger(__name__)

    request_data = request.body.decode("utf-8")
    request_sig = request.headers.get("X-CC-Webhook-Signature", None)
    webhook_secret = settings.COINBASE_COMMERCE_WEBHOOK_SHARED_SECRET

    try:
        event = Webhook.construct_event(request_data, request_sig, webhook_secret)

        # List of all Coinbase webhook events:
        # https://commerce.coinbase.com/docs/api/#webhooks

        if event["type"] == "charge:confirmed":
            logger.info("Payment confirmed.")
            user_id = event["data"]["metadata"].get("user_id")
            txn_id = event["data"]["metadata"].get("txn_id")

            if txn_id:
                txn = Transaction.objects.filter(id=txn_id).first()
                if txn:
                    txn.status = "success"
                    txn.save()

            # TODO: run some custom code here
        elif event["type"] == "charge:failed":
            logger.info("Payment failed.")
            user_id = event["data"]["metadata"].get("user_id")
            txn_id = event["data"]["metadata"].get("txn_id")

            if txn_id:
                txn = Transaction.objects.filter(id=txn_id).first()
                if txn:
                    txn.status = "failed"
                    txn.save()

    except (SignatureVerificationError, WebhookInvalidPayload) as e:
        return HttpResponse(e, status=400)

    logger.info(f"Received event: id={event.id}, type={event.type}")
    return HttpResponse("ok", status=200)


def initiate_payment(request):
    if request.method == "GET":
        return render(request, "initiate_payment.html", {})
    elif request.method == "POST":
        print("req: ", request.POST)
        amount = request.POST.get("amount")
        name = request.POST.get("name")
        description = request.POST.get("description")

        try:
            if int(amount) < 0:
                messages.error(request, f"Amount must be greater than 0")
                return redirect("initiate_payment")
        except ValueError:
            messages.error(request, f"Invalid Amount")
            return redirect("initiate_payment")

        # Create a deposit record in your database
        txn = Transaction.objects.create(
            source="crypto",
            invoice_id=generate_invoice_number(),
            amount=amount,
            name=name,
            description=description,
        )

        # Initialize the Coinbase Commerce client
        coinbase_client = Client(api_key=settings.COINBASE_COMMERCE_API_KEY)

        # Create a Coinbase Commerce charge
        charge = coinbase_client.charge.create(
            name=f"Transfer by {name}",
            description=f"Crypto Transfer by {name}",
            local_price={
                "amount": amount,
                "currency": "USD",
            },  # Use your desired currency
            pricing_type="fixed_price",
            metadata={
                "txn_id": str(txn.id),
                "user_id": str(request.user.id) if request.user else None,
                "name": name,
                "description": description,
            },  # Store the deposit ID for reference
        )

        # Redirect the user to the Coinbase Commerce payment page
        payment_url = charge.hosted_url

        return redirect(payment_url)
    else:
        return render(request, "initiate_payment.html", {})
