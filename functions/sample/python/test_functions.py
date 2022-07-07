import json
import get_reviews_by_dealerid
import post_review
from os import path


def make_creds():
    basepath = path.dirname(__file__)
    filepath = path.abspath(path.join(basepath, "..", "..", ".creds.json"))
    request = {}
    with open(filepath, mode='r') as f:
        request = json.load(f)
    return request


def test_get_reviews_by_dealerid(request, dealerId):
    request['dealerId'] = dealerId
    response = get_reviews_by_dealerid.main(request)
    return json.dumps(response, indent=2)


def test_post_review(request, new_review):
    request.update(new_review)
    response = post_review.main(request)
    return json.dumps(response, indent=2)


if __name__ == '__main__':
    request = make_creds()

    print(test_get_reviews_by_dealerid(request, 15))

    new_review = {
        "id": 1114,
        "name": "Simon Lidder",
        "dealership": 15,
        "review": "Oh, Great service!",
        "purchase": True,
        "another": "field",
        "purchase_date": "02/16/2021",
        "car_make": "Audi",
        "car_model": "Car",
    }
    # print(test_post_review(request, new_review))
