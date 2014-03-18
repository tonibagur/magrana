from django import forms
from django.forms import ModelForm
from django.forms import Textarea
from .. models.models import Gift
from .. models.models import PomeloUser

class GiftForm(ModelForm):
    name_products = (
	('fashion_her', 'Fashion Her'),
	('outdoors', 'Outdoors'),
	('home','Home'),
	('travel', 'Travel'),
	('media', 'Media'),
	('fashion_him', 'Fashion Him'),
    )
    products = forms.ChoiceField(choices=name_products)
    email = forms.EmailField()
    class Meta:
        model = Gift
        exclude = ['sender', 'product', 'id']
        widgets = {
	    'message': Textarea(attrs={'cols': 100, 'rows': 5}),
        }
        
