import requests
from bs4 import BeautifulSoup
import supybot.conf as conf
import supybot.utils as utils
from supybot.commands import *
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
      
class KnowYourMeme(callbacks.Plugin):
    """
    Looks up memes on the website KnowYourMeme
    """

    def meme(self, irc, msg, args, searchTerm):
        """
        [<searchTerm>]
        
        Searches up a meme. If <searchTerm> is provided, it searches a specific meme. Otherwise, it chooses a random one.
        """
        if(not searchTerm):
            page = "http://knowyourmeme.com/random"
        else:
            for i in searchTerm:  #formatting search term
            if i == " ":
                i = "+"
                searchedURL = "http://knowyourmeme.com/search?q=" + searchTerm # making the search url
                resultsPage = requests.get(searchedURL, headers=_HEADERS) 
                soup = BeautifulSoup(resultsPage.content, 'html.parser')  
                listOfElements = soup.findAll("a", href=True)  #Finding all links in the results page
                page = "http://knowyourmeme.com" + listOfElements[140]['href']  #Picking first meme

        url = requests.get(page, headers=_HEADERS) #opening the final page
        soup = BeautifulSoup(url.content, 'html.parser')
        title = soup.find('meta', attrs={"property": "og:title"})['content'] #getting title info
        finalURL = soup.find('meta', attrs={"property": "og:url"})['content'] #getting the page url
        irc.reply(f"{title}, {finalURL}")
    meme = wrap(meme, [optional('searchTerm')])

    def memepic(self, irc, msg, args):
        """
        Gets a meme image from KnowYourMeme.
        """
        url = "http://knowyourmeme.com/photos/random"
        page = requests.get(url, headers=_HEADERS)  # requesting code
        print(page.url)
        irc.reply(catURL)
    memepic = wrap(memepic)
    
      
Class = KnowYourMeme