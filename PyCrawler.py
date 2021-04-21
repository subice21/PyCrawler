import requests
from bs4 import BeautifulSoup
import concurrent.futures
import time
import re

START_URL = "https://www.websitetoCrawl.com/"
MAX_THREADS = 30
LINKS = []

def download_url(url): 
    global links,LINKS
    resp = requests.get(url)
    data = BeautifulSoup(resp.content, "html.parser")
    stories = data.find_all("a")
    links = [x["href"] for x in stories if START_URL in x["href"]]
     
    for l in links:
        x = re.search("https://www.reddit.com/",l)
        z = re.search("https://www.stumbleupon.com/",l) 
        y = re.search("https://www.facebook.com/",l)
        t = re.search("https://pinterest.com/",l)
        if (z or x or y or t ):
            links.remove(l)

    LINKS += links       
    time.sleep(0.25)

def unique(list1):
    unique_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list
    
def save_link(linkz):
    title = "zaz.html"
    for i in linkz:
        with open(title, "a") as fh:
            fh.write("<a href='" + i + "'>" + i.replace(START_URL, "") + "</a><br>" )

def download_data(url): 
    LINKS_magnet = []
    linkTitleArr = []
    imgarr = []
    about_data = []

    resp = requests.get(url)
    data = BeautifulSoup(resp.content, "html.parser")
    
    #LINKS_magnet
    stories = data.find_all("a")
    magnet = [x["href"] for x in stories if "magnet:?xt" in x["href"]] 
    LINKS_magnet += magnet
    
    #Title
    linkTitle = data.find_all("h2")
    for child in linkTitle:
        #print(child.contents)
        for x in child.contents[0]:
            linkTitleArr = x

    #img = data.find_all("img")
    #imgar = [x["src"] for x in img if "" in x["src"]] 
    #print(imgarr)
    #imgarr +=imgar
    
    #game_area_description
    about = data.find_all(id="game_area_description")
    for child in about:
        for x in child.contents[1]:
           if len(x) > 10:
            print(X)   
            about_data = x
           

    time.sleep(0.25)


def threads(function, urls):
    threads = min(MAX_THREADS, len(urls))   
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(function, urls)

def main():
    t0 = time.time()
    print(f"going to Website: {START_URL}")
    download_url(START_URL)
    uniList = unique(links)
    print(f"{len(uniList)} links crawled @ first sweep")
    threads(download_url,uniList)
    unique_LINKS = unique(LINKS)
    save_link(unique_LINKS)
    t1 = time.time()
    print(f"{len(unique_LINKS)} links crawled @ 2nd sweep , and save to zaz.html")
    print(f"it took: {t1-t0} seconds")

    t0 = time.time()
    threads(download_data,unique_LINKS)
    t1 = time.time()
    print(f"{t1-t0} seconds to download {len(unique_LINKS)} ")

main()

