from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

from lists.models import Item, List
from lists.forms import ItemForm

def home_page(request):
    return render(request, 'lists/home.html',{'form':ItemForm()})
    
    
def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save(for_list=list_)
            #return HttpResponseRedirect('/lists/%d/' % requested_list.id)
            return HttpResponseRedirect(list_.get_absolute_url())
    items = list_.item_set.all()
    return render(request, 'lists/list.html',{'items':items,                          
                'list':list_, 'form': form})


def new_list(request):
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            print("is valid")
            list_ = List.objects.create()
            form.save(for_list=list_)
            return HttpResponseRedirect(list_.get_absolute_url())
            #return HttpResponseRedirect(reverse('lists:home'))
    return render(request, 'lists/home.html',{'form': form})

#Ch10 Version---doesn't use modelform
'''
def new_list(request):
    list_ = List.objects.create()
    item = Item(text=request.POST.get('text'), list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, 'lists/home.html',
                      {"error":error})
    return HttpResponseRedirect(list_.get_absolute_url())
'''

#def add_item(request, list_id):
#    requested_list = List.objects.get(id=list_id)
#    Item.objects.create(text=request.POST.get('item_text'), list=requested_list)
   