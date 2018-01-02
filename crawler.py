import re
import urllib.request as req
import datetime

url_list = []
starting_url = ""
sitemap_xml_file_path = ""


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
		self.priority = 1.0
		self.change_frequency = "daily"

	def append_prev_url(self, url):
		self.prev_urls.append(url)

	def append_next_url(self, url):
		self.next_urls.append(url)

class Crawler(object):
	def __init__(self):
		pass

	def run(self):
		if sitemap_xml_file_path != "No":
			Sitemap().load(sitemap_xml_file_path)
			self.save()
			VisualSitemap().build(url_list)
		else:
			self.crawl(URL(starting_url))
			for u in url_list:
				if u.has_been_crawled == False:
					self.crawl(u)
				if len(url_list) >= 10:
					break
			self.save()
			Sitemap().build(url_list)
			VisualSitemap().build(url_list)

	def crawl(self, u):
		x = req.urlopen(u.full_url).read().decode('utf-8')
		for s in re.findall('href="(.*?)"', x, re.S):
			u.next_urls.append(s)
			u.has_been_crawled = True
			if any(sub in s for sub in ('.css', '.js', '#', '?', 'javascript')):
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
		with open("sitemap.xml", "w") as f:
			f.writelines("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd\">\n")
			for url in url_list:
				f.writelines("  <url>\n")
				f.writelines("    <loc>" + url.full_url + "</loc>\n")
				f.writelines("    <lastmod>" + datetime.datetime.now().strftime("%Y-%m-%d") + "</lastmod>\n")
				f.writelines("    <changefreq>" + url.change_frequency + "</changefreq>\n")
				f.writelines("    <priority>" + str(url.priority) + "</priority>\n")
				f.writelines("  </url>\n")
			f.writelines("</urlset>")

	def load(self, file_path):
		with open(file_path, "r") as f:
			for line in f:
				if "<loc>" in line:
					url_list.append(URL(line.strip()[5:-6]))

class VisualSitemap(object):
	def __init__(self):
		self.prefix_html = "<html><head><title>Website Visual Sitemap</title><link rel=\"stylesheet\" href=\"styles.css\"></head><body>"
		self.suffix_html = "</body></html>"
		self.html_string = ""

	def build(self, urls):
		self.html_string = urls
		self.save()

	def save(self):
		with open("index.html", "w") as f:
			f.writelines(self.prefix_html)
			for value in url_list:
				f.writelines("<p>{0}</p>".format(value.full_url))
			f.writelines(self.suffix_html)

if __name__ == '__main__':
	starting_url = input("Please enter the website URL you're building a sitemap for: >> ")
	sitemap_xml_file_path = input("Do you have a current XML sitemap? Please enter the location now (if no Sitemap, just type No): >> ")
	Crawler().run()
