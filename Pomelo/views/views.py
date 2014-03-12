from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext, loader

def registerGift(request):
	#template = loader.get_template('form.html')
	#if (request.method=='POST'):
	#	form = ContractForm(request.POST)
	#	if form.is_valid():
	return render(request, "form.html")
