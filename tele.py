import requests
import telegram
import random
import re
from bs4 import BeautifulSoup

token_tele = '492227439:AAF3wwl73zSTGFYyo3QqLA2tqrhKz7gsEa4'
api_key = '35c2d6b4'
imdb_url = 'http://www.imdb.com/search/keyword'


class MoviesBot():
    readyStrings = ['Ready to /help!']
    whatStrings = ['Yes?', 'Hmmm?', 'What do you want?']
    yesStrings = ['I can do that.', 'Be happy to.', 'Sure!']
    noStrings = ["I can't do that.", "You stupid?", "Not right...", "Don't think that I can do that..."]

    options = ["search", "recommend", "tag"]

    helpMessage = """ Hello, fellow user! I'm the Movies Bot!

	Here is what I can do now:
	/search Give me a series/movie title and I'll get information about it for you!
	/tag without parameters gives you the whole list of tags from IMDb
	/tag with a tags from a list gives you a movie-list, based on tags you have chosen before

	Note! All tags have to be written with a delimiter ','!
	"""
    def_url = 'http://www.omdbapi.com/?t=TITLE&apikey=API&plot=short&tomatoes=false&r=json'
    default_url = def_url.replace("API", api_key)

    def __init__(self, token=token_tele):
        self.token = token
        self.bot = telegram.Bot(token)
        try:
            self.lastUpdate = self.bot.getUpdates()[-1].update_id
        except IndexError:
            self.lastUpdate = None

    def startBot(self):
        while True:
            for update in self.bot.getUpdates(offset=self.lastUpdate, timeout=10):
                chat_id = update.message.chat_id
                message = update.message.text

                if message:
                    if "@SelectionCinemaBot" in message:
                        botid = "@SelectionCinemaBot"
                        message = message[:message.find(botid)] + message[message.find(botid) + len(botid):]
                    if (message.startswith('/')):
                        command, _, arguments = message.partition(' ')
                        if command == '/start':
                            self.bot.sendMessage(chat_id=chat_id, text=MoviesBot.readyStrings[0])
                        elif command == '/help':
                            self.bot.sendMessage(chat_id=chat_id, text=MoviesBot.helpMessage)
                        elif command[1:] in MoviesBot.options:
                            noArgument = False
                            if arguments == '':
                                noArgument = True

                            rand = random.randint(0, len(MoviesBot.yesStrings) - 1)
                            self.bot.sendMessage(chat_id=chat_id, text=MoviesBot.yesStrings[rand])

                            if command == '/search':
                                if noArgument:
                                    self.bot.sendMessage(chat_id=chat_id, text="Give me something to search.")
                                else:
                                    msg, poster = self.searchMovie(arguments)
                                    self.bot.sendPhoto(chat_id=chat_id, photo=poster)
                                    self.bot.sendMessage(chat_id=chat_id, text=msg)

                            if command == '/tag':
                                if noArgument:
                                    self.bot.sendMessage(chat_id=chat_id, text=self.getTags(command='/tag'))
                                else:
                                    try:
                                        m = self.searchTag(arguments)
                                        self.bot.sendMessage(chat_id=chat_id, text=m)
                                    except Exception:
                                        rand = random.randint(0, len(MoviesBot.noStrings) - 1)
                                        self.bot.sendMessage(chat_id=chat_id, text=MoviesBot.noStrings[rand])
                    else:
                        rand = random.randint(0, len(MoviesBot.whatStrings) - 1)
                        self.bot.sendMessage(chat_id=chat_id, text=MoviesBot.whatStrings[rand])

                    self.lastUpdate = update.update_id + 1

    def searchMovie(self, title):
        usr_request = MoviesBot.default_url.replace("TITLE", title)
        mov = requests.get(usr_request).json()
        message = mov['Title'] + "\n" + 'Year: ' + mov['Year'] + "\n"
        poster = mov['Poster']
        return message, poster

    def searchTag(self, message):
        chr = ','
        a = message.split(chr)
        msg = str()
        for word in a:
            msg += str(word.rstrip('')) + '%2C'
        msg = msg.strip('%2C')
        msg = msg.replace(' ', '')
        movie_url = imdb_url + '?keywords=' + msg
        movie = requests.get(movie_url).text
        soup = BeautifulSoup(movie, "html.parser")
        m = soup.find('div', class_="lister-list")
        r = self.Parser(m)
        return r

    def getTags(self, command):
        if command == '/tag':
            tags = requests.get(imdb_url).text
            soup = BeautifulSoup(tags, "html.parser")
            m = soup.find('div', class_="widget_nested")
            r = self.Parser(m)
            return r

    def Parser(self, m):
        m = str(m)
        k = str(re.findall('> ?\w+ ?</a>', m))
        k = k.replace('</a>', '')
        k = k.replace('>', '')
        k = k.replace("'", '\n')
        k = k.replace(',', '')
        k = k.rstrip(']')
        k = k.lstrip('[')
        return k
"""
    def PosterID(self, m):
        m = str(m)
        x = str(re.findall('tt\d+/+', m))
        x = x.replace('/', '')
        x = x.replace("'", '')
        x = x.rstrip(']')
        x = x.lstrip('[')
        return x

    def poster(self, m):
        url = 'http://www.omdbapi.com/?i=IMDB&apikey=API'
        url = url.replace('API', api_key)
        l = self.PosterID(m)
        l = l.rstrip(']')
        l = l.lstrip('[')
        l = l.split(',')
        ret_lst = []
        from collections import OrderedDict
        l = list(OrderedDict((element, None) for element in l))
        id = random.randint(1, len(l))
        url = url.replace('IMDB', l[id])
        movie = requests.get(url).json()
        title = movie['Title']
        poster = movie['Poster']
        ret_lst.append(title)
        ret_lst.append(poster)
        ret_lst = list(OrderedDict((element, None) for element in ret_lst))
        return ret_lst
"""
def main():
    moviesbot = MoviesBot()
    moviesbot.startBot()


if __name__ == '__main__':
    main()