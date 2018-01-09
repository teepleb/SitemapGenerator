import re
import urllib.request as req
import global_vars
from url import URL
from sitemap import Sitemap
from visual_sitemap import VisualSitemap


class Crawler(object):
    def __init__(self):
        pass

    def run(self):
        if global_vars.sitemap_xml_file_path != "No":
            Sitemap().load()
            self.save()
            self.build_children()
            VisualSitemap().build()
        else:
            self.crawl(URL(global_vars.starting_url))
            for u in global_vars.url_list:
                if not u.has_been_crawled:
                    self.crawl(u)
                if len(global_vars.url_list) >= 50:
                    break
            self.save()
            Sitemap().build()
            self.build_children()
            VisualSitemap().build()

    def crawl(self, u):
        x = req.urlopen(u.complete_url).read().decode('utf-8')
        for s in re.findall('href="(.*?)"', x, re.S):
            u.has_been_crawled = True
            if any(sub in s for sub in ('.css', '.js', '#', '?', 'javascript')):
                continue
            if global_vars.starting_url not in s:
                continue
            if s not in [url.complete_url for url in global_vars.url_list]:
                global_vars.url_list.append(URL(s))

    def save(self):
        with open('urls.txt', 'w') as f:
            for val in global_vars.url_list:
                f.writelines(val.complete_url + "\n")

    def build_children(self):
        pass