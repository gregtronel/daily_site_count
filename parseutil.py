import sys
import re
import urllib2, urlparse  
from BeautifulSoup import BeautifulSoup  


"""
    Utility script for parsing information.
    Handles reading/formatting/writing the data files needed for daily_site_count.

"""

def get_soup_from_url(url):
    """
    """
    r = urllib2.urlopen(url).read()
    
    return BeautifulSoup(r)


def visible(element):
    """
    """
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
     
    return True


def parse_static_for_num_items(url):
    """
    """
    soup = get_soup_from_url(url)
    texts = soup.findAll(text=True)
    visible_texts = filter(visible, texts)
    lines=[]
    for line in visible_texts:
        if re.search('\d+ items found$', line):
            lines.append(line)
    try:
        assert len(lines) == 1
        num_items = lines[0].replace(' ','').replace('itemsfound','')
    except AssertionError, e:
        print str(e)
        sys.exit()    
    
    return num_items


def parse_sales(url):
    """
    """
    soup = get_soup_from_url(url)
    children = soup.findAll('li', {"class" : "open"})[0]
    child_urls = []
    num_items = {}
    
    # scrape children urls needed to collect count data for each sales category
    regex = re.compile("\"\/sale.*\d+\"")
    matches = regex.findall(unicode(children))
    for match in matches:
        if match.startswith('"') and match.endswith('"'):
            match = match[1:-1] 
            child_urls.append(urlparse.urljoin(url,match))
    
    # scrape count data from each (child) sales url
    for child_url in child_urls:
        soup = get_soup_from_url(child_url)
        try:
            count_url = soup.findAll('a', {"class" : "topSellingTitle"}, href=True)
            if len(count_url) > 1:
                count_url = count_url[0]['href']
            else:
                count_url = count_url['href']
        except Exception, e:
            print str(e)
            sys.exit()
        count_url = urlparse.urljoin(url, count_url)
        num_items[child_url] = parse_static_for_num_items(count_url)
    
    return num_items

