import stripe
from fastapi import Request
from typing import Optional, Union
from datetime import datetime
from stripe.checkout import Session
from stripe import PaymentIntent, Charge


def retrieve_successfull_purchase_details(stripe_session: Session, request: Request) -> dict:
    if not isinstance(stripe_session, Session):
        raise ValueError("stripe_session must be a Session object")
    
    if not isinstance(request, Request):
        raise ValueError("request must be a Request object")
    
    # Retrieve the session details from Stripe
    customer_details = stripe_session.get("customer_details", {})
    purchase_created = stripe_session.get("created")
    purchase_date = format_purchase_date(purchase_created)
    customer_email = customer_details.get("email", "N/A")
    customer_name = customer_details.get("name", "N/A")
    customer_country = customer_details.get("address", {}).get("country", "N/A")
    amount_total = stripe_session.get("amount_total")
    total_amount = format_total_amount(amount_total)
    
    stripe_payment_intent = retrieve_payment_intent(stripe_session)
    stripe_charge = retrive_stripe_charge(stripe_payment_intent)
    
    payment_method_details = stripe_charge.get("payment_method_details", {})
    card_details = payment_method_details.get("card", {})
    card_brand = card_details.get("brand", "N/A")
    card_last4 = format_last4_card_number(card_details.get("last4"))
    card_exp_month = card_details.get("exp_month")
    card_exp_year = card_details.get("exp_year")
    card_exp_date = format_card_exp_date(card_exp_month, card_exp_year)
    
    return {
                "request": request,
                "purchase_date": purchase_date,
                "customer_email": customer_email,
                "customer_name": customer_name,
                "customer_country": customer_country,
                "total_amount": total_amount,
                "card_brand": card_brand,
                "card_last4": card_last4,
                "card_exp_date": card_exp_date,
            }


def format_purchase_date(purchase_created: Optional[int]) -> str:
    if isinstance(purchase_created, int):
        return datetime.fromtimestamp(purchase_created).strftime("%Y-%m-%d %H:%M:%S")
    return "N/A"


def format_last4_card_number(card_last4: Optional[str]) -> str:
    if card_last4 is not None and isinstance(card_last4, str) and len(card_last4) == 4:
        return f"**** **** **** {card_last4}"
    return "N/A"


def format_card_exp_date(card_exp_month: Optional[int], card_exp_year: Optional[int]) -> str:
    if isinstance(card_exp_month, int) and isinstance(card_exp_year, int):
        if card_exp_month < 10:
            card_exp_month = f"0{str(card_exp_month)}"
        return f"{card_exp_month}/{card_exp_year}"
    return "N/A"


def format_total_amount(total_amount: Union[float, int, None]) -> str:
    if isinstance(total_amount, (int, float)):
        return f"${total_amount / 100}" # Convert cents to dollars
    return "N/A"


def retrieve_payment_intent(stripe_session: Session) -> PaymentIntent:
    if not isinstance(stripe_session, Session):
        raise ValueError("stripe_session must be a Session object")
    
    payment_intent_id = stripe_session.get("payment_intent")
    if not payment_intent_id:
        raise ValueError("Payment intent ID not found in the session")
    
    return stripe.PaymentIntent.retrieve(payment_intent_id)


def retrive_stripe_charge(payment_intent: PaymentIntent) -> Charge:
    if not isinstance(payment_intent, PaymentIntent):
        raise ValueError("payment_intent must be a PaymentIntent object")
    
    # Retrieve the charge using the latest_charge field
    latest_charge_id = payment_intent.get("latest_charge")
    if not latest_charge_id:
        raise ValueError("Latest charge ID not found in the payment intent")
    
    return stripe.Charge.retrieve(latest_charge_id)