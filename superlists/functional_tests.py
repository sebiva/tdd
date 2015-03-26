from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

  def setUp(self):
    self.browser = webdriver.Firefox()
    self.browser.implicitly_wait(3)
  def tearDown(self):
    self.browser.quit()

  def test_can_start_a_list_and_retrieve_it_later(self):
    # Open the page
   self.browser.get('http://localhost:8000')

   # Check header
   self.assertIn('To-Do', self.browser.title)
   header_text = self.browser.find_element_by_tag_name('h1').text
   self.assertIn('To-Do', header_text)

   # Test input
   inputbox = self.browser.find_element_by_id('id_new_item')
   self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')
   # Adding something to the todo list
   inputbox.send_keys('Buy food')
   # When enter is pressed, the page should be updated and there should be an item
   # "1: Buy food" in a todo list table
   inputbox.send_keys(Keys.ENTER)
   self.check_for_row_in_list_table('1: Buy food')

   # Another item is added to the list
   inputbox = self.browser.find_element_by_id('id_new_item')
   inputbox.send_keys('Haskell!')
   inputbox.send_keys(Keys.ENTER)

   # Now both items should be shown
   self.check_for_row_in_list_table('1: Buy food')
   self.check_for_row_in_list_table('2: Haskell!')

   self.fail('Finish test!')

  def check_for_row_in_list_table(self, row_text):
    table = self.browser.find_element_by_id('id_list_table')
    rows = table.find_elements_by_tag_name('tr')
    self.assertIn(row_text, [row.text for row in rows])

if __name__ == '__main__':
  unittest.main(warnings='ignore')
