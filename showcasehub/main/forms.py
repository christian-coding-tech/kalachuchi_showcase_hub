from django import forms
from .models  import TeaserItem, Feedback

class TeaserItemForm(forms.ModelForm):
    class Meta:
        model = TeaserItem
        fields = ['title', 'image', 'description', 'Available', 'category',
                  'seller_name', 'store_name', 'store_location', 'store_link']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter teaser title'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter teaser description'}),
            'Available': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }