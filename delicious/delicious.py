import urllib2 as urllib
import base64


def main() :
    webuser = "Konstantin_Grigoriev"
    webpass = "parabolla_84"
    #params = urllib.urlencode({ "user" : "Konstantin_Grigoriev", "pass" : "parabolla_84" }) 
    #url = urllib.urlopen("https://api.del.icio.us/v1/tags/get", params)
    url = "https://api.del.icio.us/v1/tags/get"
    request =  urllib.Request(url) 

    if webuser: 
        base64string = base64.encodestring('%s:%s' % (webuser, webpass))[:-1]
        request.add_header("User-Agent", "my-test-app") 
        request.add_header("Authorization", "Basic %s" % base64string) 

    htmlfile = urllib.urlopen(request) 
    response = htmlfile.read()
    print response
    htmlfile.close()

from pydelicious import DeliciousAPI

def main1():
    webuser = "Konstantin_Grigoriev"
    webpass = "parabolla_84"
    api = DeliciousAPI(webuser, webpass)
    print api.bundles_all()
    
from Tkinter import *

class DiliciousApplication(Frame):
    def __init__(self, master=None):
        webuser = "Konstantin_Grigoriev"
        webpass = "parabolla_84"
        self.api = DeliciousAPI(webuser, webpass)
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.search = Entry(self)
        self.search.bind("<KeyPress-Return>", self.on_search_changed)
        self.search.grid()
        self.list = Listbox(self)
        self.refresh_list()
        self.list.grid()
        self.quitButton = Button(self, text="Quit", command=self.quit)
        self.quitButton.grid()
    
    def refresh_list(self, tag=""):
        print "refreshing list for tag : ", tag
        self.list.delete(0, self.list.size())
        posts = self.api.posts_all(tag=tag, results=20)["posts"]
        print "posts found : ", len(posts)
        for post in posts:
            self.list.insert(END, post["description"])       
    
    def on_search_changed(self, event):
        print "char : ", event.char
        print "search : ", self.search.get()
        self.refresh_list(self.search.get())

def main2():
    app = DiliciousApplication()
    app.mainloop()      
    
if __name__ == '__main__':
    main2()
