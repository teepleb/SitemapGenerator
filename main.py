from crawler import Crawler
import global_vars

if __name__ == '__main__':
    global_vars.starting_url = input("Please enter the website URL you're building a sitemap for: >> ")
    global_vars.sitemap_xml_file_path = input("Do you have a current XML sitemap? Please enter the location now (if no Sitemap, just type No): >> ")
    Crawler().run()