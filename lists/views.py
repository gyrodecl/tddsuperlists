from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from lists.models import Item

def home_page(request):
    if request.method == 'POST':
        if 'item_text' in request.POST:
            next_item = Item(text=request.POST.get('item_text'))
            next_item.save()
        return HttpResponseRedirect('/')
            #return render(request, 'lists/home.html',
            #              {'new_item_text': request.POST.get('item_text')})
    else:
        items = Item.objects.all()
        return render(request, 'lists/home.html',{'items':items})