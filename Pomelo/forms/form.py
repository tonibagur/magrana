from django import forms

class GiftForm(forms.Form):
    name = forms.CharField(max_length=20)
    price = forms.DecimalField()
    email = forms.EmailField()
    message = forms.CharField(max_length=500)
    url_video = forms.CharField(max_length=500)
