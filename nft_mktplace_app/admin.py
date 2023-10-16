from django.contrib import admin

# Register your models here.
from .models import Bid, Listing, NFTToken, Transaction

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('token', 'seller', 'price', 'is_auction', 'start_time', 'end_time', 'current_highest_bid')  

class NFTTokenAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

admin.site.register(NFTToken, NFTTokenAdmin)

class BidAdmin(admin.ModelAdmin):
    list_display = ('listing', 'bidder', 'amount')

admin.site.register(Bid, BidAdmin)

class TransactionAdmin(admin.ModelAdmin):    
    list_display = ('listing', 'buyer', 'amount', 'settled')

admin.site.register(Transaction, TransactionAdmin)