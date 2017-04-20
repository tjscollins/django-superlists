from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Joe has heard about a cool new online to-do app.  He checks out the app's
        # homepage.
        self.browser.get('http://localhost:8000')

        #He notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!');

        # He is invited to enter a to-do item immediately

        # He types 'Buy a new stapler' into a text box (he lost his red swingline)

        # When he hits enter, the page updates, and now the page lists:
        # "1: Buy new swingline stapler" as an item in a to-do list

        # There is still a text box inviting Joe to add another item.  He enters
        # "Burn down office and collect insurance money"

        # The page updates again, and now shows both items on Joe's list

        # Joe wonders whether the site will remember his list.  Then he sees that
        # the site has generated a unique URL for him -- there is some explanatory
        # text to that effect.

        # He visits that URL -- the to-do list is still there

        # Joe closes the browser knowing he can revisit the list

if __name__ == '__main__':
    unittest.main(warnings='ignore')
