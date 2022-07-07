#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def main(dict):
    try:
        dealerId = int(dict['dealerId'])

        authenticator = IAMAuthenticator(dict['apikey'])
        service = CloudantV1(authenticator=authenticator)
        service.set_service_url(dict['url'])

        dealer = get_dealer(service, dealerId)
        reviews = get_reviews(service, dealerId)
        return {
            'statusCode': 200,
            'dealer': dealer,
            'reviews': reviews
        }
    except KeyError:
        return {
            'statusCode': 400,
            'message': 'no dealerId specified'
        }
    except ValueError:
        return {
            'statusCode': 400,
            'message': 'dealerId must be integer'
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


def get_dealer(service, dealerId):
    db = 'dealerships'
    fields = [
        'id', 'city', 'state', 'st',
        'address', 'zip', 'lat', 'long',
        'short_name', 'full_name'
    ]
    selector = {'id': {'$eq': dealerId}}
    dealer = service.post_find(
        db=db, selector=selector, fields=fields).get_result()
    if not len(dealer['docs']):
        raise ApiException(code=404, message='dealer does not exist')
    return dealer['docs'][0]


def get_reviews(service, dealerId):
    db = 'reviews'
    fields = [
        '_id', 'name', 'dealership', 'review',
        'purchase', 'purchase_date', 'car_make',
        'car_model', 'car_year', 'sentiment'
    ]
    selector = {'dealership': {'$eq': dealerId}}
    reviews = service.post_find(
        db=db, selector=selector, fields=fields).get_result()
    return reviews['docs']
