#!/usr/bin/env python
# vi:fenc=utf-8:tabstop=2:shiftwidth=2:smartindent:smarttab
import os, sys, traceback

filename = os.path.join(os.path.dirname(__file__), "debug.pipe")
if not os.path.exists(filename):
	os.mkfifo(filename)
debugfile = file(filename, "w")

def debug(*args):
	data = " ".join([str(i) for i in args])
	debugfile.write("\0%s\0" % data)
	debugfile.flush()

def debug_stack():
	stack = traceback.extract_stack()
	data = "".join(traceback.format_list(stack[:-1]))
	
	filename, linenumber, function, line = stack[-2]
	
	debugfile.write(
		"\0Printing of stack was requested by:\n  File \"%s\", line %d, in %s\n    %s\n\n%s\0" %
		(
			filename,
			linenumber,
			function,
			line,
			data
		)
	)
	debugfile.flush()

def debug_exception():
	data = "".join(traceback.format_exc())
	
	filename, linenumber, function, line = traceback.extract_stack()[-2]
	
	debugfile.write(
		"\0Printing of current exception was requested by:\n  File \"%s\", line %d, in %s\n    %s\n\n%s\0" %
		(
			filename,
			linenumber,
			function,
			line,
			data
		)
	)
	debugfile.flush()

def excepthook(type, value, trace):
	data = "".join(traceback.format_exception(type, value, trace))
	
	debugfile = file(filename, "w")
	debugfile.write("\0Exception caught by sys.excepthook:\n%s\0" % data)
	debugfile.flush()

sys.excepthook = excepthook

sys.stdout = sys.stderr = debugfile
sys.stdout.flush()

debug("###clear###")

