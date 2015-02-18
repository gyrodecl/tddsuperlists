from django.test import TestCase
from django.core.exceptions import ValidationError

from lists.models import Item, List

#[4]Just test models--saving and retriving--no views here
class ItemModelTest(TestCase):
    
    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')
    
    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())
    
    #Rewrite in Chapter 12--make easier
    '''
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()
        
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()
    
        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()
        
        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)
        
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(),2)
        
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text,'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text,'Item the second')
        self.assertEqual(second_saved_item.list,list_)
    '''   
        
    #chapter 10
    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    #Chapter 12--more validation constraints
    #[a] first the case we want to catch
    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='bla')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='bla')
            item.full_clean()
    
    #[b]second make sure it works normally--same text, different lists is ok
    #first time we've had a test with no assertion--want to make sure it's normal
    def test_CAN_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')
        item.full_clean()  #should not raise---no assertion--just making sure no error
    
    #[c]
    def test_list_ordering(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='i1')
        item2 = Item.objects.create(list=list1, text='item 2')
        item3 = Item.objects.create(list=list1, text='3')
        #self.assertEqual(
        #    list(Item.objects.all()),
        #    [item1, item2, item3]
        #)
        self.assertSequenceEqual(Item.objects.all(),[item1,item2,item3])
        
    #[d]test how models get represented as strings
    def test_string_representation(self):
        item = Item(text='some text')
        self.assertEqual(str(item), 'some text')
    
    
    
class ListModelTest(TestCase):
               
    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), '/lists/%d/' %(list_.id,))
    

'''
self.assertRaises is the same as
try:
    item.save()
    self.fail('The save should have raised an exception')
except ValidationError:
    pass
'''