from requests_html import HTMLSession

url = 'https://www.thomasnet.com/nsearch.html?cov=NA&what=digital&heading=26096008'

s = HTMLSession()
r = s.get(url)
# html.find('div.b-sidebar.col-lg-2.pr-20.h-hidden__md-down
link = r.html.find('', first=True)
print(link.absolute_links[1])