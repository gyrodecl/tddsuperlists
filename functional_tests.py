from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
    
    def tearDown(self):
        self.browser.quit()
    
    def test_can_start_a_list_and_retrieve_it_later(self):
        #Lisa has heard about a cool new online to-do app.
        #She goes to check out its homepage
        self.browser.get('http://localhost:8000')

        #She notes the page title and header mention to-do Lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the Test!')

        #She is invited to enter a to-do item straight away

        #She types "Buy peacock feathers" into a text box

        #when she hits enter, the page updates and now the page lists
        #"1: Buy peacock feathers" as an item in a to-do list

        #There is still a text box inviting her to add another item.  She
        #enters "Use peacock features to make a fly" (Lisa is Methodical)

        #The page updates again, and now shows both items on her list

        #Lisa wonder whether the site will remember her list.  Then she sees
        #that the site has generated a unique URL for her -- there is some
        #explanatory text to that effect.
    
        #She visits the URL - her to-do list is still there

        #Satisfied, she goes back to sleep

if __name__ == '__main__':
    unittest.main(warnings='ignore')