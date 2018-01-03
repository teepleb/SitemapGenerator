import re
import urllib.request as req
import datetime
import webbrowser
import os

url_list = []
starting_url = ""
sitemap_xml_file_path = ""
parent_urls = []
parent_filter = ""
children_temp = []
longest_url_count = 3

class URL(object):
    def __init__(self, url):
        self.full_url = url
        self.simple_url = url
        self.parent_url = None
        self.has_been_crawled = False
        if url.count("/") > 4:
            indices = [s.start() for s in re.finditer("/", url)]
            self.parent_url = url[indices[2]: indices[url.count("/") - 1]]
            if url[indices[2]: indices[url.count("/") - 1]] not in parent_urls:
                parent_urls.append(url[indices[2]: indices[url.count("/") - 1]])
        elif url.count("/") == 3:
            self.parent_url = "/"
        else:
            indices = [s.start() for s in re.finditer("/", url)]
            if url[indices[url.count("/") - 2]: indices[url.count("/") - 1]] not in parent_urls:
                parent_urls.append(url[indices[url.count("/") - 2]: indices[url.count("/") - 1]])
            self.parent_url = url[indices[url.count("/") - 2]: indices[url.count("/") - 1]]

        self.priority = 1.0
        self.change_frequency = "daily"


class Crawler(object):
    def __init__(self):
        pass

    def run(self):
        if sitemap_xml_file_path != "No":
            Sitemap().load(sitemap_xml_file_path)
            self.save()
            self.build_children()
            VisualSitemap().build(url_list)
        else:
            self.crawl(URL(starting_url))
            for u in url_list:
                if u.count("/") > longest_url_count:
                    longest_url_count = u.count("/")
                if not u.has_been_crawled:
                    self.crawl(u)
                if len(url_list) >= 50:
                    break
            self.save()
            Sitemap().build(url_list)
            self.build_children()
            VisualSitemap().build(url_list)

    def crawl(self, u):
        x = req.urlopen(u.full_url).read().decode('utf-8')
        for s in re.findall('href="(.*?)"', x, re.S):
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

    def build_children(self):
        pass


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
        self.prefix_html = "<html><head><title>Website Visual Sitemap</title>" \
						   "<link rel=\"stylesheet\" href=\"js/Treant.css\">" \
                           "<link rel=\"stylesheet\" href=\"js/connectors.css\">" \
						   "<script src=\"js/raphael.js\"></script>" \
						   "<script src=\"js/Treant.js\"></script></head><body><div id=\"treemap-chart\"></div><script>"

        self.suffix_html = "</script></body></html>"
        self.js_string = ""

    def build(self, urls):
        js_prefix = "var chart_config = {" \
                            "chart: {" \
                            "container: \"#treemap-chart\"," \
                            "levelSeparation: 25," \
                            "rootOrientation: \"WEST\"," \
                            "nodeAlign: \"BOTTOM\"," \
                            "connectors: {" \
                            "type: \"step\"," \
                            "style: {" \
                            "\"stroke-width\": 1" \
                            "}" \
                            "}," \
                            "node: {" \
                            "HTMLclass: \"treemap\"" \
                            "}" \
                            "}," \
                            "nodeStructure: {" \
                            "text: { name: \"Homepage ( / )\" }," \
                            "connectors: {" \
                            "style: {" \
                            "'stroke': '#bbb'," \
                            "'arrow-end': 'block-wide-long'" \
                            "}" \
                            "}," \
                            "children: ["

        # parent
        """

                    {
                        text: { name: "dealers/" },
                        stackChildren: true,
                        connectors: {
                            style: {
                                'stroke': '#8080FF',
                                'arrow-end': 'block-wide-long'
                            }
                        },
                        children: [
                            {
                                text: {name: "dealers/west_virginia/"}
                            },
                            {
                                text: {name: "dealers/michigan/"}
                            }
                        ]
                    },

        """
        js_nodes = ""
        for url in parent_urls:
            if url.count("/") < 2:
                js_nodes += "{" \
                            "text: { name: \"" + url + "\" }," \
                            "stackChildren: true," \
                            "connectors: {" \
                            "style: {" \
                                "'arrow-end': 'block-wide-long'" \
                            "}" \
                            "}" \
                            "},"

        js_suffix = "]} };new Treant( chart_config );"
        self.js_string = js_prefix + js_nodes + js_suffix
        self.save()

    def save(self):
        with open("index.html", "w") as f:
            f.writelines(self.prefix_html)
            f.writelines(self.js_string)
            f.writelines(self.suffix_html)
            f.writelines(self.suffix_html)
            webbrowser.open('file://' + os.path.realpath("index.html"))



if __name__ == '__main__':
    starting_url = input("Please enter the website URL you're building a sitemap for: >> ")
    sitemap_xml_file_path = input("Do you have a current XML sitemap? Please enter the location now (if no Sitemap, just type No): >> ")
    Crawler().run()
