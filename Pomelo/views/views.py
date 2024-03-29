from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django_youtube.views import upload 
from django_youtube.models import Video
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import random
from .. forms.form import GiftForm
from .. models.models import Gift
from .. models.models import PomeloUser
#send_mail('Subject here', 'Here is the message.', 'from@example.com', ['to@example.com'], fail_silently=False)

subject = 'You\'ve received a Pomelo Card'

def home(request):
        return HttpResponseRedirect('/demo_gift/')

def create_message(name_sender, name_receiver, message_sender, url):
    message = 'Dear ' + str(name_receiver) + ',\n' + name_sender  + ' just sent you a Pomelo Card Gift.\nCheck the video at the following url:\n' + str(url) + '\n\n'
    if (message_sender!=''):
        message = message + '"' + str(message_sender) + '" -- '
    message = message + name_sender + '\n\n' +  'Pomelo\'s Team.'
    return message

def register_gift(request):
    if (request.method=='POST'):
        request_copy = request.POST.copy()
        receiver = False
        if (request.POST['receiver']=='' and request.POST['email']!= '' and request.POST['price']!=''):
	    name_user = request.POST['email'].split('@')[0]
	    users = User.objects.filter(username=name_user)
	    if (len(users) == 0):
		user = User.objects.create_user(request.POST['email'].split('@')[0], request.POST['email'], str(random.randrange(1000, 9000)))
		receiver = PomeloUser(user=user)
		receiver.save()
	    else:
		receiver = PomeloUser.objects.get(user=users[0].id)
            request_copy['receiver'] = str(receiver.id)
        form = GiftForm(request_copy)
        if form.is_valid():
	    sender = PomeloUser.objects.get(user=request.user.id)
            gifts = Gift.objects.filter(sender=sender.id)
	    gift = None
            if (len(gifts) > 0):
		gift = gifts.last()
            if (gift and gift.state=='draft'):
		gift.product = request.POST['products']
                gift.email = request.POST['email']
                gift.price = request.POST['price']
                gift.message = request.POST['message']
                gift.state = 'sent'
                gift.receiver = PomeloUser.objects.get(id=request.POST.get('receiver'))
		gift.youtube_embed = request.POST['youtube_embed']
		gift.url_video = request.POST['url_video']
            else:
                gift = form.save(commit=False)
                gift.sender = sender
                gift.product = request.POST['products']
                gift.state ='sent'
            gift.save()
            receiver = PomeloUser.objects.get(id=gift.receiver.id)
            message = create_message(request.user.username, receiver, gift.message, gift.url_video)
            send_mail(subject, message, request.user.email, [request.POST['email']], fail_silently=False)  
            return render(request, "gift_confirmation.html")
        else:
            print 'errors',form.errors         
            return render(request, "form.html", {
                'form' : form,
                'form_error': form.errors,
            })
    else:
        init={}
        video_id = request.GET.get('video_id', '')
        pomelo_user = PomeloUser.objects.get(user=request.user.id)
        gifts = Gift.objects.filter(sender=pomelo_user.id)
        if video_id:
            videos = Video.objects.filter(video_id=str(video_id))
            video = list(videos[:1])
            gift_tmp = gifts.last()
            if video:
                init['url_video']=video[0].youtube_url
                init['youtube_embed'] = ('embed/').join(video[0].youtube_url.split('&feature')[0].split('watch?v='))
                init['message'] = gift_tmp.message
                init['price'] = gift_tmp.price
                init['email'] = gift_tmp.email
		if (gift_tmp.receiver!=None):
		    init['receiver'] = gift_tmp.receiver.id
                init['products'] = gift_tmp.product
        form = GiftForm(initial=init)
        youtube_form,y_post_url,y_next_url = upload(request,ret_view=False)             
        return render(request, "form.html", {
                'form' : form,
                'youtube_form': youtube_form,
                'y_post_url':y_post_url,
                'y_next_url':y_next_url,
                'gifts' : gifts,
        })

@csrf_exempt
def save_draft(request):
    id_pomelo_user = PomeloUser.objects.get(user=request.user.id)
    receiver = None
    if (request.POST.get('receiver')!=''):
	receiver = PomeloUser.objects.get(id=request.POST.get('receiver'))
    email = request.POST.get('email')
    price = request.POST.get('price')
    message = request.POST.get('message')
    product = request.POST.get('product')
    gifts = Gift.objects.filter(sender=id_pomelo_user.id)
    if price=='' :
        price = 0
    if (len(gifts) == 0):
        gift = Gift.objects.create(product=product, price=price, message=message, email=email, receiver=receiver, sender=id_pomelo_user)
    else:
        gift = gifts.last()
        if (gift.state=='sent'):
            gift = Gift.objects.create(product=product, price=price, message=message, email=email, receiver=receiver, sender=id_pomelo_user)
        else:
            gift.product = product
            gift.email = email
            gift.price = price
            gift.message = message
	    if (receiver):
		gift.receiver = receiver
            gift.sender = id_pomelo_user
            gift.save()
    return HttpResponse(gift.id)

def views_gifts(request):
    pomelo_user = PomeloUser.objects.get(user=request.user.id)
    gifts = Gift.objects.filter(sender=pomelo_user.id)
    return render(request, "gift_story.html", {
            'gifts' : gifts,
        })

        
