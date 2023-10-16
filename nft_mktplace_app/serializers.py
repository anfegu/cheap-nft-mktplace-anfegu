from rest_framework import serializers
from .models import NFTToken, Listing, Bid, Transaction

class NFTTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFTToken
        fields = '__all__'

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
