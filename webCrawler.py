# GoCardless Web Crawler by Lewis Yates

from bs4 import BeautifulSoup
import urlparse
import mechanize

browser = mechanize.Browser()
# initial URL is pushed onto the stack - starting from the GoCardless homepage
response = browser.open("https://gocardless.com/")
soup = BeautifulSoup(response, "html.parser")

# set the starting point for the crawler and init the mechanize browser object (GC.com)
startURL = "https://gocardless.com/"
print "Web Crawler by Lewis Yates\n", "Starting URL:", startURL, "\n", "Status Code:", response.code, "\n", "" # Opening program title with website response code

# create lists for the urls in queue and visited urls
urls = [startURL]
visited = [startURL]

# sets a limit to the number of pages to crawl to find new links
while len(urls) <= 10:
    try:
        browser.open(urls[0])
        urls.pop(0) # url is popped off of the stack at position 0

        for link in browser.links():
            newURL = urlparse.urljoin(link.base_url,link.url) # newURL is appended to BaseURL link

            if newURL not in visited and startURL in newURL: # checks that the same site has not been visited twice
                visited.append(newURL)
                urls.append(newURL)
                print '~~~', newURL, '~~~\n\n' # print newURL https://gocardless.com/newURL

                # newURL is mechanised so that static assets can be pulled from each new link found
                browser = mechanize.Browser()
                newURL = browser.open(newURL)
                soup = BeautifulSoup(newURL, "html.parser")

                # retrieves all the <link> tags and contents of <href> attributes
                for item in soup.find_all('link'):
                    staticCSS = (item.get("href"))
                    print staticCSS, "\n"

                # retrieves all the <img> tags and contents of <src> attributes
                for item in soup.find_all('img'):
                    staticIm = (item.get("src"))
                    print staticIm, "\n"

                # retrieves all the <script> tags and contents of <src> attributes
                for item in soup.find_all("script"):
                        staticJS = item.get("src")
                        print staticJS, "\n"

    # any errors are caught and 'ERROR' is printed, URL is popped off of the stack
    except:
        print ("ERROR")
        urls.pop(0)



