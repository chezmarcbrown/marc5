from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

class User(AbstractUser):
    pass

class Listing(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=500)
    active = models.BooleanField(default=True)
    starting_bid = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    watchers = models.ManyToManyField(User, blank=True, related_name="watched_listings")

    def __str__(self):
        return f'{self.title}'

    def watcher_count(self):
        return len(self.watchers.all())

    def toggle_watcher(self, user):
        user_is_watching = self.watchers.filter(id=user.id).exists()
        if user_is_watching:
            self.watchers.remove(user)
        else:
            self.watchers.add(user)

    def bidder_count(self):
        return len(self.bids.all())

    def high_bid(self):
        b = self.bids.all().order_by('-created_at')
        if len(b) == 0:
            return None
        else:
            return b.first()

    def high_bid_amount(self):
        bid = self.high_bid()
        if bid:
            return bid.amount
        else:
            return self.starting_bid


def validate_bid(value):
	print(f'calling validate rating {value}')
	if value < 0.0:
		raise ValidationError(f'Rating must be at least 0.0')
	elif value > 10.0:
		raise ValidationError(f'Rating cannot exceed 10.0')

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    

