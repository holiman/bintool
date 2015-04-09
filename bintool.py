#!/usr/bin/env python
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

import sys
from gui import ui

def do_rotate(num,data):
	if num > 0: return data[num:]
	return data[num:] + data[0:num] 
#		return "L(%d)%s" % (num,data)


def invert(data):
	i =[]
	for c in data:
		if c == "1": i.append("0")
		if c == "0": i.append("1")
	return "".join(i)

def asc2bin(data):
	return ''.join([bin(ord(c))[2:].zfill(8) for c in data])

#	return "BIN(%s)" % data

def bin2asc(data):
	out =[]
	length = len(data)
	i=0
	while ( i +8 <= length) :
		num =chr(int(data[i:i+8],2))
		out.append(num)
		i = i+8
		#out.append(hex()[2:])
	return "".join(out)


#	return "ASC(%s)" % data

def bin2hex(data):
	out =[]
	length = len(data)
	i=0
	while ( i +4 <= length) :
		out.append(hex(int(data[i:i+4],2))[2:])
		i = i+4
	return "".join(out)
#	return "HEX(%s)" % binstring

def hex2bin(hexstring):
	return ''.join([bin(int(c,16))[2:].zfill(4) for c in hexstring])
#	return "BIN(%s)" % hexstring

def mk_converter(inv, rotate, format = None):
	# binstr| not| >>2| hex
	def fn_canon(data):
		src = unicode(data)
		data = src.encode('utf_8') 
		#data = bytearray(data)
		if format == "hex":
			data = hex2bin(data)
		if format =="asc":
			data = asc2bin(data)
		if rotate:
			data = do_rotate(rotate,data)
		if inv:
			data = invert(data)
		return data
	#binstr| not| >>2| hex
	def fn_convert(data):
		src = unicode(data)
		data = src.encode('utf_8') 
		if(inv):
			data = invert(data)
		if(rotate):
			data = do_rotate(-rotate,data)
		if format == "hex":
			data = bin2hex(data)
		if format == "asc":
			data = bin2asc(data)
		return data

	return (fn_canon, fn_convert)

#add(field_nbin, mk_converter(1,0,0))
#add(field_nhex2, mk_converter(1,2,1))



class BinWindow(QMainWindow):
	
	def __init__(self):
		QMainWindow.__init__(self)

		# Set up the user interface from Designer.
		self.ui = ui.Ui_MainWindow()
		self.ui.setupUi(self)

		# Make some local modifications.
		#self.ui.colorDepthCombo.addItem("2 colors (1 bit per pixel)")


		self.fields = []
		self.connect(self.ui.lineEdit_bin,mk_converter(0,0,None))
		self.connect(self.ui.lineEdit_nbin,mk_converter(1,0,None))
		self.connect(self.ui.lineEdit_nhex,mk_converter(1,0,"hex"))
		self.connect(self.ui.lineEdit_nhex1,mk_converter(1,1,"hex"))
		self.connect(self.ui.lineEdit_nhex2,mk_converter(1,2,"hex"))
		self.connect(self.ui.lineEdit_nhex3,mk_converter(1,3,"hex"))
		self.connect(self.ui.lineEdit_hex,mk_converter(0,0,"hex"))
		self.connect(self.ui.lineEdit_hex1,mk_converter(0,1,"hex"))
		self.connect(self.ui.lineEdit_hex2,mk_converter(0,2,"hex"))
		self.connect(self.ui.lineEdit_hex3,mk_converter(0,3,"hex"))
		self.connect(self.ui.lineEdit_nascii,mk_converter(1,0,"asc"))
		self.connect(self.ui.lineEdit_nascii1,mk_converter(1,1,"asc"))
		self.connect(self.ui.lineEdit_nascii2,mk_converter(1,2,"asc"))
		self.connect(self.ui.lineEdit_nascii3,mk_converter(1,3,"asc"))
		self.connect(self.ui.lineEdit_ascii,mk_converter(0,0,"asc"))
		self.connect(self.ui.lineEdit_ascii1,mk_converter(0,1,"asc"))
		self.connect(self.ui.lineEdit_ascii2,mk_converter(0,2,"asc"))
		self.connect(self.ui.lineEdit_ascii3,mk_converter(0,3,"asc"))

	def connect(self, component, update_fns = None):
		(to_canon_fn, to_specific_fn)  = update_fns;


		def updateData(canon_data):
			component.setText(to_specific_fn(canon_data))
		
		self.fields.append((component, updateData))

		def updateAll(text):
			data = to_canon_fn(text)
			self.update(source = component, data = data)

		QtCore.QObject.connect(component, QtCore.SIGNAL(_fromUtf8("textEdited(QString)")),  updateAll)
	
	def update(self, source, data):
		for (c,update_fn) in self.fields:
			if c == source: continue;
			update_fn(data)

#	def oldconnect(self,component, to_canonical = None, converter = None, validator = None):
#		self.fields.append(component)
#
#		def on_edit(data):
#			if validator is not None and not validator(text)):
#				return
#			if to_canonical is not None:
#				data = to_canonical(text)
#			self.updateFields( data )
#		
#		def on_data(data):
#			self.setText(text)
#
#		QtCore.QObject.connect(component, QtCore.SIGNAL(_fromUtf8("textEdited(QString)")),  on_edit)
#	
#	def old_updateFields(self,text,component):
#		print("regenerated called, text %s %s" % (repr(text), repr(component)))
#		for c in self.fields:
#			if c == component: continue;
#			c.setText(text)
#
def main():
	app = QApplication(sys.argv)
	window = BinWindow()
	window.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()