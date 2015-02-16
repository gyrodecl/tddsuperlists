'''
Functional Tests for Superlists---test form input validation
'''
from unittest import skip
from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):

    #Ch10--Validation of form inputs
    def test_cannot_add_empty_list_items(self):
        #Edith goes to the home page and accidentally tries to submit
        #an empty list item.  She hits Enter on the empty input box
        
        #The home page refreshes, and there is an error message saying
        #that List items cannot be blank
    
        #She tries again with some text for the item, which now works
        
        #She now decides to submit a second blank list item
        
        #She receives a similar warning on the List page
        
        #And she can correct it by filling some text in
        self.fail('write me')