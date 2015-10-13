# ATE ( Ara Text Editor )
# main part

import fltk
import sys

# classes to import
import window.py

# main
textbuf = Fl_Text_Buffer()
style_init()

window = new_view()
window.show(1, sys.argv)

if len(sys.argv) > 1:
	load_file(sys.argv[1], -1)

Fl.run()
