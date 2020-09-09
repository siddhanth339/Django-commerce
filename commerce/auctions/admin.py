from django.contrib import admin
from .models import User, Auction_Listings
# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "starting_bid", "category")
admin.site.register(User)
admin.site.register(Auction_Listings, ListingAdmin)