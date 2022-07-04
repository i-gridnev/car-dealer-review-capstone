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
        response = requests.get( settings.API_CLOUDANT_DB + url, headers={'Content-Type': 'application/json'},
                                params=kwargs)
    except:
        print("Network exception occurred")
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url)
    if json_result:
        dealers = json_result["rows"]["docs"]
        for dealer_doc in dealers:
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"], state=dealer_doc["state"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results


def get_dealer_by_id_from_cf(url, dealerId):
    json_result = get_request(url, dealerId=dealerId)
    dealer_doc = json_result["rows"]["docs"][0]
    return CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                     id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                     short_name=dealer_doc["short_name"], state=dealer_doc["state"],
                     st=dealer_doc["st"], zip=dealer_doc["zip"])


def get_reviews_by_dealer_id_from_cf(url, dealerId):
    results = []
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        reviews = json_result["docs"]["docs"]
        for review_doc in reviews:
            review_obj = DealerReview(
                id=review_doc.get('id'), name=review_doc.get('name'), dealership=review_doc.get('dealership'),
                review=review_doc.get('review'), purchase=review_doc.get('purchase'), car_make=review_doc.get('car_make'),
                purchase_date=review_doc.get('purchase_date'), car_model=review_doc.get('car_model'), car_year=review_doc.get('car_year')
            )
            results.append(review_obj)
    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
