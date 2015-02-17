'''
Functional Test for creating a list
'''
from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrieve_it_later(self):
        #Lisa has heard about a cool new online to-do app.
        #She goes to check out its homepage
        #self.browser.get('http://localhost:8000')
        self.browser.get(self.server_url)

        #She notes the page title and header mention to-do Lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        #She is invited to enter a to-do item straight away
        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        #She types "Buy peacock feathers" into a text box
        inputbox.send_keys('Buy peacock feathers')
        
        #import time
        #time.sleep(10)
        
        #when she hits enter, the page updates, she's taken to a new url
        #and now the page lists
        #"1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        lisa_list_url = self.browser.current_url
        self.assertRegex(lisa_list_url, '/lists/.+')
        
        #table = self.browser.find_element_by_id('id_list_table')
        #rows = table.find_elements_by_tag_name('tr')
        '''self.assertTrue(
            any(row.text == '1: Buy peacock feathers' for row in rows),
            "New to-do item did not appear in table---its text was: \n%s" %(
                table.text    
            )
        )
        '''
        #self.assertIn('1: Buy peacock feathers',[row.text for row in rows])
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        #There is still a text box inviting her to add another item.  She
        #enters "Use peacock feathers to make a fly" (Lisa is Methodical)    
        inputbox = self.get_item_input_box()
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)
                
        #The page updates again, and now shows both items on her list
        #table = self.browser.find_element_by_id('id_list_table')
        #rows = table.find_elements_by_tag_name('tr')
        #self.assertIn('1: Buy peacock feathers',[row.text for row in rows])
        #self.assertIn('2: Use peacock feathers to make a fly',[row.text for row in rows])
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
        
        #Now a new user Francis comes to our site
        #we user a new browser window to make sure no data, such as cookies,
        #are from Lisa's session
        self.browser.quit()
        self.browser = webdriver.Firefox()
        
        #Francis visits the home page---there's no sign of Lisa's list
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)
        
        #Francis starts a new list 
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        
        #Francis now has his own unique url for his list
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, lisa_list_url)
        
        #Again, there's no sign of Lisa's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Buy milk', page_text)
        self.assertNotIn('Buy peacock feathers', page_text)
        
        
        #self.fail('Finish the Test!') 
    
        #She visits the URL - her to-do list is still there

        #Satisfied, she goes back to sleep