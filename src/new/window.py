# window draws

# editor window
class EditorWindow(Fl_Double_Window) :
	search = ""
	def __init__(self, w, h, label) :
		Fl_Double_Window.__init__(self, w, h, label)

# set/update title
def set_title(win):
	global filename, title
	if len(filename) == 0:
		title = "Untitled"
	else:
		title = os.path.basename(filename)
	if changed:
		title = title+" (modified)"
	win.label(title)
