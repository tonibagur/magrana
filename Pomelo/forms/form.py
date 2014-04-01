from django import forms
from django.forms import ModelForm
from django.forms import Textarea
from .. models.models import Gift
from .. models.models import PomeloUser
from djangular.forms import NgFormValidationMixin, NgModelFormMixin

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
    youtube_embed = forms.CharField(required=False)
    message = forms.CharField(required=False, widget=Textarea(attrs={'cols': 100, 'rows': 5}))
    url_video = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    class Meta:
        model = Gift
        exclude = ['sender', 'product', 'id', 'state']


class GiftFormWithNgModel(NgModelFormMixin, GiftForm):
    form_name = 'gift_form'
    scope_prefix = 'gift_data'


