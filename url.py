import datetime
import global_vars

class URL(object):
	def __init__(self, url):
		# grab the url to save a couple versions (if need)
		self.complete_url = url
		self.clean_url = url.replace(global_vars.starting_url, "/")

		#verify there is a trailing slash at the end of the url
		if self.clean_url[-1:] != "/":
			self.clean_url += "/"

		# general variables just for storing/data purposes (they may never be used but might later on)
		self.crawl_depth = self.clean_url.count("/") - 1

		if self.crawl_depth > global_vars.crawl_depth:
			global_vars.crawl_depth = self.crawl_depth

		self.priority = 1.0
		self.change_frequency = "daily"
		self.last_modified = datetime.datetime.now().strftime("%Y-%m-%d")


		# lets find the parent URL using our cleaned up URL for crawl depth
		if self.clean_url != "/":
			self.parent = self.get_parent(self.clean_url)
		else:
			self.parent = "/"

		if self.parent not in global_vars.parent_urls and self.parent != "/":
			global_vars.parent_urls.append(self.parent)

		# boolean to test if the URL has been crawled, this stops redundant looping and saves resources
		self.has_been_crawled = False

		self.add_to_tree(self.clean_url)

	# builds parent URL for reference later on in tree
	def get_parent(self, url):
		if url.count("/") == 2:
			return url
		elif url.count("/") > 2:
			self.add_to_tree_parent_known(url, url.split("/"))
			temp = url.split("/")[1:-2]
			temp = "/" + "/".join(temp) + "/"
			return temp
		else:
			temp = url.split("/")[1:-2]
			temp = "/" + "/".join(temp) + "/"
			return temp

	# adds to parent/child relationship tree
	def add_to_tree(self, url):
		if self.parent not in global_vars.url_tree.keys():
			global_vars.url_tree[self.parent] = []
		else:			
			global_vars.url_tree[self.parent].append(url.replace(self.parent, "/"))

	def add_to_tree_parent_known(self, url, parent):
		print("URL: {0} - Parent: {1}".format(url, parent))

	# future function to load urls into data structures via a TXT file
	def load(self):
		pass