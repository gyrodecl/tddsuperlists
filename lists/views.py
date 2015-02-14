from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from lists.models import Item, List

def home_page(request):
    return render(request, 'lists/home.html',{})
    
    
def view_list(request, list_id):
    requested_list = List.objects.get(id=list_id)
    items = requested_list.item_set.all()
    return render(request, 'lists/list.html',{'items':items,
                'list':requested_list})


def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST.get('item_text'), list=list_)
    return HttpResponseRedirect('/lists/%d/' % list_.id)


def add_item(request, list_id):
    requested_list = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST.get('item_text'), list=requested_list)
    return HttpResponseRedirect('/lists/%d/' % requested_list.id)