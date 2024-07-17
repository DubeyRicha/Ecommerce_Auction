from logging import exception
from wsgiref.util import request_uri
from xxlimited import new
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.shortcuts import redirect

from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required



def index(request):
    categories = AuctionListing.objects.values_list('category', flat=True).distinct()
    
    listing =AuctionListing.objects.filter(active ="True")
    return render(request, "auctions/index.html",{
        "listing" : listing,
        "categories": categories
    })


def listing(request, list_id):
        
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
       
    listing = AuctionListing.objects.get(pk=list_id)
    watchlist = Watchlist.objects.filter(user=request.user, listing=listing)
    comments = Comment.objects.filter(listing = listing)
    already_watching = False
    if(watchlist):
        already_watching = True


    msg = request.session.pop('msg', None)
    context = {
        "listing": listing,
        "already_watching": already_watching,
        "bidform": NewBidForm(),
        "commentform": CommentForm,
        "comments":comments
    }
    if msg is not None:
        context["msg"] = msg
    return render(request, "auctions/listing.html",context)


def bid(request,list_id):
    if request.method == "POST":
        listing = AuctionListing.objects.get(pk=list_id)
        currentbid = listing.current_bid
        fixedbid = listing.fixed_bid
        bidform = NewBidForm(request.POST)

        if bidform.is_valid():
            bid = bidform.cleaned_data["bid"]
           
            if bid<= fixedbid:
                msg =f"your bid should be greater than fixed bid: {fixedbid}"
            elif currentbid is not None and bid <= currentbid:
                msg =f"your bid should be greater than current bid: {currentbid}"
            else:
                new_bid = Bid.objects.create(bidder=request.user, listing = listing,bid_amount = bid)
                listing.current_bid = bid
                listing.winner = request.user
                listing.save()
                msg ="bid placed successfully"
                    
            request.session['msg'] = msg    
        return HttpResponseRedirect("/listing/" + str(list_id))
    

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

def category(request,categoryname):
    category = AuctionListing.objects.filter(category =categoryname, active=True)
    return render(request, "auctions/category.html",{
        "category":category,
        "categoryname":categoryname
    })
def category_list(request):
    categorylist = AuctionListing.objects.values_list('category', flat=True).distinct()
    return render(request, "auctions/categorylist.html",{
        "categorylist":categorylist
    })

@login_required
def watchlist(request):
    user = request.user
    watchlists = Watchlist.objects.filter(user=user)
    return render(request, "auctions/watchlist.html",{
        "watchlists" :watchlists
    })

@login_required
def watch(request, list_id):
    listing = AuctionListing.objects.get(pk=list_id)

    if not Watchlist.objects.filter(user=request.user, listing=listing):
        if request.method == "POST":
            Watchlist.objects.create(user=request.user, listing=listing)

    else:
        if request.method == "POST":
            Watchlist.objects.filter(user=request.user, listing=listing).delete()

    return  HttpResponseRedirect('/listing/' + str(list_id))
    

@login_required
def createlisting(request):
    if request.method == "POST":
        form = ListingForm(request.POST,request.FILES)
        if form.is_valid():
            newListing = form.save(commit=False)
            newListing.seller = request.user
            newListing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html",{
                "form": form
            })

    form = ListingForm()
    return render(request, "auctions/create.html",{
        "form": form
    })

@login_required
def close(request,list_id):
    listing = AuctionListing.objects.get(pk = list_id)
    if listing.winner == request.user:
        msg = "listing closed successfully"
        listing.active = False
        listing.save()
    else:
        msg ="only the seller can close the listing"
    request.session['msg'] = msg
    return HttpResponseRedirect('/listing/' + str(list_id))


@login_required
def comment(request, list_id):
    listing = AuctionListing.objects.get(pk=list_id)
    form = CommentForm(request.POST)
    if form.is_valid:
        new_comment = form.save(commit=False)
        new_comment.commenter = request.user
        new_comment.listing = listing
        new_comment.save()
    return HttpResponseRedirect('/listing/' + str(list_id))
    
