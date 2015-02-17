from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError

from lists.models import Item, List
from lists.forms import ItemForm

def home_page(request):
    return render(request, 'lists/home.html',{'form':ItemForm()})
    
    
def view_list(request, list_id):
    requested_list = List.objects.get(id=list_id)
    error = None
    if request.method == 'POST':
        try:
            item = Item(text=request.POST.get('text'), list=requested_list)
            item.full_clean()
            item.save()
            #return HttpResponseRedirect('/lists/%d/' % requested_list.id)
            return HttpResponseRedirect(requested_list.get_absolute_url())
        except ValidationError:
            error = "You can't have an empty list item"
    items = requested_list.item_set.all()
    return render(request, 'lists/list.html',{'items':items,                          
                'list':requested_list, "error":error })


def new_list(request):
    list_ = List.objects.create()
    item = Item(text=request.POST.get('text'), list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, 'lists/home.html',{"error":error })
    return HttpResponseRedirect(list_.get_absolute_url())


#def add_item(request, list_id):
#    requested_list = List.objects.get(id=list_id)
#    Item.objects.create(text=request.POST.get('item_text'), list=requested_list)
   