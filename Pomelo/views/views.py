from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from .. forms.form import GiftForm
from .. models.models import PomeloUser
import random
from django_youtube.views import upload 
from django_youtube.models import Video

def registerGift(request):
    if (request.method=='POST'):
        request_copy = request.POST.copy()
        receiver = False
        if (request.POST['receiver']=='' and request.POST['email']!= ''):
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
            print 'errors',form.errors         
            return render(request, "form.html", {
                'form' : form,
                'form_error': form.errors,
            })
    else:
        form = False
        video_id = request.GET.get('video_id', '')
        if video_id:
            videos = Video.objects.filter(video_id=str(video_id))
            video = list(videos[:1])
            if video:
                form = GiftForm(initial={
                    'url_video': video[0].youtube_url,
                    'youtube_embed' : ('embed/').join(video[0].youtube_url.split('&feature')[0].split('watch?v=')),
                    }) 
        else:
            form = GiftForm()
        youtube_form,y_post_url,y_next_url = upload(request,ret_view=False) 
        return render(request, "form.html", {
                'form' : form,
                'youtube_form': youtube_form,
                'y_post_url':y_post_url,
                'y_next_url':y_next_url,
            })
