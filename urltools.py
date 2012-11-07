# vi:fenc=utf-8:tabstop=2:shiftwidth=2:smartindent:smarttab
import cookielib, gzip, StringIO, urlparse, urllib, urllib2, zlib
import htmlparser

USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:13.0) Gecko/20100101 Firefox/13.0.1'

HTML=1
IMAGE=2

referer = None

cj = cookielib.LWPCookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

class Request:
	def __init__(self, url, data=None, headers={}, base=None, expect=None):
		global referer
		
		if base != None:
			url = urlparse.urljoin(base, url)
		self.url = url
		
		if data != None and type(data) != str:
			data = urllib.urlencode(data)
		self.data = data
		
		headers['User-Agent'] = USER_AGENT
		headers['Accept-Language'] = "de-de,de;q=0.8,en-us;q=0.5,en;q=0.3"
		headers["Accept-Encoding"] = "gzip, deflate"
		headers["DNT"] = "1"
		
		if expect == None:
			pass
		elif expect == HTML:
			headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
		elif expect == IMAGE:
			headers["Accept"] = "image/png,image/*;q=0.8,*/*;q=0.5"
		else:
			raise Exception("Unknown Expectation: %s", expect)
		
		if referer:
			headers['Referer'] = referer
		if expect != IMAGE:
			referer = url
		
		self.headers = headers
		self.referer = referer
		
		self.request = urllib2.Request(self.url, self.data, self.headers)
		self.response = urllib2.urlopen(self.request)
		
		if self.response.info().get('Content-Encoding') == 'gzip':
			if hasattr(gzip, "decompress"):
				self.file = StringIO.StringIO(gzip.decompress(self.response.read()))
			else:
				self.file = StringIO.StringIO(gzip.GzipFile(fileobj=self.response))
		elif self.response.info().get('Content-Encoding') == 'deflate':
			self.file = StringIO.StringIO(zlib.decompress(self.response.read()))
		else:
			self.file = StringIO.StringIO(self.response.read())
	
	def read(self, length=None):
		return self.file.read(length)
	
	def get_dom(self):
		return htmlparser.parse(self.file.read())

def open(*args, **kwargs):
	return Request(*args, **kwargs)

def get_cookie(host, name):
	for cookie in cj:
		if cookie.domain == host and cookie.name == name:
			return cookie
	return None

