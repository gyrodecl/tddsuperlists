from django.conf.urls import patterns, include, url
from lists import views

urlpatterns = patterns('',
    url(r'^$', 'lists.views.home_page', name='home'),
    url(r'^(?P<list_id>\d+)/$', 'lists.views.view_list',name='view_list'),
    url(r'^new$', 'lists.views.new_list',name='new_list'),
    url(r'^(?P<list_id>\d+)/add_item$','lists.views.add_item',name="add_item_to_list")                
                       
)