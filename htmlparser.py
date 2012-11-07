#!/usr/bin/env python
# vi:fenc=utf-8:tabstop=2:shiftwidth=2:smartindent:smarttab

import tidylib, xml.dom.minidom
import domextensions

def parse(response):
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
	return xml.dom.minidom.parseString(html)

