from bs4 import BeautifulSoup
import urllib.request



def extractJobDescript(url):
    r = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(r)
    letters = soup.find_all("div", {"id": "content"})
    lobby = []
    for element in letters:
        lobby.append(element.get_text())
    return(lobby[0].strip().replace("\n", ""))
