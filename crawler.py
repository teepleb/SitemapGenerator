import re
import urllib.request as req
import datetime
import webbrowser
import os
import global_vars
from url import URL
from sitemap import Sitemap


class Crawler(object):
    def __init__(self):
        pass

    def run(self):
        if global_vars.sitemap_xml_file_path != "No":
            Sitemap().load()
            self.save()
            self.build_children()
            VisualSitemap().build(global_vars.url_list)
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
            VisualSitemap().build(global_vars.url_list)

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
        for url in global_vars.parent_urls:
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
            webbrowser.open('file://' + os.path.realpath("index.html"))



if __name__ == '__main__':
    global_vars.starting_url = input("Please enter the website URL you're building a sitemap for: >> ")
    global_vars.sitemap_xml_file_path = input("Do you have a current XML sitemap? Please enter the location now (if no Sitemap, just type No): >> ")
    Crawler().run()
