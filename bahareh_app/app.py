#! /usr/bin/env python3.6

"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""

import stripe
import json
import os
import pprint
from datetime import datetime

from flask import Flask, render_template, jsonify, request, send_from_directory

# Setup Stripe python client library
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
stripe.api_version = os.getenv('STRIPE_API_VERSION')

item_cost = {
    'hotdog_pins': 1200 #EUR cents
}

currency_conversion = {
    "EUR": 0.8846,
    "USD": 1,
    "JPY": 107.2718,
    "CAD": 1.3577,
    "GBP": 0.7931,
    "CHF": 0.9463,
    "AUD": 1.4550
}

static_dir = str(os.path.abspath(os.path.join(__file__ , "..", os.getenv("STATIC_DIR"))))
template_dir = str(os.path.abspath(os.path.join(__file__ , "..", os.getenv("TEMPLATE_DIR"))))
app = Flask(__name__, static_folder=static_dir,
            static_url_path="", template_folder=template_dir)


@app.route('/', methods=['GET'])
def get_checkout_page():
    # Display checkout page
    return render_template('index.html', cost=item_cost['hotdog_pins'])


def calculate_order_amount(currency):
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    return "%d" % (item_cost['hotdog_pins'] * currency_conversion[currency])


@app.route('/create-payment-intent', methods=['POST'])
def create_payment():
    data = json.loads(request.data)
    # Create a PaymentIntent with the order amount and currency
    currency = 'USD'
    if data['currency'].upper() in currency_conversion:
        currency = data['currency'].upper()
    intent = stripe.PaymentIntent.create(
        amount=calculate_order_amount(currency),
        currency=currency
    )

    try:
        # Send publishable key and PaymentIntent details to client
        return jsonify({'publishableKey': os.getenv('STRIPE_PUBLISHABLE_KEY'), 'clientSecret': intent.client_secret})
    except Exception as e:
        return jsonify(error=str(e)), 403


def add_successful_log(entry):
    with open("payment_secure.log", "a") as log_file:
        log_file.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+": ")
        pprint.pprint(entry, log_file)

@app.route('/confirm', methods=['POST'])
def confirmation_received():
    add_successful_log(json.loads(request.data))
    return jsonify({'success':True}), 200

@app.route('/webhook', methods=['POST'])
def webhook_received():
    # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    request_data = json.loads(request.data)

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']
    data_object = data['object']

    if event_type == 'payment_intent.succeeded':
        print('💰 Payment received!')
        # Fulfill any orders, e-mail receipts, etc
        # To cancel the payment you will need to issue a Refund (https://stripe.com/docs/api/refunds)
    elif event_type == 'payment_intent.payment_failed':
        print('❌ Payment failed.')
    return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run()
