from django.shortcuts import render
from django.http import HttpResponseRedirect

def registerGift(request):
	if (request.method=='POST'):
		form = ContractForm(request.POST)
		if form.is_valid():
