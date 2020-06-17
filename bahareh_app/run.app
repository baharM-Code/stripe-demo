#!/bin/bash

export STRIPE_PUBLISHABLE_KEY=pk_test_XE2Ln0QMZI3AEVYsjTk68agI
export STRIPE_SECRET_KEY=sk_test_oNOFntcaaT7OerMBeeu6GjJV
export STATIC_DIR="static/"
export TEMPLATE_DIR="templates/"
FLASK_ENV=development python app.py
