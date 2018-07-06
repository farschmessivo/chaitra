from tornado import httpclient, gen
import tornado.ioloop
import tornado.web
from bs4 import BeautifulSoup
from collections import Counter
from re import split

@gen.coroutine
def fetch_url(url):
    try:
        response = yield httpclient.AsyncHTTPClient().fetch(url)
        print("Fetched %s" % url)
        html = response.body if isinstance(response.body, str) \
            else response.body.decode(errors="ignore")
    except Exception as e:
        print("Exception: %s %s" % (e, url))
        return []
    return html

def extract(tags):
    [tag.extract() for tag in tags]

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("main.html", counted_words="", url="https://octopuslabs.com")

    @gen.coroutine
    def post(self):
        url = self.get_argument("url")
        html = yield fetch_url(url)
        body = BeautifulSoup(html, "html.parser").body
        extract(body.find_all('script'))
        extract(body.find_all('style'))
        stripped_strings = [string for string in body.stripped_strings]
        text = []
        for stripped_string in stripped_strings:
            words = split(r'\W+', stripped_string)
            text.extend([word.strip().lower() for word in words if len(word.strip()) > 0])
        counted_words = Counter(text).most_common(100)
        counted_words.sort(key=lambda word: word[0])
        self.render("main.html", counted_words=counted_words, url=url)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    port = 5000
    print("Listening on port %s..." % port)
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()