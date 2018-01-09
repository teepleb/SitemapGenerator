import global_vars
import webbrowser
import os

class VisualSitemap(object):
    def __init__(self):
        # default values for beginning/ending of HTML file
        self.prefix_html = "<html><head><title>Website Visual Sitemap</title>" \
						   "<link rel=\"stylesheet\" href=\"js/Treant.css\">" \
                           "<link rel=\"stylesheet\" href=\"js/connectors.css\">" \
						   "<script src=\"js/raphael.js\"></script>" \
						   "<script src=\"js/Treant.js\"></script></head><body><div id=\"treemap-chart\"></div><script>"

        self.suffix_html = "</script></body></html>"
        self.js_string = ""

    # build the JS string that runs the tree structure
    def build(self):
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

    # builds HTML file for viewing the tree structure and displays the webpage in default browser
    def save(self):
        with open("index.html", "w") as f:
            f.writelines(self.prefix_html)
            f.writelines(self.js_string)
            f.writelines(self.suffix_html)
            webbrowser.open('file://' + os.path.realpath("index.html"))