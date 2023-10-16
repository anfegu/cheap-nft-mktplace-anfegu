from django.db import models
from django.contrib.auth.models import User

class NFTToken(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

def __str__(self):
    return self.name

class Listing(models.Model):
    token = models.ForeignKey(NFTToken, on_delete=models.CASCADE)
    seller = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_auction = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    current_highest_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.token.name} - ${self.price}"

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bidder = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.bidder} - ${self.amount}"

class Transaction(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    buyer = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    settled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.listing.token.name} - ${self.amount} - Settled: {self.settled}"
