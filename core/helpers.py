import random


def calculate_amount_received(initial_investment, daily_interest_rate, days):
    days = int(days)
    initial_investment = float(initial_investment.replace(",", ""))
    daily_interest_rate = float(daily_interest_rate)

    # Calculate the final amount received
    interest_for_a_day = (daily_interest_rate / 100) * initial_investment

    total_interest_to_receive = interest_for_a_day * days

    return initial_investment + total_interest_to_receive


def generate_invoice_number():
    # Generate a random 6-digit number
    random_number = random.randint(100000, 999999)

    # Create the invoice number string
    invoice_number = f"INV-{random_number}"

    return invoice_number
