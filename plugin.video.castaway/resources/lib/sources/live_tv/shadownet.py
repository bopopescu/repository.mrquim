from __future__ import unicode_literals
from resources.lib.modules import client,webutils
import re,sys,xbmcgui,os
from addon.common.addon import Addon
addon = Addon('plugin.video.castaway', sys.argv)

AddonPath = addon.get_path()
IconPath = AddonPath + "/resources/media/"
def icon_path(filename):
    return os.path.join(IconPath, filename)

class info():
    def __init__(self):
    	self.mode = 'shadownet'
        self.name = 'shadownet.ro'
        self.icon = 'shadownet.png'
        self.paginated = True
        self.categorized = True
        self.multilink = False
class main():
	def __init__(self,url = 'http://www.sdw-net.co/'):
		self.base = 'http://www.sdw-net.co/'
		self.url = url


	def categories(self):
		html = client.request(self.base)
		cats = re.findall('<li class=""><a href="(.+?)">(.+?) Channels</a>',html)
		out = []
		for c in cats:
			url = c[0]
			title = c[1].replace('amp;','') + ' Channels'
			img = info().icon
			out.append((url,title,img))
		return out

	def channels(self,url):
		self.url = url
		html = client.request(url, referer=self.base)
		html = client.parseDOM(html, 'div', attrs={'id':'CategoryContent'})[0]
		channels = re.findall('<div class="ProductImage">\s*<a href="(.+?)"\s*><img src="(.+?)" alt="(.+?)" /></a>', html)
		events = self.__prepare_channels(channels)
		events = list(set(events))
		events.sort(key=lambda x: x[1])
		return events

	def __prepare_channels(self,channels):
		new=[]
		for channel in channels:
			url = channel[0]
			img = channel[1]
			title = channel[2].encode('utf-8')
			new.append((url,title,img))
		return new

	def next_page(self):
		html = client.request(self.url)
		try:
			next = re.findall('<a href="(.+?)">Next',html)[0]
			if next==self.url: next = False
		except:
			next = False

		return next
