import os, time, traceback

debugfile = file("/home/felix/Desktop/fuse/debug.log","a")

def debug(*args):
	data = " ".join([str(i) for i in args])
	timestamp = time.strftime("%H:%M:%S")
	
	try:
		(filename, line, function, text) = traceback.extract_stack()[-2]
	except:
		function = "???"
		line = -1
		filename = "???"
	debugfile.write("="*50 + "\n%s: %s@%s:%3d:\n%s\n" % (timestamp,function,filename,line, data))
	debugfile.flush()

