from msilib import MSIMODIFY_DELETE
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404

#-------------------------------------------------------------------

class Listings(models.Model):
    ...

    ELECTRONICS = 'TCH'
    CLOTHING = 'CLT'
    UNKNOWN = 'UNK'
    FOOD = 'FOD'
    ART = 'ART'
    ACCESSORIES = 'AC'


    CATEGORY_CHOICES = [
    (ELECTRONICS, 'Electronics'),
    (FOOD, 'Food'),
    (ART, 'Art'),
    (CLOTHING, 'Clothing'),
    (ACCESSORIES, 'Accessories'),
    (UNKNOWN, 'Unknown'),
    ]

    category = models.CharField(max_length = 3, choices = CATEGORY_CHOICES, default = 'ELECTRONICS')


#         category = Listings.objects.filter(category = selection)


class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/categories', blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Listings(models.Model):
    ...
    category = models.ForeignKey(..)
       
    c = Category.objects.get(category_id)
    listings = c.objects.all()
#-------------------------------------------------------------------

# def category_listing(request, selection):
#     try:
#         category = Listings.objects.filter(category = selection)
#     except:
#         category = None
#     return render(request, "auctions/category_listing.html", {
#           "category": category, 
#           "selection": selection, 
#           "categories": Listings.CATEGORY_CHOICES})

#  {% for item in category %}

def category_listing(request, category_id):
    listings = Listings.objects.filter(category = category_id)
    return render(request, "auctions/category_listing.html", {
            "listings": listings})

#  {% for listing in listings %}

#-------------------------------------------------------------------

@login_required(login_url='login')
def create_listing(request):
    ...

def login_view(request):
    if request.method == "POST":

        #...
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('index')

#-------------------------------------------------------------------

def view_listing(request, item):
    pass

def view_listing(request, listing_id):
    pass


#-------------------------------------------------------------------

        listing = get_object_or_404(pk = listing_id)
        # try:
        #     f = Listings.objects.get(pk = item)
        # except Listings.DoesNotExist:
        #     raise Http404("Listing not found")


#-------------------------------------------------------------------
   watchers = models.ManyToManyField(User, blank=True, related_name="watched_listings")

@login_required(login_url='login')
def my_watchlist(request):
    return render(request, "auctions/index.html", {
        'listings': request.user.watched_listings.order_by('-created_at'),
        'banner': 'My Watchlist'
    })

class Listing(models.Model):

    def watcher_count(self):
        return len(self.watchers.all())

    def toggle_watcher(self, user):
        user_is_watching = self.watchers.filter(id=user.id).exists()
        if user_is_watching:
            self.watchers.remove(user)
        else:
            self.watchers.add(user)

#-------------------------------------------------------------------

# fat model

class Listing():

    #...

    def minimum_bid(self):
        return max(self.starting_bid, 1+self.high_bid_amount())

    def high_bid(self):
        return self.bids.all().order_by('-created_at').first()

    def high_bid_amount(self):
        bid = self.high_bid()
        if bid:
            return bid.amount
        else:
            return 0 

#-------------------------------------------------------------------

def categories_view(request, chosen_category):
    if chosen_category == 'All':
        categories = []
        listings = Listing.objects.all()
        for listing in listings:
            if listing.category not in categories:
                categories.append(listing.category)
        if len(categories) == 0: categories = False
        return render(request, 'auctions/categories.html', {"categories":categories,
                                                            "All": True})
    else:
        listings = Listing.objects.filter(category=chosen_category)
        return render(request, 'auctions/categories.html', {"listings":listings,
                                                            "All": False,
                                                            "category": chosen_category})



{% extends "auctions/layout.html" %}


    {% block main %}
    {% if All %}
    <h2>Categories</h2>

    <article>
        {% if categories %}
        {% for category in categories %}
            <section>{{ category }} <a class="w3-button view-listing"  href="{% url 'categories' category %}">View {{ category }}</a></section>
        {% endfor %}
        {% else %}
            There are currenlty no active listings to show
        {% endif %}
    </article>
   
{% else %}
     <h2>{{category}}</h2>

    <article>
        {% if listings %}
        {% for listing in listings %}
            <section>{{ listing }} <a class="w3-button view-listing"  href="{% url 'listing' listing.id %}">View {{ listing.title }}</a></section>
        {% endfor %}
        {% else %}
            There are currenlty no active listings to show
        {% endif %}
    </article>
    {% endif %}
    {% endblock %}



class NewListing(forms.Form):    
    categories = [
        ('Other', 'Other'),
        ('Furniture', 'Furniture'),
        ('Outdoor', 'Outdoor'),
        ('Sports', 'Sports'),
        ('Automobile', 'Automobile'),
        ('Bicycles', 'Bicycle'),
        ('Apparel', 'Apparel'),
        ('Electronics', 'Electronics'),
    ]
 
    title = forms.CharField(label="Title:")    
    price = forms.IntegerField(label="Price:", min_value=0)    
    description = forms.CharField(label="Entry:", widget=forms.Textarea())
    image = forms.ImageField(label="Image:", required=False)   
    category = forms.CharField(label="Category", widget=forms.Select(choices=categories))
