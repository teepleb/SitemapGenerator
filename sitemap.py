import datetime
import global_vars
from url import URL

class Sitemap(object):
    def __init__(self):
        pass

    # builds a sitemap XML with general settings that can be uploaded to the server
    def build(self):
        with open("sitemap.xml", "w") as f:
            f.writelines("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd\">\n")
            for url in global_vars.url_list:
                f.writelines("  <url>\n")
                f.writelines("    <loc>" + url.complete_url + "</loc>\n")
                f.writelines("    <lastmod>" + datetime.datetime.now().strftime("%Y-%m-%d") + "</lastmod>\n")
                f.writelines("    <changefreq>" + url.change_frequency + "</changefreq>\n")
                f.writelines("    <priority>{0}</priority>\n".format(url.priority))
                f.writelines("  </url>\n")
            f.writelines("</urlset>")

    # loads URLs from a sitemap to be used to create the visual sitemap
    def load(self):
        with open(global_vars.sitemap_xml_file_path, "r") as f:
            for line in f:
                if "<loc>" in line:
                    global_vars.url_list.append(URL(line.strip()[5:-6]))