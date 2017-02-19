import base64,os,re,requests,string,sys,urllib
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,xbmcvfs

addon_id   = 'plugin.video.VegasLifeTV'
icon       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
s          = requests.session()
base       = 'https://vimeo.com'

def CAT():
	addDir('VegasLifeTV',base+'/vegaslifetv/albums',1,icon,fanart,'')
	addDir('VegasLifeTV Live','url',4,icon,fanart,'')
		
def INDEX(url):
	open = OPEN_URL(url)
	all = regex_get_all(open,'div class="thumbnail_wrapper">','srcset=')
	for a in all:
		name = regex_from_to(a,'title="','"').replace("&#039;","'").replace('&amp;','&')
		url  = regex_from_to(a,'<a href="','"')
		url  = (base+url+'/rss')
		thumb= regex_from_to(a,'<img src="','"')
		addDir(name,url,2,icon,fanart,'')
	try:
		nxp= re.compile('pagination_next.*?<a href="(.*?)"',re.DOTALL).findall(open)
		next=str(nxp).replace("['","").replace("']","")
		addDir('[COLOR red]NEXT PAGE[/COLOR]',base+next,1,icon,fanart,'')
	except:pass
	
def INDEX2(url):
	open = OPEN_URL(url)
	all  = regex_get_all(open,'<item>','/><media:title>')
	for a in all:
		name = regex_from_to(a,'<title>','</title>').replace("&#039;s","'").replace('&amp;','&')
		url   = regex_from_to(a,'<link>','</link>')
		xbmc.log(str(url))
		icon = re.compile('thumbnail.*?url="(.*?)"').findall(a)
		icon = str(icon).replace("']","").replace("['","")
		addDir(name,url,3,icon,fanart,'')
		
def RESOLVE(url):
	url = (url+'/')
	id = regex_from_to(url,'com/','/')
	config='plugin://plugin.video.vimeo/play/?video_id='+id
	liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
	liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': description})
	liz.setProperty('IsPlayable','true')
	liz.setPath(str(config))
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	
def Live():
	play = 'http://xvegaslifetvx.api.channel.livestream.com/3.0/playlist.m3u8'
	liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
	liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': description})
	liz.setProperty('IsPlayable','true')
	liz.setPath(str(play))
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	
			
			
	
def addDir(name,url,mode,icon,fanart,description):
	u=sys.argv[0]+"?url="+url+"&mode="+str(mode)+"&name="+str(name)+"&icon="+str(icon)+"&description="+str(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=icon)
	liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
	liz.setProperty('fanart_image', fanart)
	if mode==3 or mode==4:
		liz.setProperty("IsPlayable","true")
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	else:
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok
	xbmcplugin.endOfDirectory

def regex_from_to(text, from_string, to_string, excluding=True):
	if excluding:
		try: r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
		except: r = ''
	else:
		try: r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
		except: r = ''
	return r


def regex_get_all(text, start_with, end_with):
	r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
	return r


def OPEN_URL(url):
	headers = {}
	headers['User-Agent'] = User_Agent
	link = s.get(url, headers=headers, verify=False).text
	link = link.encode('ascii', 'ignore')
	return link
	
def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
	return param


params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None
query=None
type=None

try:
	url=urllib.unquote_plus(params["url"])
except:
	pass
try:
	name=urllib.unquote_plus(params["name"])
except:
	pass
try:
	iconimage=urllib.unquote_plus(params["iconimage"])
except:
	pass
try:
	mode=int(params["mode"])
except:
	pass
try:
	description=urllib.unquote_plus(params["description"])
except:
	pass
try:
	query=urllib.unquote_plus(params["query"])
except:
	pass
try:
	type=urllib.unquote_plus(params["type"])
except:
	pass

if mode==None or url==None or len(url)<1:
	CAT()

elif mode==1:
	INDEX(url)
	
elif mode==2:
	INDEX2(url)
	
elif mode==3:
	RESOLVE(url)

elif mode==4:
	Live()


xbmcplugin.endOfDirectory(int(sys.argv[1]))