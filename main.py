#!/usr/bin/env python
# vi:fenc=utf-8:tabstop=2:shiftwidth=2:smartindent:smarttab:expandtab

import fuse, os, stat, time, traceback, sys

import config, debug, netstorage

fuse.fuse_python_api = (0, 2)

sys.stdout = sys.stderr = debug.debugfile
sys.stdout.write("\n\n\n")
sys.stdout.flush()

class NetStorageStat(fuse.Stat):
	def __init__(self, server, fh):
		try:
			if not "detail" in fh:
				fh = server.getFileDetails(fh)
			self.fh = fh
			
			if fh["folder"]:
				self.st_mode = stat.S_IFDIR | 0755
				self.st_nlink = 2
				self.st_size = 4096
			else:
				self.st_mode = stat.S_IFREG | 0666
				self.st_nlink = 1
				if "size" in fh:
					self.st_size = fh["size"]
				else:
					self.st_size = 0;
			
			self.st_ino = 0
			self.st_dev = 0
			self.st_uid = 0
			self.st_gid = 0
			self.st_rdev = 0
			self.st_blksize = 0
			self.st_blocks = 24
			self.st_atime = time.time()
			self.st_mtime = self._get_time("mtime")
			self.st_ctime = self._get_time("ctime")
		except Exception, e:
			debug.debug(traceback.format_exc())
			raise e
	
	def _get_time(self, t):
		for i in (t, "mtime", "ctime", "atime"):
			if i in self.fh:
				return self.fh[i]
		return time.time()
	
	def __getattr__(self, name):
		raise AttributeError
	
	def __hasattr__(self, name):
		return False

class NetStorageFS(fuse.Fuse):
	def __init__(self, server, root, username, password, *args, **kw):
		self.server = netstorage.NetStorage(server, root, username, password)
		
		fuse.Fuse.__init__(self, *args, **kw)
		
		self.dir_class = NetStorageFolder
	
	def getattr(self, path):
		debug.debug("getattr(",path,")")
		try:
			if path == "/":
				fh = \
				{
					"detail": True,
					"folder": True
				}
			else:
				parent, name = path.rsplit("/", 1)
				if parent.startswith("/"):
					parent = parent[1:]
				
				contents = self.server.getFolderIndex(parent)
				fh = [f for f in contents if f["filename"] == name]
				
				if not len(fh):
					debug.debug("No such file or directory")
					return -errno.ENOENT
				
				fh = fh[0]
			
			st = NetStorageStat(self.server, fh)
			
			return st
		except Exception, e:
			debug.debug(traceback.format_exc())
			raise e

	def readdir(self, path, offset):
		try:
			if path[0] == "/":
				path = path[1:]
			
			dirents = \
			[
				".",
				".."
			]
			
			dirents.extend([i["filename"] for i in self.server.getFolderIndex(path)])
			
			for r in dirents:
				yield fuse.Direntry(str(r))
		except Exception, e:
			debug.debug(traceback.format_exc())
			raise e
	
	#def read(self, *args):
	
	def __getattr__(self, name):
		raise AttributeError
	
	def __hasattr__(self, name):
		return False

class NetStorageFolder:
	def __init__(self, *args):
		pass
		#de FIXME bug.debug("NetStorageFolder",args)
	
	def __getattr__(self, name):
		raise AttributeError
	
	def __hasattr__(self, name):
		return False

def main():
	server = NetStorageFS(config.servername, config.root, config.username, config.password)
	#version="%prog " + fuse.__version__,
	#				usage=usage, dash_s_do='setsingle')
	try:
		server.parse(errex=1)
		server.main()
	except Exception,e:
		debug.debug(traceback.format_exc())
		raise e

if __name__ == '__main__':
	main()

