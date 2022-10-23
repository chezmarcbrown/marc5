import re
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import User, Listing
from .forms import ListingForm, BidForm

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            next_url = request.POST.get("next", "index")
            return redirect(next_url)
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        next_url = request.GET.get("next", "index")
        return render(request, "auctions/login.html", {"next": next_url })


def logout_view(request):
    logout(request)
    return redirect("index")


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
        return redirect("index")
    else:
        return render(request, "auctions/register.html")


def index(request):
    return render(request, "auctions/index.html", {
        'listings': Listing.objects.all().filter(active=True).order_by('-created_at'),
        'banner': 'All Listings'
    })

def listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.method == 'POST':
        clicked = request.POST["doit"]
        if clicked == "toggle-watcher":
            listing.toggle_watcher(request.user)
            return redirect('listing', listing_id=listing.id)
        elif clicked == "bid":
            return redirect('bid', listing_id=listing.id)
            return HttpResponse("make a bid")
        elif clicked == "close-auction":
            listing.active = False
            listing.save()
            return redirect('my-listings')
        else:
            return HttpResponseServerError(f'Unknown button clicked')
    else:
        being_watched = listing.watchers.filter(id=request.user.id).exists()
        return render(request, "auctions/listing.html", {
            'listing': listing,
            'being_watched': being_watched,
        })

@login_required(login_url='login')
def my_listings(request):
    # user.id needed because user is SimpleLazyObject, not reconstituted
    listings1 = Listing.objects.filter(creator=request.user.id).order_by('-created_at')
    listings2 = request.user.listings.all().order_by('-created_at')

    return render(request, "auctions/index.html", {
        'listings': request.user.listings.order_by('-created_at'),
        'banner': 'My Listings'
    })

@login_required(login_url='login')
def my_watchlist(request):
    return render(request, "auctions/index.html", {
        'listings': request.user.watched_listings.order_by('-created_at'),
        'banner': 'My Watchlist'
    })

@login_required(login_url='login')
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.creator = request.user
            listing.save()
            messages.success(request, f'Listing created successfully!')
            return redirect("index")
        else:
            messages.error(request, 'Problem creating the listing. Details below.')	
    else: 
        form = ListingForm()
    return render(request, "auctions/new_listing.html", {'form':form})

@login_required(login_url='login')
# should check that the user is not the creator of this item
def bid(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.method == 'POST':
        form = BidForm(request.POST)
        form.set_minimum_bid(listing.high_bid_amount())
        if form.is_valid():
            bid = form.save(commit=False)
            bid.bidder = request.user
            bid.listing = listing
            bid.save()
            return redirect('listing', listing_id=listing_id)
        else:
            messages.error(request, "Problem with the bid")
    else:
        form = BidForm()
    return render(request, "auctions/bid.html", {
            'form': form,
            'listing': listing,
        })
   