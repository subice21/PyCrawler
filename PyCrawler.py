import requests
from bs4 import BeautifulSoup
import concurrent.futures
import time
import re

START_URL = "https://crotorrents.com/"
MAX_THREADS = 30
LINKS = []
links = []

def download_url(url): 
    global links,LINKS
    resp = requests.get(url)
    data = BeautifulSoup(resp.content, "html.parser")
    stories = data.find_all("a")
    links = [x["href"] for x in stories if "https://crotorrents.com/" in x["href"]]
     
    for l in links:
        x = re.search("https://www.reddit.com/",l)
        z = re.search("https://www.stumbleupon.com/",l) 
        y = re.search("https://www.facebook.com/",l)
        t = re.search("https://pinterest.com/",l)
        if (z or x or y or t ):
            print("found one outsider")
            links.remove(l) 
    LINKS += links
        
    time.sleep(0.25)

def unique(list1):
    unique_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list


def download_newLinks(story_urls):
    threads = min(MAX_THREADS, len(story_urls))
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(download_url, story_urls)
     
def save_link(linkz):
    title = "zaz.html"
    for i in linkz:
        with open(title, "a") as fh:
            fh.write("<a href='" + i + "'>" + i + "</a><br>" )
        
    time.sleep(0.25)

def main():
    t0 = time.time()
    download_url(START_URL)
    uniList = unique(links)
    print(len(uniList))

    download_newLinks(uniList)
    
    unique_LINKS = unique(LINKS)
    save_link(unique_LINKS)
    t1 = time.time()
    print(f"{t1-t0} seconds to download {len(unique_LINKS)} ")

main()
