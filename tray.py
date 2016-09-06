#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import os
from database import Database

if(os.name=='nt'):
	WIN=True;
else:
	WIN=False;

db = Database();

TRAY_TOOLTIP = 'Pilnuj tray app'
TRAY_ICON = 'icon.png'
TRAY_ICON2 = 'icon2.png'

def create_menu_item(menu, label, func):
	item = wx.MenuItem(menu, -1, label)
	menu.Bind(wx.EVT_MENU, func, id=item.GetId())
	menu.AppendItem(item)
	return item

class TaskBarIcon(wx.TaskBarIcon):
	def __init__(self, frame):
		self.frame = frame
		super(TaskBarIcon, self).__init__()
		self.set_icon(TRAY_ICON)
		self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)        
		self.timer.Start(15000) # start timer after a delay
		if(not WIN):
			self.note = wx.NotificationMessage("Pilnuj", "")

	def CreatePopupMenu(self):
		menu = wx.Menu()
		create_menu_item(menu, 'OK, I understand', self.on_ok)
		create_menu_item(menu, 'Note', self.on_note)
		menu.AppendSeparator()
		create_menu_item(menu, 'Exit', self.on_exit)
		return menu

	def set_icon(self, path):
		icon = wx.IconFromBitmap(wx.Bitmap(path))
		self.SetIcon(icon, TRAY_TOOLTIP)

	def on_left_down(self, event):
		print 'Tray icon was left-clicked.'

	def on_ok(self, event):
		db.add_all();
		self.set_icon(TRAY_ICON);

	def on_timer(self, event):
		print "Timer"
		changed = db.check();
		if(len(changed)>0):
			self.set_icon(TRAY_ICON2);
			files=[];
			for abs_path in changed:
				files.append(os.path.basename(abs_path))
			msg="File(s) changed:"+",".join(files);
			if(WIN):
				self.ShowBalloon("Pilnuj",msg,msec=3000)
			else:
				self.note.SetMessage("File(s) changed:"+",".join(files))
				self.note.Show(timeout=3)

		#else:
		#	self.note.Close()

	def on_note(self, event):
		if(WIN):
			self.ShowBalloon("Pilnuj","Hello world!",msec=3000)
		else:
			wx.NotificationMessage("Pilnuj", "Hello world!").Show()

	def on_exit(self, event):
		wx.CallAfter(self.Destroy)
		self.frame.Close()

class App(wx.App):
	def OnInit(self):
		frame=wx.Frame(None)
		if(WIN):
			self.locale = wx.Locale(wx.LANGUAGE_ENGLISH);
		self.SetTopWindow(frame)
		TaskBarIcon(frame)
		return True

app = App(False)
app.MainLoop()
