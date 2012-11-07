from xml.dom.minidom import Element, Node

def getChildren(self):
	return [node for node in self.childNodes if node.nodeType==1]

def getFirstElementChild(self):
	children = self.children
	if len(children):
		return children[0]
	
def getLastElementChild(self):
	children = self.children
	if len(children):
		return children[-1]

def getNextElementSibling(self):
	node = self.nextSibling
	while node:
		if node.nodeType == 1:
			return node
		node = node.nextSibling

def getPreviousElementSibling(self):
	node = self.previousSibling
	while node:
		if node.nodeType == 1:
			return node
		node = node.previousSibling

def getTextContent(self):
	if self.nodeType == 3:
		return self.nodeValue
	elif self.nodeType == 1:
		return "".join([node.textContent for node in self.childNodes])

def getAttribute(self, key):
	if self.hasAttribute(key):
		return self.getAttribute(key)
	raise KeyError(key)

Node.nextElementSibling       = property(getNextElementSibling)
Node.previousElementSibling   = property(getPreviousElementSibling)
Node.textContent              = property(getTextContent)
Element.__getitem__           = getAttribute
Element.children              = property(getChildren)
Element.firstElementChild     = property(getFirstElementChild)
Element.lastElementChild      = property(getLastElementChild)
