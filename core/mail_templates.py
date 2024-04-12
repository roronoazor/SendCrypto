

SEND_TRANSACTION_OTP = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Account Verification</title>
</head>
<body>
    <p>Dear User,</p>
    <p>Here is your OTP code for the transaction: <strong>{{ otp_code }}</strong>.</p>
    <p>Please note that this code is only valid for 10 minutes. Use it promptly to proceed with your transaction.</p>
    
    <p>Best regards,</p>
    <p>XanderFX Team</p>
</body>
</html>
"""

NOTIFY_SETTLEMENT_TEAM_OF_CRYPTO_TO_CASH = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Transaction Notification</title>
</head>
<body>
    <p>Dear Settlement Team,</p>
    <p>Please be informed that {{ email }} has initiated a claim indicating that cryptocurrency was sent to exchange for cash.</p>
    <p>Below are the transaction details for your settlement processing:</p>
    <p>
        Transaction Date: <strong>{{ transaction_date }}</strong><br>
        Name: <strong>{{ name }}</strong><br>
        Email: <strong>{{ email }}</strong><br>
        Amount: <strong>{{ amount }}</strong><br>
        Type of Crypto: <strong>{{ crypto_type }}</strong><br>
        Bank Details:<br>
        &nbsp;&nbsp;&nbsp;Name: <strong>{{ bank_name }}</strong><br>
        &nbsp;&nbsp;&nbsp;Account Holder: <strong>{{ account_name }}</strong><br>
        &nbsp;&nbsp;&nbsp;Account Number: <strong>{{ account_number }}</strong><br>
        Invoice Number: <strong>{{ invoice_number }}</strong><br>
        Swift/BIC Code: <strong>{{ swift_bic }}</strong><br>
        IBAN: <strong>{{ iban }}</strong><br>
        Routing Number: <strong>{{ routing_number }}</strong>
    </p>
    <p>Your prompt attention to this matter is greatly appreciated.</p>
    <p>Thank you,</p>
</body>
</html>
"""


NOTIFY_SETTLEMENT_TEAM_OF_CASH_TO_CRYPTO = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Transaction Notification</title>
</head>
<body>
    <p>Dear Settlement Team,</p>
    <p>Please be informed that {{ email }} has initiated a claim indicating that cash was sent to exchange for cryptocurrency.</p>
    <p>
        Transaction Date: <strong>{{ transaction_date }}</strong><br>
        Name: <strong>{{ name }}</strong><br>
        Email: <strong>{{ email }}</strong><br>
        Amount: <strong>{{ amount }}</strong><br>
        Currency: <strong>{{ currency }}</strong><br>
        Wallet Address: <strong>{{ wallet_address }}</strong><br>
        Crypto Type: <strong>{{ crypto_type }}</strong><br>
        Invoice Number: <strong>{{ invoice_number }}</strong>
    </p>
    <p>Your prompt attention to this matter is greatly appreciated.</p>
    <p>Thank you,</p>
</body>
</html>
"""


CUSTOMER_RECEIPT_MAIL = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Transaction Receipt</title>
</head>
<body>
    <h1>Transaction Receipt</h1>
    <p>Hello,</p>
    <p>Please note that your transaction is in the process of being completed and is anticipated to be resolved within the next 24 hours.</p>
    <p>For your records, below are the details of the transaction:</p>
    <p>
        Invoice Number: <strong>{{ invoice_number }}</strong><br>
        Amount: <strong>{{ amount }}</strong><br>
        Cryptocurrency: <strong>{{ crypto_type }}</strong><br>
        Transaction Date: <strong>{{ transaction_date }}</strong>
    </p>
    <p>Thank you for choosing us,</p>
</body>
</html>
"""