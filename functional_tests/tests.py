from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.1)

    def test_can_start_a_list_for_one_user(self):
        # Joe has heard about a cool new online to-do app.  He checks out the app's
        # homepage.
        self.browser.get(self.live_server_url)

        #He notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is invited to enter a to-do item immediately
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # He types 'Buy new swingline stapler' into a text box (he lost his red
        # swingline)
        inputbox.send_keys('Buy new swingline stapler')

        # When he hits enter, the page updates, and now the page lists:
        # "1: Buy new swingline stapler" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy new swingline stapler')

        # There is still a text box inviting Joe to add another item.  He enters
        # "Burn down office and collect insurance money"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Burn down office and collect insurance money')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on Joe's list
        self.wait_for_row_in_list_table('1: Buy new swingline stapler')
        self.wait_for_row_in_list_table('2: Burn down office and collect insurance money')

        # Joe closes the browser knowing he can revisit the list

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Joe starts a new todo list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Don\'t talk about fight club')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Don\'t talk about fight club')

        # He notices that his list has a unique URL
        joe_list_url = self.browser.current_url
        self.assertRegex(joe_list_url, '/lists/.+')

        # Now a new user, Eliza, comes along to the site.

        ## We use a new browser session to make sure that no information of
        ## Joe's is coming through from cookies, etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Eliza visits the home page.  There is no sign of Joe's list.
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Don\'t talk about fight club', page_text)
        self.assertNotIn('Burn down office', page_text)

        # Eliza starts a new list by entering a new item.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Eliza gets her own unique url
        eliza_list_url = self.browser.current_url
        self.assertRegex(eliza_list_url, '/lists/.+')
        self.assertNotEqual(eliza_list_url, joe_list_url)

        # Again, there's no trace of Joe's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Don\'t talk about fight club', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfied, they both go back to sleep.
