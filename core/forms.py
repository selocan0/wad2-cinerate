from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }
        error_messages = {
            'rating': {
                'min_value': "Rating must be at least 1.",
                'max_value': "Rating cannot be more than 5.",
            },
        }
