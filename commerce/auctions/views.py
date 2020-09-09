from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, Auction_Listings
from django.contrib.auth.decorators import login_required 

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Auction_Listings.objects.all()
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

class ListingForm(forms.Form):
    title = forms.CharField(label = "Title", max_length=20)
    description = forms.CharField(label = "Description", max_length=50)
    starting_bid = forms.IntegerField(label = "Price(INR)")
    image_url = forms.URLField(label='Image')
    
    CHOICES = [
        ("FA", 'Fashion'),
        ("EL", 'Electronics'),
        ("HO", 'Home'),
        ("MU", 'Music'),
        ("BO", 'Books'),
    ]
    category = forms.ChoiceField(choices = CHOICES, initial = "FA")

def createListing(request):
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = ListingForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            ti = form.cleaned_data["title"]
            des = form.cleaned_data["description"]
            bid = form.cleaned_data["starting_bid"]
            img = form.cleaned_data["image_url"]
            cat = form.cleaned_data["category"]
            listing = Auction_Listings(title = ti, description = des, starting_bid = bid, image_url = img, category = cat, current_bid = bid, owner = request.user)
            listing.save()
            # Redirect user to list of tasks
            return HttpResponseRedirect(reverse("index"))
        
        else:
            # If the form is invalid, re-render the page with existing information.
            return render(request, "auctions/createListing.html", {
                "form": form
            })

    return render(request, "auctions/createListing.html", {
        "form": ListingForm()
    })

class BidForm(forms.Form):
    bid = forms.IntegerField(label = "Price(INR)")

def listing(request, id):
    item = Auction_Listings.objects.get(pk = id)
    c = dict(item.CHOICES)
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = BidForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            bid = form.cleaned_data["bid"]
            current_bid = item.current_bid

            if (bid < current_bid):
                return render(request, "auctions/Listing.html", {
                "form": form,
                "listing": item,
                "choice": c[item.category],
                "message": "Your bid is less than the current bid."
            })
            else:
                item.current_bid = int(bid)
                item.save()
                # Redirect user to list of tasks
                return HttpResponseRedirect(reverse("index"))
        
        else:
            # If the form is invalid, re-render the page with existing information.
            return render(request, "auctions/Listing.html", {
                "form": form,
                "listing": item,
                "choice": c[item.category],
            })

    return render(request, "auctions/listing.html", {
        "form": BidForm(),
        "listing": item,
        "choice": c[item.category],
    })

def search(request, cat): # cat -> category
    items = Auction_Listings.objects.filter(category = cat)
    return render(request, "auctions/index.html", {
        "listings": items
    })


@login_required
def show_watchList(request):
    return render(request, "auctions/watchlist.html", {
        "items": request.user.my_items.all()
    })

@login_required
def addToWatchList(request, id):
    item = Auction_Listings.objects.get(pk = id)
    current_user = request.user
    current_user.my_items.add(item)
    current_user.save()
    return render(request, "auctions/watchlist.html",{
        "items": current_user.my_items.all()
    })

@login_required
def remove(request, id):
    item = Auction_Listings.objects.get(pk = id)
    current_user = request.user
    current_user.my_items.remove(item)
    current_user.save()
    return render(request, "auctions/watchlist.html",{
        "items": current_user.my_items.all()
    })

@login_required
def close(request, id):
    item = Auction_Listings.objects.get(pk = id)
    item.delete()
    return render(request, "auctions/index.html")

