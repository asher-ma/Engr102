import requests
import time
from bs4 import BeautifulSoup as bs

class Quote:
    def __init__(self, text, author, tags):
        self.text = text
        self.author = author
        self.tags = tags

class Tag:
    def __init__(self, tag, repetitions):
        self.tag = tag
        self.repetitions = repetitions

class Author:
    def __init__(self, author, repetitions):
        self.author = author
        self.repetitions = repetitions

def main():
    url = "https://quotes.toscrape.com"
    r = requests.get(url)
    soup = bs(r.content, "html.parser")

    quotes = []
    while True:
        time.sleep(0.5)
        relative_url = get_next_url(soup)
        if relative_url is None:
            break
        next_page = url + relative_url

        r = requests.get(next_page)
        soup = bs(r.content, "html.parser")
        quotes.extend(scrape_quotes(soup))

    get_shortest_and_longest(quotes)
    print("----------------------------------")
    get_top_tags(quotes)
    get_top_authors(quotes)

    return

def get_top_authors(quotes):
    #create list to store every author
    authors = []
    for quote in quotes:
        authors.append(quote.author)
    
    #create a list to store the authors as a class, including repetitions
    authors_classes = []        
    for author in authors:
        repetitions = authors.count(author)
        current_author = Author(author, repetitions)
        #only add author to list if it isnt already in (this obviously didnt work)
        if (authors.count(current_author) == 0) & (current_author.repetitions >= 2):
            authors_classes.append(current_author)

    #sort tags list by repetitions value
    sorted_authors = sorted(authors_classes, key = lambda x: x.repetitions, reverse=True)

    for author in sorted_authors:
        print(author.author)
        print(author.repetitions)
    
    return

    
def get_top_tags(quotes):
    #create list to store every group of tags
    tag_groups = []
    for quote in quotes:
        tag_groups.append(quote.tags)
    
    #create list to store every individual tag
    individual_tags = []
    for group in tag_groups:
        for tag in group:
            individual_tags.append(tag)

    #create a list to store the tags as a class, including repetitions
    tags = []        
    for tag in individual_tags:
        repetitions = individual_tags.count(tag)
        current_tag = Tag(tag, repetitions)
        #only add tag to list if it isnt already in (this obviously didnt work)
        if tags.count(current_tag.tag) == 0:
            tags.append(current_tag)

    #sort tags list by repetitions value
    sorted_tags = sorted(tags, key = lambda x: x.repetitions, reverse=True)

    top_10_tags = []
    # add first 10 items to final list
    for tag in sorted_tags[:10]:
        top_10_tags.append(tag.tag)
        top_10_tags.append(tag.repetitions)
        # + ": " + tag.repetitions + " times"

    print(top_10_tags)
    
    return


def get_shortest_and_longest(quotes):
    longest = 0
    shortest = 100000
    longest_quote = ""
    shortest_quote = ""

    for quote in quotes:
        if len(quote.text) > longest:
            longest = len(quote.text)
            longest_quote = quote.text

        if len(quote.text) < shortest:
            shortest = len(quote.text)
            shortest_quote = quote.text
    print("Longest Quote: ", longest_quote," Length: ", longest)
    print("Shortest Quote: ", shortest_quote, " Length: ", shortest)
    return


def get_next_url(soup: bs):
    # find the next url
    list_item = soup.find("li", {"class": "next"})
    if list_item is None:
        return None
    anchor = list_item.find("a")
    url = anchor["href"]

    return url

def scrape_quotes(soup: bs):
    quotes = soup.find_all("div", {"class": "quote"})
    quotes_list = []

    for quote in quotes:
        text = quote.find("span", {"class": "text"}).get_text(strip=True)
        # print(text)
        author = quote.find("small", {"class": "author"}).get_text(strip=True)
        # print(author)
        tags = quote.find_all("a", {"class": "tag"})
        
        tags_text = []
        for tag in tags:
            tags_text.append(tag.get_text(strip=True))
        #print(tags_text)

        quotes_list.append(Quote(text, author, tags_text))
        
        #print("-----------------------------------")

    return quotes_list



if __name__ == "__main__":
    main()