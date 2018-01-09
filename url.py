import datetime
import constants

starting_url = constants.starting_url

class URL(object):
	def __init__(self, url):
		# grab the url to save a couple versions (if need)
		self.complete_url = url
		self.clean_url = url.replace(starting_url, '/')

		# general variables just for storing/data purposes (they may never be used but might later on)
		self.crawl_depth = self.clean_url.count("/") - 1
		self.priority = 1.0
		self.change_frequency = "daily"
		self.last_modified = datetime.datetime.now().strftime("%Y-%m-%d")


		# lets find the parent URL using our cleaned up URL for crawl depth
		self.parent = self.get_parent(self.clean_url)

		# boolean to test if the URL has been crawled, this stops redundant looping and saves resources
		self.has_been_crawled = False

	# builds parent URL for reference
	def get_parent(self, url):
		temp = url.split("/")[1:-2]
		temp = "/" + "/".join(temp) + "/"
		return temp

	def load(self):
		pass


if __name__ == '__main__':
	with open("urls.txt", "r") as f:
		for line in f:
			u = URL(line.strip())