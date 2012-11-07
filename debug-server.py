#!/usr/bin/env python
# vi:fenc=utf-8:tabstop=2:shiftwidth=2:smartindent:smarttab

import os, glib, gobject, time

filename = os.path.join(os.path.dirname(__file__), "debug.pipe")
if not os.path.exists(filename):
	os.mkfifo(filename)

def open_pipe():
	debugfile = file(filename, "r")
	glib.io_add_watch(debugfile, glib.IO_IN | glib.IO_HUP, callback)

def callback(source, condition):
	data = source.read(4096)
	if data != "":
		messages = data.split("\0")
		for msg in messages:
			if msg != "":
				log(msg)
	
	if data == "" or condition == glib.IO_HUP:
		log("Pipe was closed, will now reopen...")
		source.close()
		open_pipe()
		return False
	
	return True

def log(msg):
	if msg == "###clear###":
		print "\n"*10
		print "Screen cleared\n"
		os.system("clear")
	else:
		print "%s\n\n--> Received at %s\n%s" % ("="*79, time.strftime("%H:%M:%S"), msg.rstrip())

open_pipe()

loop = gobject.MainLoop()
loop.run()


