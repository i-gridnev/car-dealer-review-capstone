import requests
import json
from .models import CarDealer, DealerReview
from django.conf import settings
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(settings.API_CLOUDANT_DB + url, headers={'Content-Type': 'application/json'},
                                params=kwargs)
        json_data = json.loads(response.text)
        return json_data
    except:
        print("Network exception occurred")
        return {
            'statusCode': 500,
            'message': 'internal error'
        }


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def get_dealer_by_id_from_cf(dealerId):
    url = '/dealership'
    response = get_request(url, dealerId=dealerId)
    if response['statusCode'] == 200:
        response['dealer'] = CarDealer(**response['dealers'][0])
    return response

# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf():
    url = '/dealership'
    response = get_request(url)
    if response['statusCode'] == 200:
        response['dealers'] = map(
            lambda raw: CarDealer(**raw), response['dealers'])
    return response


def get_reviews_by_dealer_id_from_cf(dealerId):
    url = '/review'
    response = get_request(url, dealerId=dealerId)
    if response['statusCode'] == 200:
        response['dealer'] = CarDealer(**response['dealer'])
        response['reviews'] = map(
            lambda raw: DealerReview(**raw), response['reviews']
        )
    return response


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
