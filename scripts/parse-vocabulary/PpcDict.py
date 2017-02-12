from pprint import pprint
import codecs

class PpcDict:
    def __init__(self):
        self.config = {}
        self.wordDict = None
        self.wordIndex = None
        self.loadDictionary()

    def loadDictionary(self):
        self.wordDict = codecs.open('data/dict.dat', 'r', encoding="utf-8").read()
        self.wordIndex = codecs.open('data/dict.idx', 'r', encoding="utf-8").read()

    def wordSearch(self, word):
        entryobj = {'data': [], 'matchLen': 0}

        rawentries = []

        while len(word) > 0:
            hits = self.indexSearch(self.wordIndex, word)

            for idx, hit in enumerate(hits):
                end = self.wordDict.index(u"\n", hit) - 1
                entryline = self.wordDict[hit:end]
                rawentries.append(entryline)

            word = word[0:len(word) - 1]

        for idx, rawentry in enumerate(rawentries):
            # set highlight length to longest match
            hanziLen = rawentry.find(" ")
            if hanziLen > entryobj['matchLen']:
                entryobj['matchLen'] = hanziLen

            entryobj['data'].append(rawentry)

        return entryobj

    def indexSearch(self, book, word):
        results = []
        hanzisep = u"\u30FB"
        indexsep = u"\uFF1A"

        # find all hits for traditional characters
        hit = book.find(u"\n" + word + hanzisep)
        while hit != -1:
            start = book.find(indexsep, hit) + 1
            end = book.find(u"\n", start)
            indexString = book[start:end]
            results.append(int(indexString))

            hit = book.find(u"\n" + word + hanzisep, hit+1)

        # find all hits for simplified characters
        hit = book.find(hanzisep + word + indexsep)
        while hit != -1:
            start = book.find(indexsep, hit) + 1
            end = book.find("\n", start)
            indexString = book[start:end]
            results.append(int(indexString))

            hit = book.find(hanzisep + word + indexsep, hit+1)

        results.sort()
        uniqueResults = set(results)

        return uniqueResults

    def parseCEdictLine(self, entry):
        space1 = entry.find(" ")
        space2 = entry.find(" ", space1 + 1)
        bracket1 = entry.find("[")
        bracket2 = entry.find("]")
        slash1 = entry.find("/")
        slash2 = entry.find("/")

        params = {}

        params.trad = entry[0:space1]
        params.simp = entry[space1:space2 - space1 - 1]
        params.pinyin = self.parsePinyin(entry[bracket1:bracket2 - bracket1 - 1])
        params.definition = entry[(slash1 + 1):(slash2 - slash1 - 1)]

        return params

    def parsePinyin(self, pinyin):
        # pinyin info
        _a = [u"\u0101", u"\u00E1", u"\u01CE", u"\u00E0", u"a"];
        _e = [u"\u0113", "\u00E9", u"\u011B", u"\u00E8", u"e"];
        _i = [u"\u012B", "\u00ED", u"\u01D0", u"\u00EC", u"i"];
        _o = [u"\u014D", "\u00F3", u"\u01D2", u"\u00F2", u"o"];
        _u = [u"\u016B", "\u00FA", u"\u01D4", u"\u00F9", u"u"];
        _v = [u"\u01D6", "\u01D8", u"\u01DA", u"\u01DC", u"\u00FC"];
        ztone = [u'', '\u02CA', u'\u02C7', u'\u02CB', u'\u30FB'];

        result = {'tones': [], 'tonemarks': [], 'zhuyin': [], 'tonenums': []}
        zhuyin = []
        tonenums = []

        pinyin = pinyin.split(" ")
        for idx, item in enumerate(pinyin):
            pin = item.replace('u:', "\u00FC")
            tone = 4

            tonenums.append(pin)

            if pin.find(1) != -1:
                tone = 0
            elif pin.find(2) != -1:
                tone = 1
            elif pin.find(3) != -1:
                tone = 2
            elif pin.find(4) != -1:
                tone = 3

            result.tones.append(tone + 1)

            prepin = pin[0:len(pin) - 1]
            indx = self.pinyinref.find(prepin.lower())
            zhuyin.append(self.zhuyin[indx] + ztone[tone])

            if pin.find('a') != -1:
                pin = pin.replace("a", _a[tone])
            elif pin.find("e") != -1:
                pin = pin.replace("e", _e[tone])
            elif pin.find("ou") != -1:
                pin = pin.replace("ou", _o[tone])
            else:
                for idx2, item2 in enumerate(pin):
                    if(self.isVowel(item2)):
                        if item2 == "i":
                            pin = pin.replace("i", _i[tone])
                        elif item2 == "o":
                            pin = pin.replace("o", _o[tone])
                        elif item2 == "u":
                            pin = pin.replace("u", _u[tone])
                        elif item2 == u"\u00FC":
                            pin = pin.replace(u"\u00FC", _v[tone])
            item = pin[0:len(pin) - 1]
        result['tonemarks'] = pinyin.join(" ")
        result['zhuyin'] = zhuyin.join(" ")
        result['tonenums'] = tonenums.join(" ")
        return result

    def isVowel(self, char):
        return char.lower() in 'aeiou'

    def pinyinref(self): return [
        'a', 'ai', 'an', 'ang', 'ao', 'ba', 'bai', 'ban', 'bang', 'bao', 'bei', 'ben', 'beng', 'bi', 'bian', 'biao',
        'bie',
        'bin', 'bing', 'bo', 'bu', 'ca', 'cai', 'can', 'cang', 'cao', 'ce', 'cen', 'ceng', 'cha', 'chai', 'chan',
        'chang',
        'chao', 'che', 'chen', 'cheng', 'chi', 'chong', 'chou', 'chu', 'chua', 'chuai', 'chuan', 'chuang', 'chui',
        'chun',
        'chuo', 'ci', 'cong', 'cou', 'cu', 'cuan', 'cui', 'cun', 'cuo', 'da', 'dai', 'dan', 'dang', 'dao', 'de', 'deng',
        'di', 'dian', 'diang', 'diao', 'die', 'ding', 'diu', 'dong', 'dou', 'du', 'duan', 'dui', 'dun', 'duo', 'e',
        'ei',
        'en', 'er', 'fa', 'fan', 'fang', 'fei', 'fen', 'feng', 'fo', 'fou', 'fu', 'ga', 'gai', 'gan', 'gang', 'gao',
        'ge',
        'gei', 'gen', 'geng', 'gong', 'gou', 'gu', 'gua', 'guai', 'guan', 'guang', 'gui', 'gun', 'guo', 'ha', 'hai',
        'han',
        'hang', 'hao', 'he', 'hei', 'hen', 'heng', 'hong', 'hou', 'hu', 'hua', 'huai', 'huan', 'huang', 'hui', 'hun',
        'huo',
        'ji', 'jia', 'jian', 'jiang', 'jiao', 'jie', 'jin', 'jing', 'jiong', 'jiu', 'ju', 'juan', 'jue', 'jun', 'ka',
        'kai',
        'kan', 'kang', 'kao', 'ke', 'ken', 'keng', 'kong', 'kou', 'ku', 'kua', 'kuai', 'kuan', 'kuang', 'kui', 'kun',
        'kuo',
        'la', 'lai', 'lan', 'lang', 'lao', 'le', 'lei', 'leng', 'li', 'lian', 'liang', 'liao', 'lie', 'lin', 'ling',
        'liu',
        'long', 'lou', 'lu', u'l\u00FC', 'luan', u'l\u00FCe', 'lun', 'luo', 'ma', 'mai', 'man', 'mang', 'mao', 'me',
        'mei',
        'men', 'meng', 'mi', 'mian', 'miao', 'mie', 'min', 'ming', 'miu', 'mo', 'mou', 'mu', 'na', 'nai', 'nan', 'nang',
        'nao', 'ne', 'nei', 'nen', 'neng', 'ni', 'nia', 'nian', 'niang', 'niao', 'nie', 'nin', 'ning', 'niu', 'nong',
        'nou',
        'nu', u'n\u00FC', 'nuan', u'n\u00FCe', 'nuo', 'nun', 'ou', 'pa', 'pai', 'pan', 'pang', 'pao', 'pei', 'pen',
        'peng',
        'pi', 'pian', 'piao', 'pie', 'pin', 'ping', 'po', 'pou', 'pu', 'qi', 'qia', 'qian', 'qiang', 'qiao', 'qie',
        'qin',
        'qing', 'qiong', 'qiu', 'qu', 'quan', 'que', 'qun', 'ran', 'rang', 'rao', 're', 'ren', 'reng', 'ri', 'rong',
        'rou',
        'ru', 'ruan', 'rui', 'run', 'ruo', 'sa', 'sai', 'san', 'sang', 'sao', 'se', 'sei', 'sen', 'seng', 'sha', 'shai',
        'shan', 'shang', 'shao', 'she', 'shei', 'shen', 'sheng', 'shi', 'shong', 'shou', 'shu', 'shua', 'shuai',
        'shuan',
        'shuang', 'shui', 'shun', 'shuo', 'si', 'song', 'sou', 'su', 'suan', 'sui', 'sun', 'suo', 'ta', 'tai', 'tan',
        'tang', 'tao', 'te', 'teng', 'ti', 'tian', 'tiao', 'tie', 'ting', 'tong', 'tou', 'tu', 'tuan', 'tui', 'tun',
        'tuo',
        'wa', 'wai', 'wan', 'wang', 'wei', 'wen', 'weng', 'wo', 'wu', 'xi', 'xia', 'xian', 'xiang', 'xiao', 'xie',
        'xin',
        'xing', 'xiong', 'xiu', 'xu', 'xuan', 'xue', 'xun', 'ya', 'yai', 'yan', 'yang', 'yao', 'ye', 'yi', 'yin',
        'ying',
        'yo', 'yong', 'you', 'yu', 'yuan', 'yue', 'yun', 'za', 'zai', 'zan', 'zang', 'zao', 'ze', 'zei', 'zen', 'zeng',
        'zha', 'zhai', 'zhan', 'zhang', 'zhao', 'zhe', 'zhei', 'zhen', 'zheng', 'zhi', 'zhong', 'zhou', 'zhu', 'zhua',
        'zhuai', 'zhuan', 'zhuang', 'zhui', 'zhun', 'zhuo', 'zi', 'zong', 'zou', 'zu', 'zuan', 'zui', 'zun', 'zuo'
    ]

    def zhuyinref(self): return [
                   u'\u311A', u'\u311E', u'\u3122', u'\u3124', u'\u3120', u'\u3105\u311A', u'\u3105\u311E', u'\u3105\u3122',
                   u'\u3105\u3124',
                   u'\u3105\u3120', u'\u3105\u311F', u'\u3105\u3123', u'\u3105\u3125', u'\u3105\u30FC', u'\u3105\u30FC\u3122',
                   u'\u3105\u30FC\u3120', u'\u3105\u30FC\u311D', u'\u3105\u30FC\u3123', u'\u3105\u30FC\u3125',
                   u'\u3105\u311B',
                   u'\u3105\u3128', u'\u3118\u311A', u'\u3118\u311E', u'\u3118\u3122', u'\u3118\u3124', u'\u3118\u3120',
                   u'\u3118\u311C',
                   u'\u3118\u3123', u'\u3118\u3125', u'\u3114\u311A', u'\u3114\u311E', u'\u3114\u3122', u'\u3114\u3124',
                   u'\u3114\u3120',
                   u'\u3114\u311C', u'\u3114\u3123', u'\u3114\u3125', u'\u3114', u'\u3114\u3128\u3125', u'\u3114\u3121',
                   u'\u3114\u3128',
                   u'\u3114\u3128\u311A', u'\u3114\u3128\u311E', u'\u3114\u3128\u3122', u'\u3114\u3128\u3124',
                   u'\u3114\u3128\u311F',
                   u'\u3114\u3128\u3123', u'\u3114\u3128\u311B', u'\u3118', u'\u3118\u3128\u3125', u'\u3118\u3121',
                   u'\u3118\u3128',
                   u'\u3118\u3128\u3122', u'\u3118\u3128\u311F', u'\u3118\u3128\u3123', u'\u3118\u3128\u311B',
                   u'\u3109\u311A',
                   u'\u3109\u311E', u'\u3109\u3122', u'\u3109\u3124', u'\u3109\u3120', u'\u3109\u311C', u'\u3109\u3125',
                   u'\u3109\u30FC',
                   u'\u3109\u30FC\u3122', u'\u3109\u30FC\u3124', u'\u3109\u30FC\u3120', u'\u3109\u30FC\u311D',
                   u'\u3109\u30FC\u3125',
                   u'\u3109\u30FC\u3121', u'\u3109\u3128\u3125', u'\u3109\u3121', u'\u3109\u3128', u'\u3109\u3128\u3122',
                   u'\u3109\u3128\u311F', u'\u3109\u3128\u3123', u'\u3109\u3128\u311B', u'\u311C', u'\u311F', u'\u3123',
                   u'\u3126',
                   u'\u3108\u311A', u'\u3108\u3122', u'\u3108\u3124', u'\u3108\u311F', u'\u3108\u3123', u'\u3108\u3125',
                   u'\u3108\u311B',
                   u'\u3108\u3121', u'\u3108\u3128', u'\u310D\u311A', u'\u310D\u311E', u'\u310D\u3122', u'\u310D\u3124',
                   u'\u310D\u3120',
                   u'\u310D\u311C', u'\u310D\u311F', u'\u310D\u3123', u'\u310D\u3125', u'\u310D\u3128\u3125', u'\u310D\u3121',
                   u'\u310D\u3128', u'\u310D\u3128\u311A', u'\u310D\u3128\u311E', u'\u310D\u3128\u3122',
                   u'\u310D\u3128\u3124',
                   u'\u310D\u3128\u311F', u'\u310D\u3128\u3123', u'\u310D\u3128\u311B', u'\u310F\u311A', u'\u310F\u311E',
                   u'\u310F\u3122',
                   u'\u310F\u3124', u'\u310F\u3120', u'\u310F\u311C', u'\u310F\u311F', u'\u310F\u3123', u'\u310F\u3125',
                   u'\u310F\u3128\u3125', u'\u310F\u3121', u'\u310F\u3128', u'\u310F\u3128\u311A', u'\u310F\u3128\u311E',
                   u'\u310F\u3128\u3122', u'\u310F\u3128\u3124', u'\u310F\u3128\u311F', u'\u310F\u3128\u3123',
                   u'\u310F\u3128\u311B',
                   u'\u3110\u30FC', u'\u3110\u30FC\u311A', u'\u3110\u30FC\u3122', u'\u3110\u30FC\u3124',
                   u'\u3110\u30FC\u3120',
                   u'\u3110\u30FC\u311D', u'\u3110\u30FC\u3123', u'\u3110\u30FC\u3125', u'\u3110\u3129\u3125',
                   u'\u3110\u30FC\u3121',
                   u'\u3110\u3129', u'\u3110\u3129\u3122', u'\u3110\u3129\u311D', u'\u3110\u3129\u3123', u'\u310E\u311A',
                   u'\u310E\u311E',
                   u'\u310E\u3122', u'\u310E\u3124', u'\u310E\u3120', u'\u310E\u311C', u'\u310E\u3123', u'\u310E\u3125',
                   u'\u310E\u3128\u3125', u'\u310E\u3121', u'\u310E\u3128', u'\u310E\u3128\u311A', u'\u310E\u3128\u311E',
                   u'\u310E\u3128\u3122', u'\u310E\u3128\u3124', u'\u310E\u3128\u311F', u'\u310E\u3128\u3123',
                   u'\u310E\u3128\u311B',
                   u'\u310C\u311A', u'\u310C\u311E', u'\u310C\u3122', u'\u310C\u3124', u'\u310C\u3120', u'\u310C\u311C',
                   u'\u310C\u311F',
                   u'\u310C\u3125', u'\u310C\u30FC', u'\u310C\u30FC\u3122', u'\u310C\u30FC\u3124', u'\u310C\u30FC\u3120',
                   u'\u310C\u30FC\u311D', u'\u310C\u30FC\u3123', u'\u310C\u30FC\u3125', u'\u310C\u30FC\u3121',
                   u'\u310C\u3128\u3125',
                   u'\u310C\u3121', u'\u310C\u3128', u'\u310C\u3129', u'\u310C\u3128\u3122', u'\u310C\u3129\u311D',
                   u'\u310C\u3128\u3123',
                   u'\u310C\u3128\u311B', u'\u3107\u311A', u'\u3107\u311E', u'\u3107\u3122', u'\u3107\u3124', u'\u3107\u3120',
                   u'\u3107\u311C', u'\u3107\u311F', u'\u3107\u3123', u'\u3107\u3125', u'\u3107\u30FC', u'\u3107\u30FC\u3122',
                   u'\u3107\u30FC\u3120', u'\u3107\u30FC\u311D', u'\u3107\u30FC\u3123', u'\u3107\u30FC\u3125',
                   u'\u3107\u30FC\u3121',
                   u'\u3107\u3128\u311B', u'\u3107\u3121', u'\u3107\u3128', u'\u310B\u311A', u'\u310B\u311E', u'\u310B\u3122',
                   u'\u310B\u3124', u'\u310B\u3120', u'\u310B\u311B', u'\u310B\u311F', u'\u310B\u3123', u'\u310B\u3125',
                   u'\u310B\u30FC',
                   u'\u310B\u30FC\u311A', u'\u310B\u30FC\u3122', u'\u310B\u30FC\u3124', u'\u310B\u30FC\u3120',
                   u'\u310B\u30FC\u311D',
                   u'\u310B\u30FC\u3123', u'\u310B\u30FC\u3125', u'\u310B\u30FC\u3121', u'\u310B\u3128\u3125',
                   u'\u310B\u3121',
                   u'\u310B\u3128', u'\u310B\u3129', u'\u310B\u3128\u3122', u'\u310B\u3129\u311D', u'\u310B\u3128\u311B',
                   u'\u310B\u3128\u3123', u'\u3121', u'\u3106\u311A', u'\u3106\u311E', u'\u3106\u3122', u'\u3106\u3124',
                   u'\u3106\u3120',
                   u'\u3106\u311F', u'\u3106\u3123', u'\u3106\u3125', u'\u3106\u30FC', u'\u3106\u30FC\u3122',
                   u'\u3106\u30FC\u3120',
                   u'\u3106\u30FC\u311D', u'\u3106\u30FC\u3123', u'\u3106\u30FC\u3125', u'\u3106\u3128\u311B',
                   u'\u3106\u3121',
                   u'\u3106\u3128', u'\u3111\u30FC', u'\u3111\u30FC\u311A', u'\u3111\u30FC\u3122', u'\u3111\u30FC\u3124',
                   u'\u3111\u30FC\u3120', u'\u3111\u30FC\u311D', u'\u3111\u30FC\u3123', u'\u3111\u30FC\u3125',
                   u'\u3111\u3129\u3125',
                   u'\u3111\u30FC\u3121', u'\u3111\u3129', u'\u3111\u3129\u3122', u'\u3111\u3129\u311D',
                   u'\u3111\u3129\u3123',
                   u'\u3116\u3122', u'\u3116\u3124', u'\u3116\u3120', u'\u3116\u311C', u'\u3116\u3123', u'\u3116\u3125',
                   u'\u3116',
                   u'\u3116\u3128\u3125', u'\u3116\u3121', u'\u3116\u3128', u'\u3116\u3128\u3122', u'\u3116\u3128\u311F',
                   u'\u3116\u3128\u3123', u'\u3116\u3128\u311B', u'\u3119\u311A', u'\u3119\u311E', u'\u3119\u3122',
                   u'\u3119\u3124',
                   u'\u3119\u3120', u'\u3119\u311C', u'\u3119\u311F', u'\u3119\u3123', u'\u3119\u3125', u'\u3115\u311A',
                   u'\u3115\u311E',
                   u'\u3115\u3122', u'\u3115\u3124', u'\u3115\u3120', u'\u3115\u311C', u'\u3115\u311F', u'\u3115\u3123',
                   u'\u3115\u3125',
                   u'\u3115', u'\u3115\u3121\u3125', u'\u3115\u3121', u'\u3115\u3128', u'\u3115\u3128\u311A',
                   u'\u3115\u3128\u311E',
                   u'\u3115\u3128\u3122', u'\u3115\u3128\u3124', u'\u3115\u3128\u311F', u'\u3115\u3128\u3123',
                   u'\u3115\u3128\u311B',
                   u'\u3119', u'\u3119\u3128\u3125', u'\u3119\u3121', u'\u3119\u3128', u'\u3119\u3128\u3122',
                   u'\u3119\u3128\u311F',
                   u'\u3119\u3128\u3123', u'\u3119\u3128\u311B', u'\u310A\u311A', u'\u310A\u311E', u'\u310A\u3122',
                   u'\u310A\u3124',
                   u'\u310A\u3120', u'\u310A\u311C', u'\u310A\u3125', u'\u310A\u30FC', u'\u310A\u30FC\u3122',
                   u'\u310A\u30FC\u3120',
                   u'\u310A\u30FC\u311D', u'\u310A\u30FC\u3125', u'\u310A\u3128\u3125', u'\u310A\u3121', u'\u310A\u3128',
                   u'\u310A\u3128\u3122', u'\u310A\u3128\u311F', u'\u310A\u3128\u3123', u'\u310A\u3128\u311B',
                   u'\u3128\u311A',
                   u'\u3128\u311E', u'\u3128\u3122', u'\u3128\u3124', u'\u3128\u311F', u'\u3128\u3123', u'\u3128\u3125',
                   u'\u3128\u311B',
                   u'\u3128', u'\u3112\u30FC', u'\u3112\u30FC\u311A', u'\u3112\u30FC\u3122', u'\u3112\u30FC\u3124',
                   u'\u3112\u30FC\u3120',
                   u'\u3112\u30FC\u311D', u'\u3112\u30FC\u3123', u'\u3112\u30FC\u3125', u'\u3112\u3129\u3125',
                   u'\u3112\u30FC\u3121',
                   u'\u3112\u3129', u'\u3112\u3129\u3122', u'\u3112\u3129\u311D', u'\u3112\u3129\u3123', u'\u30FC\u311A',
                   u'\u30FC\u311E',
                   u'\u30FC\u3122', u'\u30FC\u3124', u'\u30FC\u3120', u'\u30FC\u311D', u'\u30FC', u'\u30FC\u3123',
                   u'\u30FC\u3125',
                   u'\u30FC\u311B', u'\u3129\u3125', u'\u30FC\u3121', u'\u3129', u'\u3129\u3122', u'\u3129\u311D',
                   u'\u3129\u3123',
                   u'\u3117\u311A', u'\u3117\u311E', u'\u3117\u3122', u'\u3117\u3124', u'\u3117\u3120', u'\u3117\u311C',
                   u'\u3117\u311F',
                   u'\u3117\u3123', u'\u3117\u3125', u'\u3113\u311A', u'\u3113\u311E', u'\u3113\u3122', u'\u3113\u3124',
                   u'\u3113\u3120',
                   u'\u3113\u311C', u'\u3113\u311F', u'\u3113\u3123', u'\u3113\u3125', u'\u3113', u'\u3113\u3128\u3125',
                   u'\u3113\u3121',
                   u'\u3113\u3128', u'\u3113\u3128\u311A', u'\u3113\u3128\u311E', u'\u3113\u3128\u3122',
                   u'\u3113\u3128\u3124',
                   u'\u3113\u3128\u311F', u'\u3113\u3128\u3123', u'\u3113\u3128\u311B', u'\u3117', u'\u3117\u3128\u3125',
                   u'\u3117\u3121',
                   u'\u3117\u3128', u'\u3117\u3128\u3122', u'\u3117\u3128\u311F', u'\u3117\u3128\u3123',
                   u'\u3117\u3128\u311B'
               ],