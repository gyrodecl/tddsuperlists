'''
Functional Tests for Superlists---test form input validation
'''
from unittest import skip
from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class ItemValidationTest(FunctionalTest):

    #Ch10--Validation of form inputs--see red error if try to submit empty form
    def test_cannot_add_empty_list_items(self):
        #Edith goes to the home page and accidentally tries to submit
        #an empty list item.  She hits Enter on the empty input box
        self.browser.get(self.server_url)
        inputbox = self.get_item_input_box()
        inputbox.send_keys('\n')
        
        #The home page refreshes, and there is an error message saying
        #that List items cannot be blank
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")
    
        #She tries again with some text for the item, which now works
        self.get_item_input_box().send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1: Buy milk')
        
        #She now decides to submit a second blank list item
        self.get_item_input_box().send_keys('\n')
        
        #She receives a similar warning on the List page
        self.check_for_row_in_list_table('1: Buy milk')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")
        
        #And she can correct it by filling some text in
        self.get_item_input_box().send_keys('Make tea\n')
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')
        
        #self.fail('write me')
        
    #ch12 advanced forms
    #[1]---test for our other form validation--no duplicate items!
    def test_cannot_add_duplicate_items(self):
        #Edith goes to the home page and starts a new list
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Buy wellies\n')
        self.check_for_row_in_list_table('1: Buy wellies')
        
        #she accidentally tries to enter a duplicate item
        self.get_item_input_box().send_keys('Buy wellies\n')
        
        #she sees a helpful error message
        self.check_for_row_in_list_table('1: Buy wellies')
        error = self.browser.find_element_by_css_selector('.has_error')
        self.assertEqual(error.text, "You've already got this in your list")
    