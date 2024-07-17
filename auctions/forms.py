
from django import forms
from .models import *

class ListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'price', 'fixed_bid', 'image', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'description-class'}),
        }

class NewBidForm(forms.Form):
    bid = forms.IntegerField(label="Bid")

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {'content': ''}
        widgets = {
            'content': forms.Textarea(attrs={'class': 'custom-class'}),
        }


