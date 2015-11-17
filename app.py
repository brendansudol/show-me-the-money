import logging
import os
import stripe

from flask import Flask, jsonify, request
from flask.ext.cors import CORS



stripe_keys = {
  'secret_key': os.environ.get('STRIPE_SECRET_KEY'),
  'publishable_key': os.environ.get('STRIPE_PUBLISHABLE_KEY')
}
stripe.api_key = stripe_keys['secret_key']


app = Flask(__name__)
cors = CORS(app)


stream_handler = logging.StreamHandler()
app.logger.addHandler(stream_handler)
app.logger.setLevel(logging.INFO)



@app.route('/')
def home():
    return 'Show me the money!'


@app.route('/charge', methods=['POST'])
def charge():
    try:
        post = request.form
        app.logger.info('payment from {}...'.format(post['email']))

        customer = stripe.Customer.create(
            email=post['email'],
            card=post['token_id'],
        )

        charge = stripe.Charge.create(
            customer=customer.id,
            amount=int(post['amount']),
            currency='usd',
        )

        outcome = 'success'
        app.logger.info('charge success!')
    except Exception as e:
        outcome = 'fail'
        app.logger.info('charge fail: ({})'.format(str(e)))

    return jsonify({'status': outcome})


@app.errorhandler(404)
def page_not_found(e):
    return 'Sorry, that page does not exist (404)', 404



if __name__ == '__main__':
    app.run()
