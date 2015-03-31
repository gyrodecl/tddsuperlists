from django.test import TestCase

from lists.models import List, Item
from lists.forms import ExistingListItemForm, ItemForm, EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR

class ItemFormTest(TestCase):
    
    #[0]test form class on is own---how does it render
    def test_form_renders_item_text_input(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())
    
    #[1]test form class on its own--should throw error on blank items
    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],[EMPTY_ITEM_ERROR]
        )

    #[2]test that form will allow saving with our custom save method        
    def test_form_save_handles_saving_to_a_list(self):
        list_ = List.objects.create()
        form = ItemForm(data={'text':'do me'})
        new_item = form.save(for_list=list_)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text,'do me')
        self.assertEqual(new_item.list,list_)
    
    
    
#ch12 custom ExistingListItemForm to prevent duplication
#don't want integrity errors; want validation errors that get
#displayed to the user
class ExistingListItemFormTest(TestCase):
    
    def test_form_renders_item_text_input(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_)
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
    
    def test_form_validation_for_blank_items(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'],[EMPTY_ITEM_ERROR])
        
    def test_form_validation_for_duplicate_items(self, ):
        list_ = List.objects.create()
        Item.objects.create(list=list_,text='no twins!')
        form = ExistingListItemForm(for_list=list_, data={'text':'no twins!'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'],[DUPLICATE_ITEM_ERROR])
    
        #12---test basic form
    def test_form_save(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_,data={'text':'hi'})
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.all()[0])