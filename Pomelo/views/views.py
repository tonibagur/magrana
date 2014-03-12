from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from .. forms.form import GiftForm

def registerGift(request):
    if (request.method=='POST'):
        form = GiftForm(request.POST)
        if form.is_valid():
            pass
        else:
            return render(request, "form.html", {
                'form' : form,
                'form_error': form.errors,
            })
    else:
        form = GiftForm()
        return render(request, "form.html", {
                'form' : form,
            })
