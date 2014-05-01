import unittest
import index
import slides_parser
import os
from bs4 import BeautifulSoup

class TestSlidesParser(unittest.TestCase):
	def test_parser(self):
		pass

	def test0(self):
		# Ensure test images dir exists
		test_path = os.path.join(os.getcwd(), '..', 'Images')
		self.assertIsNotNone(test_path)
		
		# Run code
		i_to_h = slides_parser.image_to_html(test_path, "dark")
		i_to_h = slides_parser.image_to_html(test_path, "light")
		i_to_h.image_retrieve()

		# Make sure album path was created
		album_path = os.path.join(test_path, "album")
		self.assertTrue(os.access(album_path, os.R_OK))	

		# Make sure index.html exists and doesn't have any <ja> tags
		index_file = open(os.path.join(test_path, "album", "index.html"), 'r')
		soup = BeautifulSoup(index_file)
		index_file.close()
		self.assertEqual(0, len(soup.find_all('ja')))

		# Make sure a slide exists and doesn't have any <ja> tags
		slide_file = open(os.path.join(test_path, "album", "slides", "cards.html"), 'r')
		soup = BeautifulSoup(slide_file)
		slide_file.close()
		self.assertEqual(0, len(soup.find_all('ja')))

if __name__=="__main__":
	unittest.main()