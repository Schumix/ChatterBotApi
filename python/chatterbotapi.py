import md5
import urllib
import urllib2
import uuid
import xml.dom.minidom

"""
    chatterbotapi
    Copyright (C) 2011 pierredavidbelanger@gmail.com
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.
    
    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

#################################################
# API
#################################################

class ChatterBotType:

    CLEVERBOT = 1
    JABBERWACKY = 2
    PANDORABOTS = 3

class ChatterBotFactory:

    def create(self, type, arg = None):
        if type == ChatterBotType.CLEVERBOT:
            return _Cleverbot('http://cleverbot.com/webservicemin')
        elif type == ChatterBotType.JABBERWACKY:
            return _Cleverbot('http://jabberwacky.com/webservicemin')
        elif type == ChatterBotType.PANDORABOTS:
            if arg == None:
                raise Exception('PANDORABOTS needs a botid arg')
            return _Pandorabots(arg)
        return None

class ChatterBot:

    def create_session(self):
        return None

class ChatterBotSession:

    def think_thought(self, thought):
        return thought

    def think(self, text):
        thought = ChatterBotThought()
        thought.text = text
        return self.think_thought(thought).text

class ChatterBotThought:

    pass

#################################################
# Cleverbot impl
#################################################

class _Cleverbot(ChatterBot):

    def __init__(self, url):
        self.url = url

    def create_session(self):
        return _CleverbotSession(self)

class _CleverbotSession(ChatterBotSession):

    def __init__(self, bot):
        self.bot = bot
        self.vars = {}
        self.vars['start'] = 'y'
        self.vars['icognoid'] = 'wsf'
        self.vars['fno'] = '0'
        self.vars['sub'] = 'Say'
        self.vars['islearning'] = '1'
        self.vars['cleanslate'] = 'false'

    def think_thought(self, thought):
        self.vars['stimulus'] = thought.text
        data = urllib.urlencode(self.vars)
        data_to_digest = data[9:29]
        data_digest = md5.new(data_to_digest).hexdigest()
        data = data + '&icognocheck=' + data_digest
        url_response = urllib2.urlopen(self.bot.url, data)
        response = url_response.read()
        response_values = response.split('\r')
        #self.vars['??'] = response_values[0] if len(response_values) > 0 else ''
        self.vars['sessionid'] = response_values[1] if len(response_values) > 1 else ''
        self.vars['logurl'] = response_values[2] if len(response_values) > 2 else ''
        self.vars['vText8'] = response_values[3] if len(response_values) > 3 else ''
        self.vars['vText7'] = response_values[4] if len(response_values) > 4 else ''
        self.vars['vText6'] = response_values[5] if len(response_values) > 5 else ''
        self.vars['vText5'] = response_values[6] if len(response_values) > 6 else ''
        self.vars['vText4'] = response_values[7] if len(response_values) > 7 else ''
        self.vars['vText3'] = response_values[8] if len(response_values) > 8 else ''
        self.vars['vText2'] = response_values[9] if len(response_values) > 9 else ''
        self.vars['prevref'] = response_values[10] if len(response_values) > 10 else ''
        #self.vars['??'] = response_values[11] if len(response_values) > 11 else ''
        self.vars['emotionalhistory'] = response_values[12] if len(response_values) > 12 else ''
        self.vars['ttsLocMP3'] = response_values[13] if len(response_values) > 13 else ''
        self.vars['ttsLocTXT'] = response_values[14] if len(response_values) > 14 else ''
        self.vars['ttsLocTXT3'] = response_values[15] if len(response_values) > 15 else ''
        self.vars['ttsText'] = response_values[16] if len(response_values) > 16 else ''
        self.vars['lineRef'] = response_values[17] if len(response_values) > 17 else ''
        self.vars['lineURL'] = response_values[18] if len(response_values) > 18 else ''
        self.vars['linePOST'] = response_values[19] if len(response_values) > 19 else ''
        self.vars['lineChoices'] = response_values[20] if len(response_values) > 20 else ''
        self.vars['lineChoicesAbbrev'] = response_values[21] if len(response_values) > 21 else ''
        self.vars['typingData'] = response_values[22] if len(response_values) > 22 else ''
        self.vars['divert'] = response_values[23] if len(response_values) > 23 else ''
        response_thought = ChatterBotThought()
        response_thought.text = response_values[16] if len(response_values) > 16 else ''
        return response_thought

#################################################
# Pandorabots impl
#################################################

class _Pandorabots(ChatterBot):

    def __init__(self, botid):
        self.botid = botid

    def create_session(self):
        return _PandorabotsSession(self)

class _PandorabotsSession(ChatterBotSession):

    def __init__(self, bot):
        self.vars = {}
        self.vars['botid'] = bot.botid
        self.vars['custid'] = uuid.uuid1()

    def think_thought(self, thought):
        self.vars['input'] = thought.text
        data = urllib.urlencode(self.vars)
        url_response = urllib2.urlopen('http://www.pandorabots.com/pandora/talk-xml', data)
        response = url_response.read()
        response_dom = xml.dom.minidom.parseString(response)
        response_thought = ChatterBotThought()
        response_thought.text = response_dom.getElementsByTagName('that')[0].childNodes[0].data
        return response_thought
