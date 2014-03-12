from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from pomeloUsers.form import GiftForm

def registerGift(request):
	template = loader.get_template('pomeloUsers/index.html')
	#if (request.method=='POST'):
	#	form = ContractForm(request.POST)
	#	if form.is_valid():
	return HttpResponse(template.render(context))
