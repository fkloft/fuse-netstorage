#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64, os
import debug, urltools, xpath

class NetStorage(object):
	def __init__(self, server, root, username, password):
		self.server = server
		self.root = root
		self.username = username
		self.password = password
		self.authentication = "Basic %s" % base64.encodestring('%s:%s' % (self.username, self.password))[:-1]
		
		try:
			response = urltools.Request(self.root, base=self.server, expect=urltools.HTML)
		except urllib2.HTTPError, e:
			if hasattr(e, "code") and e.code == 401:
				base64string = base64.encodestring('%s:%s' % (self.username, self.password))[:-1]
				try:
					response = urltools.Request(
						self.root,
						base=self.server,
						expect=urltools.HTML,
						headers={"Authorization": "Basic %s" % base64string}
					)
				except:
					debug.debug(traceback.format_exc())
			else:
				raise e
		except:
			debug.debug(traceback.format_exc())
		
	
	def getSession(self):
		for cookie in urltools.cj:
			if cookie.name.lower() == "novellsession1":
				return cookie.value
		return None
	
	def getFolderIndex(self, path):
		try:
			response = urltools.Request(
				os.path.join(self.root, path),
				base=self.server,
				headers={"Authorization": self.authentication},
				expect=urltools.HTML
			)
		except Exception,e:
			debug.debug(traceback.format_exc())
			raise e
		
		dom = response.get_dom()
		
		script = dom.getElementsByTagName("body")[0].firstElementChild.childNodes[1].nodeValue
		string = script.split("devicePath=",1)[1].split("\n",1)[0].strip()
		deviceFolder = urllib.unquote(json.loads(string))
		
		table = xpath.find('//div[@id="fileArea"]/table[@class="FilesTable"]', dom)[0]
		
		files = []
		
		for row in table.childNodes:
			if row.nodeType != 1 or row.nodeName.lower() != "tr":
				continue
			
			c = row.children
			script = c[1].lastElementChild.childNodes[1].nodeValue
			
			filename = c[1].firstElementChild["title"]
			timestring = c[3].firstElementChild.childNodes[1].nodeValue.split('"')[1]
			mtime = time.strptime(timestring, "%b %d %Y %H:%M %Z")
			folder = "el.isFolder = true" in script
			string = script.split("el.fileURL=",1)[1].split(";",1)[0]
			uri = urllib.unquote(json.loads(string))
			files.append(\
			{
				"filename":filename,
				"mtime":mtime,
				"folder":folder,
				"uri": uri,
				"devicePath": os.path.join(deviceFolder, filename)
			})
		
		return files
	
	def getFileDetails(self, data):
		post = \
		{
			"method": "props",
			"file": data["uri"],
			"session": self.getSession()
		}
		
		try:
			response = urltools.Request(
				"/NetStorage/servlet/FileProps",
				base=self.server,
				data=post,
				headers={"Authorization": self.authentication}
			)
		except Exception,e:
			debug.debug(traceback.format_exc())
			raise e
		
		dom = response.get_dom()
		try:
			table = xpath.find('//div[@id="NFSRights"]/table', dom)[0]
		except IndexError:
			return data
		
		c = table.children
		data["size"] = int(c[1].children[1].firstChild.nodeValue.strip())
		
		try:
			script = c[2].children[1].firstElementChild.childNodes[1].nodeValue
			string = script.split("str=",1)[1].split("\n",1)[0].strip()
			timestring = urllib.unquote(json.loads(string))
			data["ctime"] = time.strptime(timestring, "%Y-%m-%dT%H:%M:%SZ")
		except:
			debug.debug(traceback.format_exc())
		
		try:
			script = c[3].children[1].firstElementChild.childNodes[1].nodeValue
			string = script.split("new Date(",1)[1].split(")\n",1)[0].strip()
			timestring = urllib.unquote(json.loads(string))
			data["mtime"] = time.strptime(timestring, "%a, %d %b %Y %H:%M:%S %Z")
		except:
			debug.debug(traceback.format_exc())
		
		data["detail"] = True
		
		return data
	



