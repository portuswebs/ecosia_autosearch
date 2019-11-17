import urllib.request
import threading
import timeit
import csv
import random
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def read_url(self, url):
        with urllib.request.urlopen(url) as page:
            page.read()

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in filter(lambda attr : attr[0] == "class" and (attr[1] == "result-title result-title-ad" or attr[1] == "result-title result-title-sidebar-ad"), attrs):
                for attr in filter(lambda attr : attr[0] == "href", attrs):
                    self.read_url(attr[1])
                    break
            if (lambda attr : attr[0] == "class" and attr[1] == "title" in attrs):
                pass
            return

if __name__ == "__main__":
    start = timeit.default_timer()
    list_actions = []
    list_adjectives_1 = []
    list_adjectives_2 = []
    list_services = []
    list_products = []

    with open('list_actions.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count >= 2:
                # print(row)
                if row[0] != "":
                    list_actions.append(row[0])
                if row[1] != "" :
                    list_adjectives_1.append(row[1])
                if row[2] != "" :
                    list_adjectives_2.append(row[2])
                if row[3] != "" :
                    list_services.append(row[3])
                if row[4] != "" :
                    list_products.append(row[4])
            line_count += 1
        # print(f'Processed {line_count} lines.')

    result = {
    1: lambda x, y: random.choice(list_actions) + "+" if x else "" + random.choice(list_adjectives_1) + "+" if y else "",
    2: lambda x, y: random.choice(list_actions) + "+" if x else "" + random.choice(list_adjectives_2) + "+" if y else "",
    3: lambda x, y: random.choice(list_adjectives_1) + "+" if x else "",
    }[random.randint(1, 3)](random.randint(0, 2) == 0, random.randint(0, 2) == 0) + random.choice(list_products)
    print ("https://www.ecosia.org/search?q=" + result) 

    contents = urllib.request.urlopen("https://www.ecosia.org/search?q=" + result).read()
    #contents = urllib.request.urlopen("https://www.ecosia.org/search?q=chocolate").read()
    parser = MyHTMLParser()
    parser.feed("".join(map(chr, contents)))
    stop = timeit.default_timer()

    print('Time: ', stop - start)