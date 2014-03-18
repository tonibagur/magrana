from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from .. forms.form import GiftForm
from .. models.models import PomeloUser
import random

def registerGift(request):
    if (request.method=='POST'):
	request_copy = request.POST.copy()
	receiver = False
	if (request.POST['receiver']=='' and request.POST['email']!= ''):
	    print(request.POST['email'].split('@')[0])
	    user = User.objects.create_user(request.POST['email'].split('@')[0], request.POST['email'], str(random.randrange(1000, 9000)))
	    receiver = PomeloUser(user=user)
	    receiver.save()
	    request_copy['receiver'] = str(receiver.id)
	form = GiftForm(request_copy)
        if form.is_valid():
	    gift = form.save(commit=False)		
	    gift.sender = PomeloUser.objects.get(user=request.user.id)
	    gift.product = request.POST['products'] 
	    gift.save()	    
            return render(request, "resposta.html")
        else:
	    print('*************************')
	    print(form.errors)
            return render(request, "form.html", {
                'form' : form,
                'form_error': form.errors,
            })
    else:
        form = GiftForm()
        return render(request, "form.html", {
                'form' : form,
            })
