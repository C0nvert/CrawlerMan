# Manga Web Scraper CLI for different Sources
# Created by Alexander Zejnalov 26.09.2020

import os
import sys
import requests as r
from bs4 import BeautifulSoup
from tqdm import tqdm
import argparse


def sources(name):
    # Request data from desired url

    if  name == "onepiece":
        base_url = "https://w16.read-onepiece.com/manga/one-piece-chapter-"
        mangaName = "One Piece"
    elif name == "dnk":
        base_url = "https://domesticgirlfriend.net/manga/domestic-na-kanojo-chapter-"
        mangaName = "Domestic na Kanojo"
    elif name == "boruto":
        base_url = "https://read-boruto-manga.com/manga/boruto-chapter-"
        mangaName = "Boruto"
    elif name == "snk":
        base_url = "https://readshingekinokyojin.com/manga/shingeki-no-kyojin-chapter-"
        mangaName = "Shingeki No Kyojin"
    elif name == "snkcol":
        base_url = "https://ww7.readsnk.com/chapter/shingeki-no-kyojin-colored-chapter-"
        mangaName = "Shingeki No Kyojin Color"
        print("There are no colored Chapters from Chapter 2-49!")
        raw_input("Press Enter to continue...")
    return [base_url,mangaName]

def soap():
    
    if sourceslist[1] == "Shingeki No Kyojin Color":
        request = r.get(sourceslist[0]+ str('{num:03d}'.format(num=args.min)) + "/")
        soup = BeautifulSoup(request.text, "html.parser")
    else:
        request = r.get(sourceslist[0] + str(args.min) + "/")
        soup = BeautifulSoup(request.text, "html.parser")

    # source the images which will be downloaded
    x = soup.findAll('img')
    links = []
    modifyLinks = []

    for img in x:
        links.append(img['src'])

    
    # Check if List is Empty
    if len(links) != 0:
        # Check if Image URL is obscured, if it is, cut the String to get an Image URL
        try:
            for s in links:
                cuttedString = s.split("url=", 1)[1]
                cuttedString = cuttedString.rsplit('&container', 1)[0]
                modifyLinks.append(cuttedString)
                links = modifyLinks
        except Exception as e:
            print(e.message)
    else:
        print('Chapter '+str(args.min)+' is Empty!\n\nCheck the following Source in your Web Browser: ' +
              str(sourceslist[0]+str('{num:03d}'.format(num=args.min)))+'\n')
        args.min += 1
        links=soap()
    return links

def mkdir(chapter):
     path = sourceslist[1]+"/"+str(chapter)
     isDir = os.path.isdir(path)
     try:
        os.mkdir(sourceslist[1])
     except OSError:
        pass
     if isDir:
        print('\nDirectory is already available. Skipping folder creation..\n')
        return path
     else:
        print('Creating a directory for Chapter ' +
              str(chapter) + '\n' + '')
        os.mkdir(path)
        return path

def genImage(path, links):
    try:
        # Generate and save images
        print('Starting Download... \n')
        for index, img_link in enumerate(links):
            for i in tqdm(range(1)):
                img_data = r.get(img_link).content
                with open(path + "/" + str(index + 1) + '.png', 'wb+') as f:
                    f.write(img_data)

        print('\n\nChapter ' + str(args.min) + ' completed')
        args.min += 1
        return args.min

    except Exception as e:
        print(e.message)
        sys.exit(1)


def main():
    while args.min <= args.max:
        links = soap()
        path = mkdir(args.min)
        args.min = genImage(path, links)
        

if __name__ == "__main__":
    # CLI args
    parser = argparse.ArgumentParser()
    parser.add_argument('-min', type=int, required=False, default=1,
                        help='Chapter to Start from\nDefault Value[1]\n')
    parser.add_argument('-max', type=int, required=False, default=276,
                        help='Chapter to Start from\nDefault Value[276]\n')
    parser.add_argument('-name', type=str, required=False,
                        help='Download Manga\nChoose from One Piece, Domestic na Kanojo, Boruto, Shingeki No Kyojin(Colored)\nArguments:(onepiece, dnk, boruto, snk, snkcol)')

    args = parser.parse_args()
    sourceslist = []
    sourceslist = sources(args.name)
    links = []
    path = ''
    main()
   
 

    
