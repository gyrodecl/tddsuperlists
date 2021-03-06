from unittest import skip

from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase
from django.http import HttpRequest
from django.utils.html import escape

from lists.models import Item, List
from lists.views import home_page
from lists.forms import (DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR,
                         ExistingListItemForm, ItemForm,)

#Each Test class is for a different view

#[0]test whether our homepage url returns the correct view and template
#lists/home
class HomePageTest(TestCase):
    maxDiff = None
    
    #Add chapter 11--check template used rather than which function
    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')
    
    #Add chapter 11-form
    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'],ItemForm)

    '''
    #Ch 2--old tests that didn't use the django test client    
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
    '''
    
    ''' Ch2 don't need this anymore
    def test_home_page_returns_correct_html(self):
        #the below should probably be
        #response = self.client.get('/lists/')
        #self.assertEqual(response.status_code, 200)
        #self.assertTemplateUsed(response, 'lists/home.html')
        
        request = HttpRequest()    #low-level testing---actually creating a request
        response = home_page(request)    #and passing it to the view function
        expected_html = render_to_string('lists/home.html', {'form':ItemForm()})   #and testing what templates render
        self.assertMultiLineEqual(response.content.decode(), expected_html)  #just test whether right template is being used
    '''

#[1]test whether you can create a new list by posting to '/lists/new'
#and whether it redirects to 'lists/(numberofnewlist)
class NewListTest(TestCase):
    
    def test_saving_a_POST_request(self):
        response = self.client.post('/lists/new',
                    data={'text':"A new list item"})
        
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
                        data={'text': 'A new list item'})
        created_list = List.objects.first()
        self.assertRedirects(response, ('lists/%d/' % (created_list.id,)))
        #self.assertEqual(response.status_code,302)    #run assertions
        #self.assertEqual(response['location'],'/lists/the-only-list-in-the-world/')


#[2]test our view that adds an item to an existing list
# '/lists/%d/add_item'
#can we add an item to an existing list and does it redirect
#to the page to view the new list
class NewItemTest(TestCase):
    
    #Ch10--test that user can't save a list with a blank item--want
    #error messages sent back to user
    ''' CH:11 ---WE SPLIT THIS BELOW TEST INTO #
    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/home.html')
        expected_error = escape("You can't have an empty list item")
        #print (response.content.decode())
        self.assertContains(response, expected_error)
    '''
    #1
    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post('/lists/new', data={'text':''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/home.html')
    
    #2
    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post('/lists/new', data={'text':''})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))
    
    #3
    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={'text':''})
        self.assertIsInstance(response.context['form'],ItemForm)
    
    
    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(),0)
        self.assertEqual(Item.objects.count(),0)


#[3]tests our View for individual lists---/lists/(num)/
#a.do we use the right template?
#b.what items get shown on a given list
class ListViewTest(TestCase):
        
    #Valid get request uses the main template
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
    
    
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        self.client.post(
            '/lists/%d/' % (correct_list.id,),
            data={'text': 'A new item for an existing list'}
        )
        
        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text,'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)
        
        #make sure our post to existing list redirects to existing list
    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        response = self.client.post(
            '/lists/%d/' % (correct_list.id,),
            data={'text': 'A new item for an existing list'}
        )
        #most_recent_list_id = List.objects.first().id 
        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))

        
    #Add Chapter 10---make sure view_list uses the ItemForm
    #This is the valid get request--want to display form
    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertIsInstance(response.context['form'],ExistingListItemForm)
        self.assertContains(response, 'name="text"')
    
    #ch.10 helper method
    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(
            '/lists/%d/' % (list_.id,),
            data={'text': ''}
        )

    #ch10
    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(),0)

    #ch10
    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/list.html')
        
    #ch10
    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'],ExistingListItemForm)

    #ch10
    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))
    
    #ch12---Experimenting with Duplicate Item Validation at the Views Layer
    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text="textey")
        #then try to pass duplicate data into the list
        response = self.client.post(
            '/lists/%d/' % (list1.id,),
            data={'text': "textey"}
        )
        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'lists/list.html')
        self.assertEqual(Item.objects.all().count(),1)
    

    #Added Chapter 10
    #SPLIT THE BELOW INTO 3 Separate Tests
    '''
    def test_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        response = self.client.post(
            '/lists/%d/' % (list_.id,),
            data={'text': ''}
        )
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'lists/list.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)
    '''
    
    '''
    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)
        response = self.client.get('/lists/the-only-list-in-the-world/')
        
        self.assertContains(response, 'itemey 1' )
        self.assertContains(response, 'itemey 2')
    '''