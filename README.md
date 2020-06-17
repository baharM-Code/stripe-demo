# stripe-demo
payment intents demo

Author
------
Bahareh Mir

About
-----
This is a demo app to demonstrate Stripe's payment intent API

To install and run app
----------------------
IMPORTANT: pre-requisites are a unix terminal with python3 (and pip3) installed

On a terminal run the following steps:

Step-1:

python3 -m venv flask

Step-2:

source flask/bin/activate

Step-3:

gunzip bahareh_app.tar.gz

Step-4:

tar xvf bahareh_app.tar

Step-5:

cd bahareh_app

Step-6:

pip3 install -r requirements.txt

Step-7:

./run.app

This will run a demo web server and next step would be to go to browser on same machine to simulate a client experience

Step-8:

Go to browser and enter: 

http://127.0.0.1:5000/

Step-9:

Click on currency type
Click 'Pay' and wait for further prompts
Repeat this step as many times as possible with different inputs

Step-10:

Ctrl+C to quit the web server if needed and check payments_secure.log for log entries of successful payments

cat payments_secure.log

go to Step-7 from here to repeat the program
