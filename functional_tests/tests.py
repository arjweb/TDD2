import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import sys


class NewVisitorTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)  # To avoid issues if browser can't keep up with tests

    def tearDown(self):
        self.browser.quit()

    # Helper method
    def check_for_row_in_list_table(self, expected_row):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(
            expected_row,
            [row.text for row in rows]
        )

    # -----------------------------------------------------------

    def test_layout_and_styling(self):
        # Edith goes to the home page
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centred
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512, delta=5
        )
        # She starts a new list and sees the input is nicely
        # centered there too
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )

    def test_starting_a_new_todo_list(self):
        # Edith has heard of a great website on to to lists and goes to homepage
        self.browser.get(self.server_url)
        header = self.browser.find_element_by_tag_name('h1')
        self.assertIn('To-Do', header.text)

        # She notices the header mentions to-do lists
        self.assertIn('To-Do', self.browser.title)

        # She is invited to enter a do-do right away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # She types "Buy peacock feathers" into a to-do
        inputbox.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates and lists "1. Buy peacock feathers"
        inputbox.send_keys(Keys.ENTER)

        # import time
        # time.sleep(10)

        self.check_for_row_in_list_table("1: Buy peacock feathers")

        # There is still a text box inviting her to enter another to-do
        # She enters "Use feathers to make a fly"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table("2: Use feathers to make a fly")
        self.check_for_row_in_list_table("1: Buy peacock feathers")

        # Edith sees her list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # Now a new user, Francis, comes along to the site
        # # We use a new browser session so no cookies shared etc.
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # Francis visits the home page, and there is no trace of Edith's list
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis starts a new list by entering a new item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again no sign of Edith's content
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Edith wonders whether the site will remember her list.  She sees there is a
        # unique url for her
        # self.fail('Finish the test')

        # She visits that url and her list is still there

        # Satisfied, they both go to sleep


if __name__ == '__main__':
    unittest.main()
