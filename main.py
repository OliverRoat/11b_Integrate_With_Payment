import os
from datetime import datetime
from fastapi import FastAPI, Request, Form, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import stripe
from stripe_service import retrieve_successfull_purchase_details

load_dotenv()

app = FastAPI()

# Serve static files from the "public" directory under the "/static" path
app.mount("/static", StaticFiles(directory="public"), name="static")

templates = Jinja2Templates(directory="public")

# Load Stripe configuration
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
DOMAIN = os.getenv("DOMAIN")
PRODUCT_ID = os.getenv("TEST_PRODUCT_ID")


@app.get("/")
def serve_root_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/cancel")
def serve_cancel_page(request: Request):
    return templates.TemplateResponse("cancel.html", {"request": request})

@app.get("/success")
def serve_success_page(request: Request, session_id: str = Query(...)):
    try:
        # Retrieve the session details from Stripe
        session = stripe.checkout.Session.retrieve(session_id)
        purchase_details = retrieve_successfull_purchase_details(session, request)

        # Pass the data to the success.html template
        return templates.TemplateResponse(
            "success.html",
            purchase_details,
        )
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))


@app.post("/create-checkout-session") # Integration of Stripe Checkout
async def create_checkout_session(quantity: int = Form(...)):
    try:
        session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price": PRODUCT_ID,
                    "quantity": quantity,
                }
            ],
            mode="payment",
            success_url=f"{DOMAIN}/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{DOMAIN}/cancel",
        )
        return RedirectResponse(url=session.url, status_code=303)
    except Exception as e:
        return {"error": str(e)}