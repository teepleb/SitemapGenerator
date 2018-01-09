import global_vars
import webbrowser
import os

class VisualSitemap(object):
    def __init__(self):
        # default values for beginning/ending of HTML file
        self.prefix_html = "<html><head><title>Website Visual Sitemap</title>\n" \
                           "<link rel=\"stylesheet\" href=\"js/Treant.css\">\n" \
                           "<link rel=\"stylesheet\" href=\"js/connectors.css\">\n" \
                           "<script src=\"js/raphael.js\"></script>\n" \
                           "<script src=\"js/Treant.js\"></script>\n</head>\n<body>\n<div id=\"treemap-chart\"></div>\n<script>\n"

        self.suffix_html = "</script>\n</body>\n</html>"
        self.js_string = ""

    # build the JS string that runs the tree structure
    def build(self):
        js_prefix = "    var chart_config = {\n" \
                            "        chart: {\n" \
                            "            container: \"#treemap-chart\",\n" \
                            "            levelSeparation: 25,\n" \
                            "            connectors: {" \
                            "                type: \"step\",\n" \
                            "                style: {" \
                            "                    \"stroke-width\": 1\n" \
                            "                }\n" \
                            "            },\n" \
                            "            node: {\n" \
                            "                HTMLclass: \"treemap\"" \
                            "            }\n" \
                            "       },\n" \
                            "       nodeStructure: {" \
                            "           text: { name: \"" + global_vars.starting_url + "\" },\n" \
                            "           connectors: {" \
                            "               style: {\n" \
                            "                   'stroke': '#bbb',\n" \
                            "                   'arrow-end': 'block-wide-long'\n" \
                            "               }\n" \
                            "           },\n" \
                            "       children: [\n"
        js_nodes = ""
        parent_url_count = 1
        parent_url_length = len(global_vars.url_tree)
        for parent_url in sorted(global_vars.url_tree):
            if parent_url == "/":
                continue
            if parent_url_count == parent_url_length:
                js_nodes += "       {\n" \
                                    "           text: { name: \"" + parent_url + "\" },\n" \
                                    "           stackChildren: true,\n" \
                                    "           connectors: {\n" \
                                    "               style: {\n" \
                                    "                   'arrow-end': 'block-wide-long'\n" \
                                    "               }\n" \
                                    "           }"

                if len(global_vars.url_tree[parent_url]) > 0:
                    child_url_length = len(global_vars.url_tree[parent_url])
                    if child_url_length > 5:
                        child_url_length = 5
                    child_url_count = 1
                    js_nodes += ",\n           children: [\n"
                    for child_url in global_vars.url_tree[parent_url]:
                        if child_url_count == child_url_length:
                            if child_url_length < 5:
                                js_nodes += "           { \n" \
                                        "text: { name: \"" + child_url + "\" } }"
                            else:
                                js_nodes += "           { \n" \
                                        "text: { name: \"" + child_url + "\" } },"
                                js_nodes += "           { \n" \
                                        "text: { name: \"..." + str(len(global_vars.url_tree[parent_url]) - child_url_length) + " more pages \" } }"
                            break
                        else:
                            js_nodes += "{ " \
                                    "text: { name: \"" + child_url + "\" } },"
                            child_url_count += 1

                    js_nodes += "]\n"
                js_nodes += "}\n"
            else:
                js_nodes += "       {\n" \
                                    "           text: { name: \"" + parent_url + "\" },\n" \
                                    "           stackChildren: true,\n" \
                                    "           connectors: {\n" \
                                    "               style: {\n" \
                                    "                   'arrow-end': 'block-wide-long'\n" \
                                    "               }\n" \
                                    "           }"

                # need to plan children
                if len(global_vars.url_tree[parent_url]) > 0:
                    child_url_length = len(global_vars.url_tree[parent_url])
                    if child_url_length > 5:
                        child_url_length = 5
                    child_url_count = 1
                    js_nodes += ",\n           children: [ \n"
                    for child_url in sorted(global_vars.url_tree[parent_url]):
                        if child_url_count == child_url_length:
                            if child_url_length < 5:
                                js_nodes += "           { \n" \
                                        "text: { name: \"" + child_url + "\" } }"
                            else:
                                js_nodes += "           { \n" \
                                        "text: { name: \"" + child_url + "\" } },"
                                js_nodes += "           { \n" \
                                        "text: { name: \"..." + str(len(global_vars.url_tree[parent_url]) - child_url_length) + " more pages \" } }"
                            break
                        else:
                            js_nodes += "{ " \
                                    "text: { name: \"" + child_url + "\" } },"
                            child_url_count += 1

                    js_nodes += "]\n"
                
                js_nodes += "},\n"
                
                parent_url_count += 1

        js_suffix = "] }\n};\nnew Treant( chart_config );\n" 
        self.js_string = js_prefix + js_nodes + js_suffix
        self.save()

    # builds HTML file for viewing the tree structure and displays the webpage in default browser
    def save(self):
        with open("index.html", "w") as f:
            f.writelines(self.prefix_html)
            f.writelines(self.js_string)
            f.writelines(self.suffix_html)
            #webbrowser.open('file://' + os.path.realpath("index.html"))