import datetime
import global_vars


class URL(object):
	def __init__(self, url):
		# grab the url to save a couple versions (if need)
		self.complete_url = url
		self.clean_url = url.replace(global_vars.starting_url, "/")

		# general variables just for storing/data purposes (they may never be used but might later on)
		self.crawl_depth = self.clean_url.count("/") - 1
		self.priority = 1.0
		self.change_frequency = "daily"
		self.last_modified = datetime.datetime.now().strftime("%Y-%m-%d")


		# lets find the parent URL using our cleaned up URL for crawl depth
		if self.clean_url != "/":
			self.parent = self.get_parent(self.clean_url)
		else:
			self.parent = "/"

		if self.parent not in global_vars.parent_urls:
			global_vars.parent_urls.append(self.parent)

		# boolean to test if the URL has been crawled, this stops redundant looping and saves resources
		self.has_been_crawled = False

	# builds parent URL for reference later on in tree
	def get_parent(self, url):
		if url.count("/") == 2:
			return self.clean_url
		else:
			temp = url.split("/")[1:-2]
			temp = "/" + "/".join(temp) + "/"
		return temp

	# future function to load urls into data structures via a TXT file
	def load(self):
		pass