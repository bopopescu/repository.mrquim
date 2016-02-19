from __future__ import unicode_literals
from resources.lib.modules import client,webutils
import re,urlparse,os,sys,json

try:
    import CommonFunctions as common
except:
    from resources.lib.modules import commonfunctionsdummy as common
from addon.common.addon import Addon
addon = Addon('plugin.video.castaway', sys.argv)

AddonPath = addon.get_path()
IconPath = AddonPath + "/resources/media/"
def icon_path(filename):
    return os.path.join(IconPath, filename)

class info():
    def __init__(self):
    	self.mode = 'livetv_nhl'
        self.name = 'livetv.sx (NHL full replays & highlights)'
        self.icon = icon_path('nhlstream.jpg')
        self.paginated = False
        self.categorized = False
        self.multilink = True


class main():
	def __init__(self,url = 'http://livetv.sx/en/videotourney/2/'):
		self.base = 'http://livetv.sx'
		self.url = url

	def items(self):
		result = client.request(self.url)
		result = result.decode('iso-8859-1').encode('utf-8')
		items= common.parseDOM(result, "table", attrs = { "height": "27" })
		items = self.__prepare_items(items,result)
		return items

	def __prepare_items(self,items,result):
		out=[]
		for video in items:
				title = re.compile('<b>(.+?)</b>').findall(video)
				title = [i for i in title if '&ndash;' in i or '-' in i][-1]
				title = title.split('<b>')[-1]
				title = title.replace('&ndash;', '-')
				title = common.replaceHTMLCodes(title)
				title = title.encode('utf-8')
				url = self.base + re.compile('<a.+?href="(.+?)"').findall(video)[0]
				out+=[(title,url,info().icon)]
			
			
		return out

	def links(self,url):
		out=[]
		html = client.request(url)
		soup = webutils.bs(html)
		table = soup.find('table',{'align':'center', 'width':'96%', 'cellpadding':'1','cellspacing':'1'})
		links = table.findAll('td',{'width':'33%'})
		for link in links:
			url = self.base + link.find('a')['href']
			title = link.findAll('a')[1].find('b').getText()
			img = link.find('img')['src']
			out.append((title,url,img))


		return out

	def resolve(self,url):
		html = client.request(url)
		soup = webutils.bs(html)
		url = soup.find('iframe',{'width':'600'})['src']
		if 'nhl' in url:
			url = url.split("playlist=")[-1]
			url = 'http://video.nhl.com/videocenter/servlets/playlist?ids=%s&format=json' % url
			result = client.request(url)
			url = re.compile('"publishPoint":"(.+?)"').findall(result)[0]
			return url
		elif 'rutube' in url:
			url = 'http:' + url
			result = client.request(url)
			m3u8 = re.compile('video_balancer&quot;: {.*?&quot;m3u8&quot;: &quot;(.*?)&quot;}').findall(result)[0]
			result = client.request(m3u8)
			url = re.compile('"\n(.+?)\n').findall(result)
			url = url[::-1]
			return url[0]
		elif 'youtube' in url:
			import liveresolver
			return liveresolver.resolve(url)
		else:
			import urlresolver
			url = urlresolver.resolve(url)
			return url