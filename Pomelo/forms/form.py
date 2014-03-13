from django.forms import ModelForm
from .. models.models import Gift

class GiftForm(ModelForm):
    class Meta:
        model = Gift
        fields = '__all__'
