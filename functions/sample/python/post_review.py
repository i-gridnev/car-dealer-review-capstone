#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
from ibmcloudant.cloudant_v1 import CloudantV1, Document
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def main(dict):
    try:
        dealerId = int(dict['dealership'])

        authenticator = IAMAuthenticator(dict['apikey'])
        service = CloudantV1(authenticator=authenticator)
        service.set_service_url(dict['url'])

        check_dealer_exist(service, dealerId)
        valid_review = {
            'name': dict['name'],
            'dealership': dealerId,
            'review': dict['review'],
            'purchase': bool(dict['purchase']),
            'purchase_date': dict['purchase_date'],
            'car_make': dict['car_make'],
            'car_model': dict['car_model'],
            'car_year': dict['car_year'],
            'sentiment': dict['sentiment']
        }
        document = Document(**valid_review)
        db = 'reviews'
        return service.post_document(db=db, document=document).get_result()
    except (KeyError, ValueError):
        return {
            'statusCode': 400,
            'message': 'fields are invalid'
        }
    except ApiException as ex:
        if ex.code == 404:
            return {
                'statusCode': ex.code,
                'message': ex.message
            }
        else:
            return {
                'statusCode': 500,
                'message': 'something went wrong on the server'
            }


def check_dealer_exist(service, dealerId):
    db = 'dealerships'
    fields = ['id']
    selector = {'id': {'$eq': dealerId}}
    dealer = service.post_find(
        db=db, selector=selector, fields=fields).get_result()
    if not len(dealer['docs']):
        raise ApiException(code=404, message='dealer does not exist')
