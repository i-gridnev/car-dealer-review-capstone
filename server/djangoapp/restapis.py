import requests
import json
from .models import CarDealer, DealerReview
from django.conf import settings
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


def send_request(url, method='GET', json_data='', **kwargs):
    try:
        response = requests.request(
            method=method, url=settings.API_CLOUDANT_DB + url, 
            headers={'Content-Type': 'application/json'},
            json=json_data,
            params=kwargs)
        json_data = json.loads(response.text)
        return json_data
    except:
        print("Network exception occurred")
        return {
            'statusCode': 500,
            'message': 'internal error'
        }

def get_dealer_by_id_from_cf(dealerId):
    url = '/dealership'
    response = send_request(url, dealerId=dealerId)
    if response['statusCode'] == 200:
        response['dealer'] = CarDealer(**response['dealers'][0])
    return response


def get_dealers_from_cf():
    url = '/dealership'
    response = send_request(url)
    if response['statusCode'] == 200:
        response['dealers'] = map(
            lambda raw: CarDealer(**raw), response['dealers'])
    return response


def get_reviews_by_dealer_id_from_cf(dealerId):
    url = '/review'
    response = send_request(url, dealerId=dealerId)
    if response['statusCode'] == 200:
        response['dealer'] = CarDealer(**response['dealer'])
        response['reviews'] = list(map(
            lambda raw: DealerReview(**raw), response['reviews']
        ))
    return response


def analyze_review_sentiments(text):
    authenticator = IAMAuthenticator(settings.WATSON_API_KEY)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator
    )
    natural_language_understanding.set_service_url(
        'https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com')

    response = natural_language_understanding.analyze(
        text=text,
        features=Features(sentiment=SentimentOptions()),
        language='en').get_result()
    return response['sentiment']['document']['label']



def post_review(review):
    url = '/review'
    response = send_request(url=url, method='POST', json_data=review)
    return response
