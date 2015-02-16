from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase
from django.http import HttpRequest
from django.utils.html import escape

from lists.models import Item, List
from lists.views import home_page

#[0]test whether our homepage url returns the correct view and template
class HomePageTest(TestCase):
    
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
        
    def test_home_page_returns_correct_html(self):
        #the below should probably be
        #response = self.client.get('/lists/')
        #self.assertEqual(response.status_code, 200)
        #self.assertTemplateUsed(response, 'lists/home.html')
        
        request = HttpRequest()    #low-level testing---actually creating a request
        response = home_page(request)    #and passing it to the view function
        expected_html = render_to_string('lists/home.html')   #and testing what templates render
        self.assertEqual(response.content.decode(), expected_html)  #just test whether right template is being used


#[1]test whether you can create a new list by posting to '/lists/new'
#and whether it redirects to 'lists/(numberofnewlist)
class NewListTest(TestCase):
    
    def test_saving_a_POST_request(self):
        response = self.client.post('/lists/new',
                    data={'item_text':"A new list item"})
        
        #request = HttpRequest()
        #request.method = 'POST'
        #request.POST['item_text'] = 'A new list item'
        
        #response = home_page(request)
        
        #now look at the Items stored in the database
        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')
    
    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new',
                        data={'item_text': 'A new list item'})
        created_list = List.objects.first()
        self.assertRedirects(response, ('lists/%d/' % (created_list.id,)))
        #self.assertEqual(response.status_code,302)    #run assertions
        #self.assertEqual(response['location'],'/lists/the-only-list-in-the-world/')


#[2]test our view that adds an item to an existing list
# '/lists/%d/add_item'
#can we add an item to an existing list and does it redirect
#to the page to view the new list
class NewItemTest(TestCase):
    
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        self.client.post(
            '/lists/%d/add_item' % (correct_list.id,),
            data={'item_text': 'A new item for an existing list'}
        )
        
        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text,'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)
        
        #make sure our post to existing list redirects to existing list
    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        response = self.client.post(
            '/lists/%d/add_item' % (correct_list.id,),
            data={'item_text': 'A new item for an existing list'}
        )
        #most_recent_list_id = List.objects.first().id 
        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))


    #Ch10--test that user can't save a list with a blank item--want
    #error messages sent back to user
    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/home.html')
        expected_error = escape("You can't have an empty list item")
        #print (response.content.decode())
        self.assertContains(response, expected_error)
    
    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(),0)
        self.assertEqual(Item.objects.count(),0)


#[3]tests our View for individual lists---/lists/(num)/
#a.do we use the righ template?
#b.what items get shown on a given list
class ListViewTest(TestCase):
    
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response,'lists/list.html')
    
    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)
        
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        
        self.assertContains(response, 'itemey 1' )
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')
    
    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'],correct_list)
    
    
    '''
    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)
        response = self.client.get('/lists/the-only-list-in-the-world/')
        
        self.assertContains(response, 'itemey 1' )
        self.assertContains(response, 'itemey 2')
    '''