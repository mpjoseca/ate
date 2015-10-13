import fltk
import sys

# global variables

changed = False
filename = ""
title = ""
textbuf = None
editor = None

# main window

class EditorWindow(Fl_Double_Window):
	search = ""
	def __init__(self, w, h, label):
		Fl_Double_Window.__init__(self, w, h, label)

# menubars and menus

menuitems = (( "&File",		0, 0, 0, FL_SUBMENU ),
		( "&New File",			0, new_cb ),
		( "&Open File...",		FL_CTRL + ord('o'), open_cb ),
		( "&Insert File...",	FL_CTRL + ord('i'), insert_cb, 0, FL_MENU_DIVIDER ),
		( "&Save File...",		FL_CTRL + ord('s'), save_cb ),
		( "&Save File &As...",	FL_CTRL + FL_SHIFT + ord('s'), saveas_cb, 0, FL_MENU_DIVIDER ),
		( "New &View",			FL_ALT + ord('v'), view_cb, 0 ),
		( "&Close View",		FL_CTRL + ord('w'), close_cb, 0, FL_MENU_DIVIDER ),
		( "E&xit",				FL_CTRL + ord('q'), quit_cb, 0),
		( None, 0 ),

	( "&Edit",	0, 0, 0, FL_SUBMENU ),
		( "Cu&t",		FL_CTRL + ord('x'), cut_cb),
		( "&Copy",		FL_CTRL + ord('c'), copy_cb),
		( "&Paste",		FL_CTRL + ord('v'), paste_cb),
		( "&Delete",	0, delete_cb ),
		( None, 0 ),

	( "&Search",		0, 0, 0, FL_SUBMENU ),
		( "&Find...",		FL_CTRL + ord('f'), find_cb ),
		( "F&ind Again",	FL_CTRL + ord('g'), find2_cb ),
		( "&Replace...",	FL_CTRL + ord('r'), replace_cb ),
		( "Re&place Again",	FL_CTRL + ord('t'), replace2_cb ),
		( None, 0 )
)

# editing the text

# add menus
m = Fl_Menu_Bar(0, 0, 660, 30);
m.copy(menuitems)

# text widget
w.editor = Fl_Text_Editor(0, 30, 660, 370);
w.editor.buffer(textbuf)

# track of changes
textbuf.add_modify_callback(changed_cb, w)
textbuf.call_modify_callbacks()

# mono-spaced font (FL_COURIER)
w.editor.textfont(FL_COURIER)

# replace dialog

self.replace_dlg = Fl_Window(300, 105, "Replace")	# replace dialog window
self.replace_find = Fl_Input(80, 10, 210, 25, "Find:")
self.replace_with = Fl_Input(80, 40, 210, 25, "Replace:")
self.replace_all = Fl_Button(10, 70, 90, 25, "Replace All")
self.replace_next = Fl_Return_Button(105, 70, 120, 25, "Replace Next")
self.replace_cancel = Fl_Button(230, 70, 60, 25, "Cancel")

# callbacks

# called whenever the user changes any text in the editor widget
def changed_cb(il, nInserted, nDeleted, i2, cl, editor):
	global changed, loading
	if (nInserted != 0 or nDeleted != 0) and loading == False:
		changed = True
	set_title(editor);	# set changed status in the title bar
	if loading:
		editor.editor.show_insert_position()

# kf_copy() to copy the clipboard text
def copy_cb(widget):
	global editor
	Fl_Text_Editor.kf_copy(0, editor.editor)

# kf_cut() to cut text
def cut_cb(widget):
	global editor
	Fl_Text_Editor.kf_cut(0, editor.editor)

# remove_selection() deletes current selected text
def delete_cb(widget):
	global textbuf
	textbuf.remove_selection()

# search string using the fl_input()
def find_cb(widget):
	global editor
	val = fl_input("Search String:", editor.search)
	if val != None:
		# User entered a string - go find it!
		editor.search = val
		find2_cb(widget)

# find next occurrence of the search string
def find2_cb(widget):
	global editor
	if editor.search[0] == 0:
		# Search string is blank; get a new one...
		find_cb(widget, editor)
		return

	pos = editor.editor.insert_position();
	(found, pos) = textbufl.search_forward(pos, editor.search);
	if found != 0:
		# Found a match; select and update the position...
		textbuf.select(pos, pos+len(editor.search))
		editor.editor.insert_position(pos+len(editor.search))
		editor.editor.show_insert_position()
	else:
		fl_alert("No occurrences of %s found!"%editor.search)

# new file
def new_cb(widget):
	global filename, changed
	if check_save() == 0:
		return
	filename = ""
	textbuf.select(0, textbuf.length())
	textbuf.remove_selection()
	changed = False
	textbuf.call_modify_callbacks()

# open file
def open_cb(widget):
	global filename
	if check_save() == 0:
		return
	newfile = fl_file_chooser("Open File?", "*", filename)
	if newfile != None:
		load_file(newfile, -1)

# kf_paste()
def paste_cb(widget):
	global editor
	Fl_Text_Editor.kf_paste(0, editor.editor)

# exit
def quit_cb(widget, data):
	global changed
	if changed and check_save() == 0:
		return
	sys.exit(0)

# replace dialog
def replace_cb(widget):
	global editor
	editor.replace_dlg.show()

# replace next occurrence
def replace2_cb(widget):
	global editor
	find = editor.replace_find.value()
	replace = editor.replace_with.value()

	if len(find) == 0:
		editor.replace_dlg.show()
		return

	editor.replace_dlg.hide()

	pos = editor.editor.insert_position()
	(found, pos) = textbuf.search_forward(pos, find)

	if found != 0:
		# Found a match; update the position and replace text...
		textbuf.select(pos, pos+len(find))
		textbuf.remove_selection()
		textbuf.insert(pos, replace)
		textbuf.select(pos, pos+len(replace))
		editor.editor.insert_position(pos+len(replace))
		editor.editor.show_insert_position()
	else:
		fl_alert("No occurrences of %s found!"%find)

# replace all occurences
def replall_cb(widget):
	global editor
	find = editor.replace_find.value()
	replaced = editor.replace_with.value()

	if len(find) == 0:
		editor.replace_dlg.show()
		return

	editor.replace_dlg.hide()
	editor.editor.insert_position(0)
	times = 0

	found = 1
	while found != 0:
		pos = editor.editor.insert_position()
		(found, pos) = textbuf.search_forward(pos, find)

		if found != 0:
			# Found a match; update the position and replace text...
			textbuf.select(pos, pos+len(find))
			textbuf.remove_selection()
			textbuf.insert(pos, replace)
			editor.editor.insert_position(pos+len(replace))
			editor.editor.show_insert_position()
			times += 1

		if times > 0:
			fl_message("Replaced %d occurrences."%times)
		else:
			fl_alert("No occurrences of %s found!"%find)

# hide replace dialog
def replcan_cb(widget):
	global editor
	editor.replace_dlg.hide()

# save file
def save_cb(widget):
	global filename
	if len(filename) == 0:
		# No filename - get one!
		saveas_cb()
		return
	else:
		save_file(filename)

# ask filename
def saveas_cb(widget, data):
	global filename
	newfile = fl_file_chooser("Save File As?", "*", filename)
	if newfile != None:
		save_file(newfile)

# Other functions

# check if current file needs to be saved
def check_save():
	global changed
	if not changed:
		return

	r = fl_choice("The current file has not been saved.\n"
					"Would you like to save it now?",
					"Cancel", "Save", "Don't Save")

	if r == 1:
		save_cb()
		return not changed

	if r == 2:
		return 1
	else:
		return 0

# load file to textbuf
loading = False
def load_file(newfile, ipos):
	global changed, loading, filename
	loading = True
	if ipos != -1:
		insert = 1
		changed = True
	else:
		insert = 0
		changed = True
	if insert == 0:
		filename = ""
		r = textbuf.loadfile(newfile)
	else:
		r = textbuf.insertfile(newfile, ipos)
	if r != 0:
		fl_alert("Error reading from file %s."%newfile)
	else:
		if insert == 0:
			filename = newfile
	loading = False
	textbuf.call_modify_callbacks()

# set title (updating)
def set_title(win):
	global filename, title
	if len(filename) == 0:
		title = "Untitled"
	else:
		title = os.path.basename(filename)
	if changed:
		title = title+" (modified)"
	win.label(title)

# main
textbuf = Fl_Text_Buffer()
style_init()

window = new_view()
window.show(1, sys.argv)

if len(sys.argv) > 1:
	load_file(sys.argv[1], -1)

Fl.run()
