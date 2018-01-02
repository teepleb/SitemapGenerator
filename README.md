# Visual Sitemap Generator

A visual sitemap generator is pivotal to understanding how your website is structured. In many cases people tend to just throw garbage on top of garbage and it reduces your ability to increase your crawl budget. In my current position as an SEO Analyst we often review site structure and ways to improve how the search engines see our website. This project was built specifically for my current position but is built to be usable for others. It is open source and please use at your own discretion.

Please note, there is no throttling currently in the program. This will crawl your website(s) with no limitations.

### Python Packages Used

- re
- urllib.request
- datetime

### Project Roadmap (My Todo List)

- URL Management
	- Build Objects for URL Properties
	- Build URL List of Website to TXT
- XML Sitemaps
	- Save/Build XML Version
	- Upload via FTP to Server (possible)
	- Ping Search Engines Accordingly (possible)
- Visual Sitemap
	- Build From Crawl
	- Build From XML Sitemap
	- Build From TXT File List of URLs
	- Export to HTML/CSS
- Crawl Speed Limitations
- User Settings (possible)
	- Page Speed Limits
	- Crawl Speed
	- Folder Limits (Crawl Various Subdirectories)