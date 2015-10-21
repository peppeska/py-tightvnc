#! /usr/bin/python


###############################################################
#
#
#   ____            _____ _       _     _ __     ___   _  ____ 
#  |  _ \ _   _    |_   _(_) __ _| |__ | |\ \   / / \ | |/ ___|
#  | |_) | | | |_____| | | |/ _` | '_ \| __\ \ / /|  \| | |    
#  |  __/| |_| |_____| | | | (_| | | | | |_ \ V / | |\  | |___ 
#  |_|    \__, |     |_| |_|\__, |_| |_|\__| \_/  |_| \_|\____|
#         |___/             |___/                              
#
#
#
###############################################################
# 
#              AUTORS
#
#       Moscato Giuseppe aka peppeska <moscatog@yahoo.it>
# 
#       Altamore Giovanni <zzuncu@hotmail.com>
# 
# 
# 
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
# 
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
# 
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
# 
###############################################################



import gtk
import gtk.glade
import os
import commands
import re
import time


class FirstDialog(gtk.Window):

	def __init__(self):
		# Load Glade Interface
		mainGlade = gtk.glade.XML("py-tightvnc.glade")

		self.status=1


		#######   Tray Icon  #############
		
		self.tray=gtk.StatusIcon()
		self.logoimage=gtk.Image()
		self.logoimage.set_from_file("py-tightvnc.png")
		self.tray.set_from_file("py-tightvnc.png")
#		self.tray.connect("activate", self.tray_click)
		self.IsHide=0
				

		################################################	
		#First Window Option
		
		# Load First Window
		self.win = mainGlade.get_widget("window1")
		


#		self.win.connect("hide",self.hide)
		self.win.set_title("Py-TightVNC")
#		self.win.set_icon("Py-TightVNC")
		self.win.connect("delete_event",self.close_win)
		
		
		#Main label
		self.win.label_first=mainGlade.get_widget("label1")
#		self.win.label_first.set_text("CiaoVa")

		#Reload Button
#		self.win.button_reload=mainGlade.get_widget("butt_reload")
#		self.win.button_reload.connect("clicked", self.control)

		#Quit Button Option
		self.win.button_quit=mainGlade.get_widget("butt_quit")
		self.win.button_quit.connect("clicked", self.quit)
	
		#Quit Item Option
		self.win.item_quit=mainGlade.get_widget("item_quit")
		self.win.item_quit.connect("activate", self.quit)
		
		#Info Item Option
		self.win.item_info=mainGlade.get_widget("imagemenuitem10")
		self.win.item_info.connect("activate", self.info)
		
		#Connect Button Option
		self.win.butt_connect=mainGlade.get_widget("butt_connect")
		self.win.butt_connect.connect("clicked", self.connect, "connect")

		#Cancel Button Option
		#self.win.button_cancel=mainGlade.get_widget("butt_cancel")
		#self.win.button_cancel.connect("clicked", self.cancel)
	
		#killall Button
		self.win.button_killall=mainGlade.get_widget("button_killall")	
		self.win.button_killall.connect("clicked",self.killall)
		
		#Button More
# 		self.win.butt_more=mainGlade.get_widget("expmore")
#		self.win.butt_more.connect("activate", self.more)
		
		self.win.scroll_text_more=mainGlade.get_widget("scroll_more")

		self.win.text_view=mainGlade.get_widget("textviewmore")	
	
		color1 = gtk.gdk.color_parse('black')
	        #self.win.scroll_text_more.modify_bg(gtk.STATE_NORMAL, color1)

#		self.win.text_view.modify_bg(gtk.STATE_NORMAL,color1)	
#
		color2 = gtk.gdk.color_parse('red')
		self.win.text_view.modify_fg(gtk.STATE_NORMAL, color2)	
		## Bottom Scrolling ## Start#

		self.win.text_more = self.win.text_view.get_buffer()
#	        self.win.text_more.set_text("string") 

#		self.win.mark = self.win.text_more.create_mark("end", self.win.text_more.get_end_iter())
#	        self.win.text_view.scroll_to_mark(self.win.mark, 0)
#		self.win.text_view.queue_draw()
#        	self.win.text_more.delete_mark_by_name("end") 
		## Bottom Scrolling ## End#
		
		self.string=""
		
		self.win.text_more.set_text("Nothing to Show")
#		print self.win.text_more.get_text(self.win.mark,0)
#		self.win.text_more.set_text("<b><big>Waiting for output...</big></b>")
#		self.win.text_more.set_use_markup(True)
		
	
		#Dialog Info
		self.win.dialog_info=mainGlade.get_widget("dialog_noserver")
		self.win.dialog_info.set_title("Server Info")
		self.win.dialog_info.butt_close=mainGlade.get_widget("butt_close")
		self.win.dialog_info.butt_close.connect("clicked",self.Dia_close)
		self.win.dialog_info.label=mainGlade.get_widget("label5")
		self.win.dialog_info.label.set_use_markup(True)
		self.win.dialog_info.logoimage=mainGlade.get_widget("image5")
		self.win.dialog_info.logoimage.set_from_file("py-tightvnc.png")	
		
		self.win.dialog_info.connect("delete_event",self.close_dialog)
		self.win.dialog_info.hide()

		#Dialog About
		self.win.dialog_about=mainGlade.get_widget("dialog_about")
		self.win.dialog_about.set_title("About")
		self.win.dialog_about.butt_close=mainGlade.get_widget("butt_close1")
		self.win.dialog_about.butt_close.connect("clicked",self.Dia_close_about)
		self.win.dialog_about.label_i=mainGlade.get_widget("label23")
		self.win.dialog_about.label_i.set_text("<b>Py-ThightVnc - http://pytightvnc.sourceforge.net</b>")
		self.win.dialog_about.label_i.set_use_markup(True)
		self.win.dialog_about.label=mainGlade.get_widget("label24")
		self.win.dialog_about.label.set_use_markup(True)
		
		self.win.dialog_about.logoimage=mainGlade.get_widget("image1")
		self.win.dialog_about.logoimage.set_from_file("py-tightvnc.png")	
		self.win.dialog_about.connect("delete_event",self.close_dialog)
		self.win.dialog_about.hide()

		###############################################
		#     User Window
		###############################################
		
		#Button User Settings
		self.win.item_usr=mainGlade.get_widget("usritem")
		self.win.item_usr.connect("activate", self.view_usr)

		self.win.dialog_usr=mainGlade.get_widget("dialog_usr")
		self.win.dialog_usr.set_title("User Settings")
		self.win.dialog_usr.butt_cancel=mainGlade.get_widget("butt_cancel1")
		self.win.dialog_usr.butt_cancel.connect("clicked",self.undo_hide_usr)
		
		self.win.dialog_usr.butt_apply=mainGlade.get_widget("butt_apply1")
		self.win.dialog_usr.butt_apply.connect("clicked",self.Usr_apply)
		
		self.win.dialog_usr.butt_apply=mainGlade.get_widget("butt_ok")
		self.win.dialog_usr.butt_apply.connect("clicked",self.Usr_ok)

		self.win.dialog_usr.entryName=mainGlade.get_widget("entry_name")	
		self.win.dialog_usr.entryPass=mainGlade.get_widget("entry_pw")	
		self.win.dialog_usr.entryVPass=mainGlade.get_widget("entry_vpw")	

		self.win.dialog_usr.checkbutt_usr=mainGlade.get_widget("checkbutton_usr")
		self.win.dialog_usr.checkbutt_usr.set_active(True)
		self.win.dialog_usr.checkbutt_usr.connect('toggled',self.Usr_cancel)
		self.win.dialog_usr.IsSens="0"

		self.win.dialog_usr.table=mainGlade.get_widget("table3")
		self.win.dialog_usr.table.set_sensitive(False)

		self.Usr_name="none"
		self.Usr_pass="none"		
		self.Usr_vpass="none"		
	
		self.win.dialog_usr.connect("delete_event",self.undo_hide_usr)
		self.win.dialog_usr.hide()
		
		#Button Net Settings
		self.win.item_net=mainGlade.get_widget("netitem")
		self.win.item_net.connect("activate", self.view_net)

		self.win.dialog_net=mainGlade.get_widget("dialog_net")
		self.win.dialog_net.set_title("Network Settings")

		self.win.dialog_net.xdmcp_radio=mainGlade.get_widget("radiobutton1")
		self.win.dialog_net.xdmcp_entry=mainGlade.get_widget("entry1")
		self.win.dialog_net.http_radio=mainGlade.get_widget("radiobutton2")
		self.win.dialog_net.http_entry=mainGlade.get_widget("entry2")
		self.win.dialog_net.bhttp_radio=mainGlade.get_widget("radiobutton3")
		self.win.dialog_net.bhttp_entry=mainGlade.get_widget("entry3")

#		self.win.dialog_net.default_radio=mainGlade.get_widget("radiobutton4")
		
		self.win.dialog_net.checkbutt_net=mainGlade.get_widget("checkbutton_net")
		
		self.win.dialog_net.checkbutt_net.set_active(True)
		self.win.dialog_net.checkbutt_net.connect('toggled',self.Net_cancel)
		self.win.dialog_net.IsSens="0"

		self.win.dialog_net.table=mainGlade.get_widget("alignment_net")
		self.win.dialog_net.table.set_sensitive(False)

		self.Xdmcp="none"
		self.Http="none"
		self.Bhttp="none"
		self.Netentry="none"

		self.win.dialog_net.butt_cancel=mainGlade.get_widget("butt_cancel2")
		self.win.dialog_net.butt_cancel.connect("clicked",self.undo_hide_net)

		self.win.dialog_net.butt_apply=mainGlade.get_widget("butt_apply2")
		self.win.dialog_net.butt_apply.connect("clicked",self.Net_apply)

		self.win.dialog_net.butt_ok=mainGlade.get_widget("butt_oknet")
		self.win.dialog_net.butt_ok.connect("clicked",self.Net_ok)

		self.win.dialog_net.connect("delete_event",self.undo_hide_net)
		self.win.dialog_net.hide()
		
		#Button Screen Settings
		self.win.item_scr=mainGlade.get_widget("screenitem")
		self.win.item_scr.connect("activate", self.view_scr)

		self.win.dialog_scr=mainGlade.get_widget("dialog_scr")
		self.win.dialog_scr.set_title("Screen Settings")
		
		self.win.dialog_scr.entrydesktop=mainGlade.get_widget("entry_desktop")		
		
		self.win.dialog_scr.checkbutt_scr=mainGlade.get_widget("checkbutton_scr")
		self.win.dialog_scr.checkbutt_scr.set_active(True)
		self.win.dialog_scr.checkbutt_scr.connect('toggled',self.Scr_cancel)
		self.win.dialog_scr.IsSens="0"
		
		self.win.dialog_scr.table=mainGlade.get_widget("table2")
		self.win.dialog_scr.table.set_sensitive(False)
		
		self.win.dialog_scr.entrywidth=mainGlade.get_widget("entry_width")		
		self.win.dialog_scr.entryheight=mainGlade.get_widget("entry_height")		

		self.win.dialog_scr.entrydepth=mainGlade.get_widget("entry_depth")		

		self.win.dialog_scr.entryred=mainGlade.get_widget("entry_RED")		
		self.win.dialog_scr.entrygreen=mainGlade.get_widget("entry_GREEN")		
		self.win.dialog_scr.entryblue=mainGlade.get_widget("entry_BLUE")		

		self.win.dialog_scr.Ashared=mainGlade.get_widget("radiobutton_alw")
		self.win.dialog_scr.Nshared=mainGlade.get_widget("radiobutton_nev")
#		self.win.dialog_scr.Dshared=mainGlade.get_widget("radiobutton_shdef")
		###control insert ####
		self.desktop_def="1"
		self.win.dialog_scr.entrydesktop.set_text(self.desktop_def)
		
		self.desktop=self.win.dialog_scr.entrydesktop.get_text()
		self.width="none"
		self.width_def="none"
		self.height="none"
		self.height_def="none"
		self.depth="none"
		self.depth_def="32"
		self.rgb="none"
		self.rgb_def="255255255"
		self.r="none"
		self.r_def="255"
		self.g="none"
		self.g_def="255"
		self.b="none"
		self.b_def="255"
		self.win.dialog_scr.entrydepth.set_text(self.depth_def)		
#		self.depth=self.win.dialog_scr.entrydepth.get_text()		
#		self.win.dialog_scr.entryred.set_text("255")		
#		self.win.dialog_scr.entrygreen.set_text("255")		
#		self.win.dialog_scr.entryblue.set_text("255")		
#		self.r=self.r_def
#		self.g=self.g_def
#		self.b=self.b_def
#		self.rgb=self.r+self.g+self.b
		self.Ashared="none"
		self.Nshared="none"
		
		self.win.dialog_scr.butt_cancel=mainGlade.get_widget("butt_cancel3")
		self.win.dialog_scr.butt_cancel.connect("clicked",self.undo_hide_scr)

		self.win.dialog_scr.butt_apply=mainGlade.get_widget("butt_apply3")
		self.win.dialog_scr.butt_apply.connect("clicked",self.Scr_apply)

		self.win.dialog_scr.butt_ok=mainGlade.get_widget("butt_okscr")
		self.win.dialog_scr.butt_ok.connect("clicked",self.Scr_ok)
		
		self.win.dialog_scr.connect("delete_event",self.undo_hide_scr)
		self.win.dialog_scr.hide()

		###############################################
			
		self.win.vbox2=mainGlade.get_widget("vbox2")		
		self.win.vbox_server = gtk.VBox()
		self.win.vbox2.add(self.win.vbox_server)
		
#		self.win.hbox21=mainGlade.get_widget("hbox21")		
#		self.win.vbox_desk = gtk.VBox()
#		self.win.hbox21.add(self.win.vbox_desk)
		self.win.label_second=mainGlade.get_widget("label22")			
		#self.win.vbox_desk.add(self.win.label_second)
		
		###############################################
				
		####################
		self.win.show_all()
#		self.win.scroll_text_more.hide()
#		self.win.text_more.hide()	
		
		################################################	
		################################################	
		################################################	
		self.count=[]

	def close_win(self,widget,data=0):
		self.win.hide()
		self.IsHide="1"
		return True
	def close_dialog(self,widget,data=0):
		widget.hide()
		return True
	def undo_usr(self, widget,data=0):
		if self.Usr_name=="none":
			self.win.dialog_usr.entryName.set_text("");
		else:
			self.win.dialog_usr.entryName.set_text(self.Usr_name)
			self.win.dialog_usr.checkbutt_usr.set_active(False)

		if self.Usr_pass=="none":
			self.win.dialog_usr.entryPass.set_text("");
		else:
			self.win.dialog_usr.entryPass.set_text(self.Usr_pass)
			self.win.dialog_usr.checkbutt_usr.set_active(False)

		if self.Usr_vpass=="none":
			self.win.dialog_usr.entryVPass.set_text("");
		else:
			self.win.dialog_usr.entryVPass.set_text(self.Usr_vpass)
			self.win.dialog_usr.checkbutt_usr.set_active(False)

		if self.Usr_name=="none" and self.Usr_pass=="none" and self.Usr_vpass=="none":
			self.win.dialog_usr.checkbutt_usr.set_active(True)
			self.win.dialog_usr.IsSens="0"
			self.win.dialog_usr.table.set_sensitive(False)


	def undo_hide_usr(self,widget,data=0):
		self.undo_usr(widget)
		self.win.dialog_usr.hide()
		return True

	def undo_net(self,widget,data=0):
		if self.Xdmcp=="none":
			self.win.dialog_net.xdmcp_entry.set_text("");
			self.win.dialog_net.xdmcp_radio.set_active(False);
		else:
			self.win.dialog_net.xdmcp_entry.set_text(self.Netentry);
			self.win.dialog_net.xdmcp_radio.set_active(True);
			self.win.dialog_net.checkbutt_net.set_active(False)
			
		if self.Http=="none":
			self.win.dialog_net.http_entry.set_text("");
			self.win.dialog_net.http_radio.set_active(False);
		else:
			self.win.dialog_net.http_entry.set_text(self.Netentry);
			self.win.dialog_net.http_radio.set_active(True);
			self.win.dialog_net.checkbutt_net.set_active(False)

		if self.Bhttp=="none":
			self.win.dialog_net.bhttp_entry.set_text("");
			self.win.dialog_net.bhttp_radio.set_active(False);
		else:
			self.win.dialog_net.bhttp_entry.set_text(self.Netentry);
			self.win.dialog_net.bhttp_radio.set_active(True);
			self.win.dialog_net.checkbutt_net.set_active(False)
		
		if self.Xdmcp=="none" and self.Http=="none" and self.Bhttp=="none":
			self.win.dialog_net.xdmcp_radio.set_active(True);

			self.win.dialog_net.checkbutt_net.set_active(True)
			self.win.dialog_net.IsSens="0"
			self.win.dialog_net.table.set_sensitive(False)
	
	def undo_hide_net(self,widget,data=0):
		self.undo_net(widget)
		self.win.dialog_net.hide()
		return True

	def undo_scr(self,widget,data=0):
	#	self.win.dialog_scr.entrydesktop.set_text(self.desktop_def)
		self.win.dialog_scr.entrywidth.set_text(self.width)           
                self.win.dialog_scr.entryheight.set_text(self.height)
		self.win.dialog_scr.entrydepth.set_text(self.depth_def);

		if self.desktop=="none":
			self.win.dialog_scr.entrydesktop.set_text(self.desktop_def)
		else:
			self.win.dialog_scr.entrydesktop.set_text(self.desktop)
	#		self.win.dialog_scr.checkbutt_src.set_active(False)
		
		if self.rgb=="none":
			self.win.dialog_scr.entryred.set_text("")
	                self.win.dialog_scr.entrygreen.set_text("")
        	        self.win.dialog_scr.entryblue.set_text("")
		else:
			self.win.dialog_scr.entryred.set_text(self.r)
	                self.win.dialog_scr.entrygreen.set_text(self.g)
        	        self.win.dialog_scr.entryblue.set_text(self.b)
			self.win.dialog_scr.checkbutt_src.set_active(False)
		
		if self.Ashared=="none":
			self.win.dialog_scr.Ashared.set_active(False)
		else:
			self.win.dialog_scr.Ashared.set_active(True)
#			self.win.dialog_scr.checkbutt_src.set_active(False)

                if self.Nshared=="none":
			self.win.dialog_scr.Nshared.set_active(False)
		else:
			self.win.dialog_scr.Nshared.set_active(True)
			self.win.dialog_scr.checkbutt_scr.set_active(False)
			
		if self.rgb=="none" and self.Nshared=="none" and self.desktop==self.desktop_def and self.depth==self.depth_def and self.width==self.width_def and self.height==self.height_def:
			self.win.dialog_scr.Ashared.set_active(True);

			self.win.dialog_scr.checkbutt_scr.set_active(True)
			self.win.dialog_scr.IsSens="0"
			self.win.dialog_scr.table.set_sensitive(False)
				
	def undo_hide_scr(self,widget,data=0):
		self.undo_scr(widget)			
		self.win.dialog_scr.hide()
		return True
		
		
#	def close_info(self,widget,data=0):
#		self.win.dialog_info.hide()
#		return True
#	def close_usr(self,widget,data=0):
#		self.win.dialog_usr.hide()
#		return True
#	def close_net(self,widget,data=0):
#		self.win.dialog_net.hide()
#		return True
#	def close_scr(self,widget,data=0):
#		self.win.dialog_scr.hide()
#		return True

	def connect(self,widget,data=0):
		a="vncserver"

		########### USER ###############################
		if self.desktop!="none":
			a=a+" :"+self.desktop
		if self.Usr_name!="none":
			a=a+" -name "+self.Usr_name

		if self.Usr_pass!="none":
			text = commands.getoutput("echo "+self.Usr_pass+" | vncpasswd -f > $HOME/.vnc/passwd")
			#text_old = self.win.text_more.get_text()	
			text_old = self.string
			self.string=text_old+"\n"+text
			self.win.text_more.set_text(self.string)
			self.scroll(widget)

		if self.Usr_vpass!="none":
			if self.Usr_pass!="none":
				text = commands.getoutput("echo "+self.Usr_vpass+" | vncpasswd -f >> $HOME/.vnc/passwd")
				#text_old = self.win.text_more.get_text()	
				text_old = self.string
				self.string=text_old+"\n"+text
				self.win.text_more.set_text(self.string)
				self.scroll(widget)
				
		
		########## SCREEN ##############################
		
		if self.width!="none":
			a=a+" -geometry "+self.width+"x"+self.height
		if self.depth!="none":
			a=a+" -depth "+self.depth
		if self.rgb!="none":
			a=a+" -pixelformat RGB"+self.rgb
		if self.Ashared!="none":
			a=a+" -alwaysshared"
		if self.Nshared!="none":		
			a=a+" -nevershared"
	
		########### NETWORK ############################
		if self.Xdmcp!="none":
			a="vncserver -query "+self.Netentry
		elif self.Http!="none":
			a=a+" -httpport "+self.Netentry
		elif self.Bhttp!="none":
			a=a+" -basehttpport "+self.Netentry
			
#		print a
#		os.system(a)
		text = commands.getoutput(a)
#		text_old = self.win.text_more.get_text()	
		text_old = self.string	
		self.string=text_old+"\n"+a+text
		self.win.text_more.set_text(self.string)
		self.scroll(widget)
	
		text_found=text.find("already")
		#print text_found
		if text_found!=-1:
#			print "ciao"			
			self.already_running(self,self.desktop)
		
		self.control(self)

	def scroll(self,widget,data=0):
		## Bottom Scrolling ## Start#
#		print "Sono scroll"
#		self.win.text_more = self.win.text_view.get_buffer()
#	        self.win.text_more.set_text("string") 

		self.win.mark = self.win.text_more.create_mark("end", self.win.text_more.get_end_iter())
#		self.iter=self.win.text_more.get_end_iter();
	        self.win.text_view.scroll_to_mark(self.win.mark,0)
#		print self.win.mark
        	self.win.text_more.delete_mark_by_name("end") 
		## Bottom Scrolling ## End#

	def info(self,widget):
		self.win.dialog_about.set_title("About")
		self.win.dialog_about.label.set_text("\n\nCreated By:\n\n<b>Moscato Giuseppe aka peppeska</b> - moscatog@yahoo.it - http://peppeska.altervista.org\n<b>Altamore Giovanni</b> - zzuncu@hotmail.com \n\nThis program is free software\n distributed under the terms of the GNU General Public License version 3")
		self.win.dialog_about.label.set_use_markup(True)
		self.win.dialog_about.show_all();
	
	def already_running(self,widget,data="NONE"):
		self.win.dialog_info.set_title("Error!")
		self.win.dialog_info.label.set_text("<b>Error!</b>\n\nA VNC server is already running as :"+data)
		self.win.dialog_info.label.set_use_markup(True)
		self.win.dialog_info.logoimage.set_from_stock(gtk.STOCK_DIALOG_ERROR,24)
		self.win.dialog_info.show_all();
		
				
#	def more(self,data="none"):
#		if self.win.butt_more.get_active():
#			print "attivo"
#			self.win.scroll_text_more.show_all()	
#		else:
#			print "non attivo"
#			self.win.scroll_text_more.hide()	

	def view_usr(self,widget):
		self.win.dialog_usr.show_all();
		
	def view_net(self,widget):
		self.win.dialog_net.show_all();

	def view_scr(self,widget):
		self.win.dialog_scr.show_all();
		
	def control(self,data="none"):
#		self.resolution()
		
		self.win.vbox_server.destroy()

		text_s = commands.getoutput("ls $HOME/.vnc/*.pid")
#		print(text_s)
		self.win.label_first.hide()
		self.win.label_first.set_text("<b>No active Desktops</b>")
		self.win.label_first.set_use_markup(True)
		self.win.label_first.show()
		self.count=[]
		p=re.compile('ls:*')
		m=p.search(text_s)
		active=""
		active_coll=[]
		if m:
##			self.win.hbox_server.hide_all()	
#			self.win.dialog_info.set_title("Server Info")
#			print("Nessun server Attivo")
			self.win.label_first.set_text("<b>No active Desktops</b>")
			self.win.label_second.set_text("")
			self.win.label_first.set_use_markup(True)
			self.tray.set_tooltip("No Active Desktops")
			self.win.dialog_scr.entrydesktop.set_text("1")
			self.win.button_killall.hide()
		else:	
			self.win.button_killall.show_all()
			self.win.vbox_server = gtk.VBox()
			
			self.win.vbox2.add(self.win.vbox_server)
			
			self.win.label_first.set_text("<b>Active Desktops</b>")
			self.win.label_first.set_use_markup(True)
			
			self.win.label_second.set_text("<b>Desktop</b>")
			self.win.label_second.set_use_markup(True)
	
			pid=text_s.splitlines()
#			print pid
			maxim=1
			for i in pid:
				pid2=i.split(":")
				pid3=pid2[1].rsplit(".")
				active_coll.append(int(pid3[0]))
				active_coll.sort()
#				print active_coll
				self.count.insert(0,int(pid3[0]))

			for elemento in active_coll:
				self.win.hbox_server = gtk.HBox(homogeneous=True)
			        self.win.vbox_server.pack_start(self.win.hbox_server, expand=False)

#				print elemento

				self.win.label_kill = gtk.Label("<b>"+str(elemento)+"</b>")
				self.win.label_kill.set_use_markup(True)

				self.win.hbox_server.add(self.win.label_kill)	
			
				self.win.butt_kill = gtk.Button("kill")
				self.win.butt_kill.connect("clicked",self.kill,str(elemento))
				self.win.butt_kill.set_size_request(80, 40)

				self.win.hbox_server.add(self.win.butt_kill)	
				
				self.win.hbox_server.show_all()

				active=active+"\n-> "+str(elemento)
				
			maxim=max(self.count)
			pid_desktop=maxim+1
			pid_desktop=str(pid_desktop)
#			print "Creato: "+maxim+" Prossimo: "+pid_desktop
			self.desktop=self.desktop_def=pid_desktop
#			print self.desktop_def
			self.win.dialog_scr.entrydesktop.set_text(self.desktop_def)
			self.tray.set_tooltip("Active Desktops: "+active)
		self.win.vbox_server.show()

	def killall(self,widget,data="none"):
		for i in self.count:
			pid=str(i)
			text = commands.getoutput("vncserver -kill :"+pid)
#			text_old = self.win.text_more.get_text()	
			text_old = self.string	
			self.string=text_old+"\n"+text
			self.win.text_more.set_text(self.string)
			self.scroll(widget)
#		self.count=[]
		self.desktop="none"	
		self.control(self)					

	def kill(self,widget,data="none"):
#		print data
		text = commands.getoutput("vncserver -kill :"+data)
#		text_old = self.win.text_more.get_text()	
		text_old = self.string	
		self.string=text_old+"\n"+text
		self.win.text_more.set_text(self.string)
		self.scroll(widget)
	
		self.desktop="none"	
		
#		self.count=[]
		
		self.win.hbox_server.destroy()
		
		self.control(self)


	def Dia_close(self,widget):
		self.win.dialog_info.hide();
	
	def Dia_close_about(self,widget):
		self.win.dialog_about.hide();
	
	def Usr_cancel(self,data="none"):
		if self.win.dialog_usr.IsSens=="0":
			### USER RESTORE ###
		#	self.Usr_name="none"
		#	self.Usr_pass="none"		
		#	self.Usr_vpass="none"		
		#	self.win.dialog_usr.entryName.set_text("")	
		#	self.win.dialog_usr.entryPass.set_text("")
			self.win.dialog_usr.table.set_sensitive(True)
			self.win.dialog_usr.IsSens="1"
		else:
			self.win.dialog_usr.table.set_sensitive(False)
			self.win.dialog_usr.IsSens="0"
			

#		self.win.dialog_usr.hide();	

	def Usr_apply(self,data="none"):
		self.Usr_name="none"
		self.Usr_pass="none"		
		self.Usr_vpass="none"	
		if self.win.dialog_usr.IsSens=="1":
			if self.win.dialog_usr.entryName.get_text()!="":
				self.Usr_name=self.win.dialog_usr.entryName.get_text()
			if self.win.dialog_usr.entryPass.get_text()!="":
				self.Usr_pass=self.win.dialog_usr.entryPass.get_text()	
			if self.win.dialog_usr.entryVPass.get_text()!="":
				self.Usr_vpass=self.win.dialog_usr.entryVPass.get_text()	
		#print self.Usr_name
		#print self.Usr_pass
		#print self.Usr_vpass

	def Usr_ok(self,widget):
		self.Usr_apply(self)
		self.win.dialog_usr.hide();	
	
	def Net_cancel(self,data="none"):
		if self.win.dialog_net.IsSens=="0":
			### NETWORK RESTORE ###
#			self.Xdmcp="none"
#			self.Http="none"
#			self.Bhttp="none"
#			self.Netentry="none"
	#		self.win.dialog_net.xdmcp_entry.set_text("")
	#		self.win.dialog_net.http_entry.set_text("")
	#		self.win.dialog_net.bhttp_entry.set_text("")
#			self.win.dialog_net.default_radio.set_active(True)

#			self.win.dialog_net.hide();
			self.win.dialog_net.table.set_sensitive(True)
			self.win.dialog_net.IsSens="1"
		else:
			self.win.dialog_net.table.set_sensitive(False)
			self.win.dialog_net.IsSens="0"

	def Net_apply(self,data="none"):
		self.Xdmcp="none"
		self.Http="none"
		self.Bhttp="none"
		self.Netentry="none"
		if self.win.dialog_net.IsSens=="1":
			if self.win.dialog_net.xdmcp_radio.get_active():
				self.Xdmcp=self.win.dialog_net.xdmcp_radio.get_active()
				if self.win.dialog_net.xdmcp_entry.get_text()!="":
					self.Netentry=self.win.dialog_net.xdmcp_entry.get_text()
						
			elif self.win.dialog_net.http_radio.get_active():
				self.Http=self.win.dialog_net.http_radio.get_active()
				if self.win.dialog_net.http_entry.get_text()!="":
					self.Netentry=self.win.dialog_net.http_entry.get_text()
	
			elif self.win.dialog_net.bhttp_radio.get_active():
				self.Bhttp=self.win.dialog_net.bhttp_radio.get_active()
				if self.win.dialog_net.bhttp_entry.get_text()!="":
					self.Netentry=self.win.dialog_net.bhttp_entry.get_text()
			#print self.Xdmcp
			#print self.Http
			#print self.Bhttp
			#print self.Netentry
		
	def Net_ok(self,widget):
		self.Net_apply(self)
		self.win.dialog_net.hide();

	def Scr_cancel(self,data="none"):
		### SCREEN  RESTORE ###
#		self.win.dialog_scr.entrydesktop.set_text("1")
		self.desktop=self.win.dialog_scr.entrydesktop.get_text()
#		self.width="none"
#		self.height="none"
		self.resolution(self)
		self.win.dialog_scr.entrydepth.set_text(self.depth_def)		
		self.depth=self.win.dialog_scr.entrydepth.get_text()		
#		self.win.dialog_scr.entryred.set_text("255")		
#		self.win.dialog_scr.entrygreen.set_text("255")		
#		self.win.dialog_scr.entryblue.set_text("255")		
#		self.rgb=self.win.dialog_scr.entryred.get_text()+self.win.dialog_scr.entrygreen.get_text()+self.win.dialog_scr.entryblue.get_text()		
		
		if self.win.dialog_scr.IsSens=="0":
#			self.Ashared="none"
#			self.Nshared="none"
	#		self.desktop="none"	
#			self.width="none"
#			self.height="none"
	#		self.depth="none"
#			self.rgb="none"
#			self.Ashared="none"
	#		self.Nshared="none"
#			self.win.dialog_scr.entrydesktop.set_text("")	
#			self.win.dialog_scr.entrywidth.set_text("")
#			self.win.dialog_scr.entryheight.set_text("")
#			self.win.dialog_scr.entrydepth.set_text("")
#			self.win.dialog_scr.entryred.set_text("")
#			self.win.dialog_scr.entrygreen.set_text("")
#			self.win.dialog_scr.entryblue.set_text("")
			self.win.dialog_scr.Ashared.set_active(True)
			
			self.win.dialog_scr.table.set_sensitive(True)
			self.win.dialog_scr.IsSens="1"
		else:
			self.win.dialog_scr.table.set_sensitive(False)
			self.win.dialog_scr.IsSens="0"
		
#			self.win.dialog_scr.hide();
	
	def Scr_apply(self,data="none"):
		self.desktop="none"	
	#	self.width="none"
	#	self.height="none"
		self.depth="none"
		self.rgb="none"
		self.r="none"
		self.g="none"
		self.b="none"
		self.Ashared="none"
		self.Nshared="none"
		if self.win.dialog_scr.IsSens=="1":
			if self.win.dialog_scr.entrydesktop.get_text()!="":
				self.desktop=self.win.dialog_scr.entrydesktop.get_text()
				#print self.desktop
			if self.win.dialog_scr.entrywidth.get_text()!="":
				if self.win.dialog_scr.entryheight.get_text()!="":
					self.width=self.win.dialog_scr.entrywidth.get_text()
					self.height=self.win.dialog_scr.entryheight.get_text()
					#print "width= "+self.width	
					#print "height= "+self.height
				else:
					print ("")
			if self.win.dialog_scr.entrydepth.get_text()!="":
				self.depth=self.win.dialog_scr.entrydepth.get_text()
				#print "depth= "+self.depth
			if self.win.dialog_scr.entryred.get_text!="":
				if self.win.dialog_scr.entrygreen.get_text()!="":
					if self.win.dialog_scr.entryblue.get_text()!="":
						self.r=self.win.dialog_scr.entryred.get_text()
						self.g=self.win.dialog_scr.entrygreen.get_text()
						self.b=self.win.dialog_scr.entryblue.get_text()
						self.rgb=self.r+self.g+self.b
						#print "RGB= "+self.rgb

			if self.win.dialog_scr.Ashared.get_active():
				self.Ashared=self.win.dialog_scr.Ashared.get_active()
			elif self.win.dialog_scr.Nshared.get_active():
				self.Nshared=self.win.dialog_scr.Nshared.get_active()
			#print self.Ashared			
			#print self.Nshared			
	
			
	
	def Scr_ok(self,widget):
		self.Scr_apply(self)
		self.win.dialog_scr.hide()

	def cancel(self, widget):
		self.Usr_cancel(self)
		self.Net_cancel(self)
		self.Scr_cancel(self)
	
	def quit(self, widget):
        	self.dialog = gtk.Dialog('Quit', self.win,
                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT, gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))
        
		self.dialog.set_property('allow-grow',0);
			
		self.dialog.vbox.pack_start(gtk.Label("Do you really want to quit?"))
        	
		self.dialog.show_all()
      		response = self.dialog.run()
		
        	if response == gtk.RESPONSE_ACCEPT:
            		return gtk.main_quit()
        	elif response == gtk.RESPONSE_REJECT:
            		self.dialog.destroy()
        	self.dialog.destroy()	

	def resolution(self, data="none"):
		text = commands.getoutput("xdpyinfo | grep dimensions")
		reso=text.split(":")
		reso2 = reso[1].split("x")
		reso2[0]=reso2[0].replace(' ','')
		reso2[1]=reso2[1].replace(' pi','')
		self.width_def=reso2[0]
		self.height_def=reso2[1]

		self.win.dialog_scr.entrywidth.set_text(self.width_def)	
		self.width=self.width_def	
		self.win.dialog_scr.entryheight.set_text(self.height_def)
		self.height=self.height_def
		#print self.width
	def tray_click(self, data="none"):
#		if self.event_box.button == 3 :
#		        menu.popup( None, None, None, 0, event.time );
#			self.traymenu.popup(None, None, gtk.status_icon_position_menu,2,1, self.tray)

		if self.IsHide==0:
			self.win.hide()
			self.IsHide=1
		else:
			self.win.show_all()
#			self.more()
			#self.win.scroll_text_more.hide()
			self.IsHide=0
			self.control(self)

	def message(self,data=None):
		"""
		Function to display messages to the user.
		"""
		msg=gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, data)
		msg.run()
		msg.destroy()

	def open_app(self,data=None):
		self.message(data)

	def close_app(self,data=None):
		self.message(data)
		gtk.main_quit()
	
	def make_menu(self,icon,event_button,event_time):
		menu = gtk.Menu()
    
#		open_item = gtk.MenuItem("Open App")
#		close_item = gtk.MenuItem()
		item_run = gtk.MenuItem("Create a Desktop")
		item_sep2 = gtk.SeparatorMenuItem()
		item_usr = gtk.MenuItem("User Settings")
		item_net = gtk.MenuItem("Network Settings")
		item_scr = gtk.MenuItem("Screen Settings")
		item_sep3 = gtk.SeparatorMenuItem()
		item_info = gtk.ImageMenuItem(stock_id=gtk.STOCK_ABOUT)
		item_sep = gtk.SeparatorMenuItem()
		item_close = gtk.ImageMenuItem(stock_id=gtk.STOCK_QUIT)
#		butt_close.connect("clicked",self.close_app)
#		run_item()
#		close_item.add(butt_close)		
    				
		
	
		#Append the menu items
#		menu.append(open_item)
		menu.append(item_run)
		menu.append(item_sep2)

		menu.append(item_usr)
		menu.append(item_net)
		menu.append(item_scr)
		
		menu.append(item_sep3)
		menu.append(item_info)

		menu.append(item_sep)
		menu.append(item_close)
    
		#add callbacks
#		open_item.connect_object("activate", self.open_app, "Open App")
		item_run.connect_object("activate",self.connect, "Close App")
		item_usr.connect_object("activate",self.view_usr,"User Settings")
		item_net.connect_object("activate",self.view_net,"Network Settings")
		item_scr.connect_object("activate",self.view_scr,"Screen Settings")
		item_info.connect_object("activate",self.info, "About")
		item_close.connect_object("activate",self.quit, "Close App")
    		
		#Show the menu items
		item_run.show()
		item_sep2.show()
		item_usr.show()
		item_net.show()
		item_scr.show()
		item_sep3.show()
		item_info.show()
		item_sep.show()
		item_close.show()
    
		#Popup the menu
		menu.popup(None, None, None,event_button,event_time)

	def on_right_click(self,data,event_button,event_time):
		self.make_menu(self,event_button,event_time)
	
	def refresh(self):
		while True:
			self.control(self)
			print "ciao"
			time.sleep(1)
		
	def main(self):
		if __name__ == '__main__':
#			icon = gtk.status_icon_new_from_stock(gtk.STOCK_ABOUT)
#			icon.connect('popup-menu', self.on_right_click)
#			icon.connect('activate', self.tray_click)
			self.tray.connect("activate", self.tray_click)
			self.tray.connect('popup-menu', self.on_right_click)
			gtk.main()
			self.win.label_first.set_text("CiaoVa")

if __name__ == "__main__" :
	m = FirstDialog()
	m.control()
	m.resolution()
	m.main()
