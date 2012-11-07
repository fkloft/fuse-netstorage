#!/usr/bin/env python

import tidylib, xml.dom.minidom

def html2dom(response):
	text = response.read()
	
	html, errors = tidylib.tidy_document(text, options=\
	{
		"output-xml": 1,
		"indent": 1,
		"tidy-mark": 0,
		"force-output": 1,
		"add-xml-decl": 1,
		"numeric-entities": 1,
		"output-encoding": "utf8",
		"drop-empty-paras": 0,
		"merge-divs": "no",
		"merge-spans": "no"
	})
	#open("/home/felix/Desktop/fuse/debug.htm","w").write(html) # FIXME
	return xml.dom.minidom.parseString(html)

