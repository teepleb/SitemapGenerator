import re
import urllib.request as req

url_list = []
starting_url = "https://www.buyandpayhere.com/"

class URL(object):
	def __init__(self, url):
		self.full_url = url
		self.simple_url = None
		self.parent_url = None
		self.has_been_crawled = False
		if url.count("/") > 3:
			indices = [s.start() for s in re.finditer("/", url)]
			self.parent_url = url[indices[url.count("/") - 2]: indices[url.count("/") - 1]]
			self.simple_url = url[indices[url.count("/") - 1]:]
		else:
			self.parent_url = "/"
			self.simple_url = "/"
		self.prev_urls = []
		self.next_urls = []


	def append_prev_url(self, url):
		self.prev_urls.append(url)

	def append_next_url(self, url):
		self.next_urls.append(url)

	def find_index(self, string, delimeter):
		return string.find(delimeter, string.find(delimeter))

	def find_index_tier(self, string, delimeter, tier):
		return string.find(delimeter, string.find(delimeter, tier + 1))

class Crawler(object):
	def __init__(self):
		pass

	def run(self):
		self.crawl(URL(starting_url))
		for u in url_list:
			if u.has_been_crawled == False:
				self.crawl(u)
			if len(url_list) >= 250:
				break
		self.save()

	def crawl(self, u):
		x = req.urlopen(u.full_url).read().decode('utf-8')
		for s in re.findall('href="(.*?)"', x, re.S):
			u.next_urls.append(s)
			u.has_been_crawled = True
			if any(sub in s for sub in ('.css', '.js', '#')):
				continue
			if starting_url not in s:
				continue
			if s not in [url.full_url for url in url_list]:
				url_list.append(URL(s))
	
	def save(self):
		with open('urls.txt', 'w') as f:
			for val in url_list:
				f.writelines(val.full_url + "\n")


class Sitemap(object):
	def __init__(self):
		pass

	def build(self, urls):
		pass

	def save(self):
		pass

	def load(self, file_path):
		pass

class VisualSitemap(object):
	def __init__(self):
		pass

	def build(self, urls):
		pass

	def save(self):
		pass

if __name__ == '__main__':
	Crawler().run()
