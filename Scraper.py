from bs4 import BeautifulSoup
import requests, json

class Scraper:    
    def getSoup(self, url):
        response = requests.get(url)
        return BeautifulSoup(response.content, 'html.parser')
    
    
    def getInfo(self, soup):
        try:
            title = soup.find("span", {"id" : "productTitle"}).get_text().strip()
        except:
            title = "null"

        try:
            price = soup.find("span", {"id" : "price_inside_buybox"}).get_text().strip()
        except:
            price = "null"
        
        try:
            imagelinks = soup.find("img", {"class" : "a-dynamic-image"}).get("data-a-dynamic-image")
        except:
            imagelinks = []

        try:
            descDiv = soup.find("ul", {"class" : "a-unordered-list a-vertical a-spacing-mini"})
            description = ""
            for child in descDiv.children:
                description += " " + child.get_text().strip()
        except:
            description = "null"
    
        return {
            "t" : title,
            "p" : price,
            "d" : description,
            "i" : imagelinks,
        }



if __name__ == "__main__":
    client = Scraper()

    with open("data.json", "w", encoding='utf-8') as outputf, open("urls.txt", "r", encoding='utf-8') as urlf:
        urls = urlf.read().splitlines()
        total = len(urls)
        
        outputf.write('[\n')
        for i, url in enumerate(urls, start=1):

            soup = client.getSoup(url)
            info = client.getInfo(soup)

            data = {
            "Title" : info.get("t"),
            "Price" : info.get("p"),
            "Desc" : info.get("d"),
            "Images" : info.get("i"),
            "Affiliate Url" : url,
            }
        
            if data:
                json.dump(data, outputf)
                outputf.write(",\n") if i != total else outputf.write("\n")

        outputf.write(']\n')
        
