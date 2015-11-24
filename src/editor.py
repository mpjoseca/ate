import wx
import os.path

class MainWindow( wx.Frame ):
    def __init__( self, filename = '*.txt' ):
        super( MainWindow, self ).__init__( None, size = ( 800,640 ) )
        self.filename = filename
        self.dirname = '.'

        self.panel = wx.Panel( self, -1 )

        self.CreateInteriorWindowComponents()

        sizer = wx.BoxSizer()
        sizer.Add( self.multiText, proportion = 1, flag = wx.CENTER|wx.EXPAND )
        self.panel.SetSizer( sizer )

        self.CreateExteriorWindowComponents()

        self.multiText.Bind( wx.EVT_KEY_UP, self.updateLineCol )
        self.multiText.Bind( wx.EVT_LEFT_DOWN, self.updateLineCol )

    def CreateInteriorWindowComponents( self ):
        self.multiText = wx.TextCtrl( self.panel, style = wx.TE_MULTILINE )

    def updateLineCol( self, event ):
        l,c = self.multiText.PositionToXY( self.multiText.GetInsertionPoint() )

        stat = "col=%s, row=%s" % ( l,c )

        self.StatusBar.SetStatusText( stat, number = 0 )

        event.Skip()

    def CreateExteriorWindowComponents( self ):
        self.CreateMenu()
        self.CreateStatusBar()
        self.SetTitle()

    def CreateMenu( self ):
        fileMenu = wx.Menu()
        for id, label, helpText, handler in \
            [( wx.ID_OPEN, '&Open', 'Open a new file', self.OnOpen ),
             ( wx.ID_SAVE, '&Save', 'Save the current file', self.OnSave ),
             ( wx.ID_SAVEAS, 'Save &As', 'Save the file under a different name',
                self.OnSaveAs ),
             ( None, None, None, None ),
             ( wx.ID_EXIT, 'E&xit', 'Terminate the program', self.OnExit )]:
            if id == None:
                fileMenu.AppendSeparator()
            else:
                item = fileMenu.Append( id, label, helpText )
                self.Bind( wx.EVT_MENU, handler, item )

        editMenu = wx.Menu()
        for id, label, helpText, handler in \
            [( wx.ID_COPY, '&Copy', 'Copy selected text', self.OnCopy ),
             ( wx.ID_PASTE, '&Paste', 'Paste clipboard text', self.OnPaste )]:
            if id == None:
                editMenu.AppendSeparator()
            else:
                item = editMenu.Append( id, label, helpText )
                self.Bind( wx.EVT_MENU, handler, item )

        aboutMenu = wx.Menu()
        for id, label, helpText, handler in \
            [( wx.ID_ABOUT, '&About', 'Information about this program',
                self.OnAbout )]:
            if id == None:
                aboutMenu.AppendSeparator()
            else:
                item = aboutMenu.Append( id, label, helpText )
                self.Bind( wx.EVT_MENU, handler, item )

        menuBar = wx.MenuBar()
        menuBar.Append( fileMenu, '&File' ) # Add the fileMenu to the MenuBar
        menuBar.Append( editMenu, '&Edit' )
        menuBar.Append( aboutMenu, '&About' )
        self.SetMenuBar( menuBar )  # Add the menuBar to the Frame

    def SetTitle( self ):
        super( MainWindow, self ).SetTitle( 'ATE %s'%self.filename )

    # helper methods

    def defaultFileDialogOptions( self ):
        return dict( message = 'Choose a file', defaultDir = self.dirname,
            wildcard = '*.*' )

    def askUserForFilename (self, **dialogOptions ):
        dialog = wx.FileDialog( self, **dialogOptions )
        if dialog.ShowModal() == wx.ID_OK:
            userProvidedFilename = True
            self.filename = dialog.GetFilename()
            self.dirname = dialog.GetDirectory()
            self.SetTitle()
        else:
            userProvidedFilename = False
        dialog.Destroy()
        return userProvidedFilename

    # event handlers

    def OnAbout( self, event ):
        dialog = wx.MessageDialog( self, 'A sample editor\n'
            'in wxPython', 'About Sample Editor', wx.OK )
        dialog.ShowModal()
        dialog.Destroy()

    def OnExit( self, event ):
        self.Close()

    def OnSave( self, event ):
        if os.path.exists( self.filename ):
            self.OnSaveFile( event )
        else:
            self.OnSaveAs( event )

    def OnOpen( self, event ):
        if self.askUserForFilename( style = wx.OPEN, **self.defaultFileDialogOptions() ):
            textfile = open( os.path.join( self.dirname, self.filename ), 'r' )
            self.multiText.SetValue( textfile.read() )
            textfile.close()

    def OnSaveFile( self, event ):
        textfile = open( os.path.join( self.dirname, self.filename ), 'w' )
        textfile.write( self.multiText.GetValue() )
        textfile.close()

    def OnSaveAs( self, event ):
        if self.askUserForFilename( defaultFile = self.filename, style = wx.SAVE,
            **self.defaultFileDialogOptions() ):
            self.OnSaveFile( event )

    # clipboard functions, flush for other programs
    def OnCopy( self, event ):
        self.dataObj = wx.TextDataObject()
        self.dataObj.SetText( self.multiText.GetStringSelection() )
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData( self.dataObj )
            wx.TheClipboard.Flush()
        else:
            wx.MessageBox( "Unable to open the clipboard", "Error" )

    def OnPaste( self, event ):
        if wx.TheClipboard.Open():
            dataObj = wx.TextDataObject()
            success = wx.TheClipboard.GetData( dataObj )
            wx.TheClipboard.Flush()
            wx.TheClipboard.Close()
            if not success: return
            text = dataObj.GetText()
            if text: self.multiText.WriteText( text )

app = wx.App()
frame = MainWindow()
frame.Show()
app.MainLoop()
