from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from lists.models import Item

def home_page(request):
    return render(request, 'lists/home.html',{})
    
    
def view_list(request):
    items = Item.objects.all()
    return render(request, 'lists/list.html',{'items':items})


def new_list(request):
    Item.objects.create(text=request.POST.get('item_text'))
    return HttpResponseRedirect('/lists/the-only-list-in-the-world/')

