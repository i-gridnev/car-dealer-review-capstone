from django.db import models
from django.utils.timezone import now


class CarMake(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name


class CarModel(models.Model):
    CAR_TYPE = (
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'WAGON'),
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    delear_id = models.IntegerField()
    type = models.CharField(max_length=10, choices=CAR_TYPE)
    Year = models.DateField()

    def __str__(self) -> str:
        return f'{self.make} {self.name} dealerId={self.delear_id}'


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip, state):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.state = state
        self.zip = zip

    def __str__(self):
        return f'Dealer {self.short_name} -- {self.st}'

class DealerReview:
    def __init__(self, _id, name, dealership, review, purchase, sentiment, purchase_date='', car_make='', car_model='', car_year=''):
        self.id = _id
        self.name = name
        self.dealership = dealership
        self.review = review
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment

    def __str__(self):
        return f'review {self.id} for {self.dealership}' 
