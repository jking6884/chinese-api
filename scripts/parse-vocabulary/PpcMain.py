from pprint import pprint

from PpcDict import PpcDict

class PpcMain:

    def __init__(self):
        self.dictCount = 1
        self.altView = 0
        self.enabled = 0
        self.loadDictionary()


    def loadDictionary(self):
        self.dict = PpcDict()

        return True

    def search(self, text):
        showMode = 0
        m = showMode
        e = None

        while True:
            e = self.dict.wordSearch(text)
            pprint(e)
            if showMode == m:
                break