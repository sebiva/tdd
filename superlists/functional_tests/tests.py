from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import sys

class NewVisitorTest(StaticLiveServerTestCase):

  @classmethod
  def setUpClass(cls):
    for arg in sys.argv:
      if 'liveserver' in arg:
        cls.server.url = 'http://' + arg.split('=')[1]
        return
    super().setUpClass()
    cls.server_url = cls.live_server_url

  @classmethod
  def tearDownClass(cls):
    if cls.server_url == cls.live_server_url:
      super().tearDownClass()

  def setUp(self):
    self.browser = webdriver.Firefox()
    self.browser.implicitly_wait(3)
  def tearDown(self):
    self.browser.quit()

  def test_can_start_a_list_and_retrieve_it_later(self):
     # Open the page, first user, edith
    self.browser.get(self.server_url)

    # Check header
    self.assertIn('To-Do', self.browser.title)
    header_text = self.browser.find_element_by_tag_name('h1').text
    self.assertIn('To-Do', header_text)

    # Test input
    inputbox = self.browser.find_element_by_id('id_new_item')
    self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')
    # Adding something to the todo list
    inputbox.send_keys('Buy feathers')
    # When enter is pressed, the page should be updated and there should be an item
    # "1: Buy feathers" in a todo list table
    inputbox.send_keys(Keys.ENTER)
    edith_list_url = self.browser.current_url
    self.assertRegex(edith_list_url, '/lists/.+')
    self.check_for_row_in_list_table('1: Buy feathers')

    # Another item is added to the list
    inputbox = self.browser.find_element_by_id('id_new_item')
    inputbox.send_keys('Use feathers and build')
    inputbox.send_keys(Keys.ENTER)

    # Now both items should be shown
    self.check_for_row_in_list_table('1: Buy feathers')
    self.check_for_row_in_list_table('2: Use feathers and build')

    ###########################################
    # New user, Francis
    ###########################################

    # Use a new browser to make sure there is no info left about the old user.

    self.browser.quit()
    self.browser = webdriver.Firefox()

    self.browser.get(self.server_url)
    page_text = self.browser.find_element_by_tag_name('body').text
    self.assertNotIn('Buy feathers', page_text)
    self.assertNotIn('and build', page_text)

    # The new user creates a new list by entering an item
    inputbox = self.browser.find_element_by_id('id_new_item')
    inputbox.send_keys('Buy milk')
    inputbox.send_keys(Keys.ENTER)

    # Francis gets his own url
    francis_list_url = self.browser.current_url

    self.assertRegex(francis_list_url, '/lists/.+')
    self.assertNotEqual(francis_list_url, edith_list_url)

    # Still no trace of old items
    page_text = self.browser.find_element_by_tag_name('body').text
    self.assertNotIn('Buy feathers', page_text)
    self.assertNotIn('and build', page_text)


  def check_for_row_in_list_table(self, row_text):
    table = self.browser.find_element_by_id('id_list_table')
    rows = table.find_elements_by_tag_name('tr')
    self.assertIn(row_text, [row.text for row in rows])


  def test_layout_and_styling(self):
    # User goes to the home page
    self.browser.get(self.server_url)
    self.browser.set_window_size(1024, 768)

    # The input box is centered
    inputbox = self.browser.find_element_by_id('id_new_item')
    self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2,
            512, delta=5)

    # The user creates a new list and sees that the input is centered there too
    inputbox.send_keys('testing\n')
    inputbox = self.browser.find_element_by_id('id_new_item')
    self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2,
            512, delta=5)
