# 11b [Individual] Integrate with Payment

**Type: Individual**

We have come full circle! We started out talking about various ways to integrate with payment providers.

You are free to choose any payment provider and not just Stripe.

This assignment can be solved with various work loads. All of them count.

**Motivation:** This could potentially become useful for your thesis project.

---

## Setup

```
$ poetry install --no-root
```

---

## Usage

```
$ poetry shell
$ uvicorn main:app --reload
```

Then open your browser and go to:
http://localhost:8000

## 🛍️ Step-by-Step: Simulate a Pant Purchase

**Open the Checkout Page**  
Visit http://localhost:8000/ in your browser to see the product (in this case a pair of pants) and quantity field.

**Choose Quantity and Click "Checkout"**  
Select how many pants you want to buy and click the "Checkout" button.

**Get Redirected to Stripe Checkout**  
A new page will open hosted by Stripe, showing your selected product and total price.

Use the following Stripe test card details to simulate payment:

📧 Email: Any email with the correct format  
💳 Card Number: 4242 4242 4242 4242  
📅 Expiration Date: Any future date  
🙍‍♂️ Card Holder Name: Any name  
🔐 CVC: Any 3 digits  
🌍 Country or region: Pick a country from the list

**Complete or Cancel the Checkout**  
To complete a successful purchase, click the "Pay" button. You’ll be redirected to the success.html page.  
To simulate a cancelled purchase, click the "Go back" or "Cancel" button. You’ll be redirected to the cancel.html page.
