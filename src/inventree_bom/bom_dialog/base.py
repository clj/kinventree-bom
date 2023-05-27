# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.dataview

###########################################################################
## Class BomDialogBase
###########################################################################

class BomDialogBase ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,623 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer5 = wx.BoxSizer( wx.VERTICAL )

        sbSizer4 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Settings" ), wx.HORIZONTAL )

        fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizer1.AddGrowableCol( 1 )
        fgSizer1.SetFlexibleDirection( wx.BOTH )
        fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_staticText1 = wx.StaticText( sbSizer4.GetStaticBox(), wx.ID_ANY, u"Field:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )

        self.m_staticText1.SetMinSize( wx.Size( 120,-1 ) )

        fgSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )

        bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

        ipn_field_nameChoices = []
        self.ipn_field_name = wx.ComboBox( sbSizer4.GetStaticBox(), wx.ID_ANY, u"IPN", wx.DefaultPosition, wx.DefaultSize, ipn_field_nameChoices, 0 )
        bSizer3.Add( self.ipn_field_name, 2, wx.ALL|wx.EXPAND, 5 )

        self.m_button2 = wx.Button( sbSizer4.GetStaticBox(), wx.ID_ANY, u"Update", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer3.Add( self.m_button2, 0, wx.ALL, 5 )


        fgSizer1.Add( bSizer3, 1, wx.EXPAND, 5 )

        self.m_staticText2 = wx.StaticText( sbSizer4.GetStaticBox(), wx.ID_ANY, u"PCA IPN:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )

        fgSizer1.Add( self.m_staticText2, 0, wx.ALL, 5 )

        pca_ipnChoices = []
        self.pca_ipn = wx.ComboBox( sbSizer4.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, pca_ipnChoices, wx.CB_SORT )
        fgSizer1.Add( self.pca_ipn, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText3 = wx.StaticText( sbSizer4.GetStaticBox(), wx.ID_ANY, u"PCB IPN:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )

        fgSizer1.Add( self.m_staticText3, 0, wx.ALL, 5 )

        pcb_ipnChoices = []
        self.pcb_ipn = wx.ComboBox( sbSizer4.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, pcb_ipnChoices, 0 )
        fgSizer1.Add( self.pcb_ipn, 0, wx.ALL|wx.EXPAND, 5 )


        fgSizer1.Add( ( 0, 0), 1, wx.EXPAND, 5 )


        sbSizer4.Add( fgSizer1, 1, wx.EXPAND, 5 )


        bSizer5.Add( sbSizer4, 0, wx.ALL|wx.EXPAND, 5 )

        sbSizer5 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Changes" ), wx.VERTICAL )

        self.changes = wx.dataview.DataViewListCtrl( sbSizer5.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        sbSizer5.Add( self.changes, 1, wx.ALL|wx.EXPAND, 5 )


        bSizer5.Add( sbSizer5, 1, wx.ALL|wx.EXPAND, 5 )

        bSizer6 = wx.BoxSizer( wx.HORIZONTAL )


        bSizer6.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_button3 = wx.Button( self, wx.ID_ANY, u"Send", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.m_button3, 0, wx.ALL, 15 )

        self.m_button4 = wx.Button( self, wx.ID_ANY, u"Close", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.m_button4, 0, wx.ALL, 15 )


        bSizer5.Add( bSizer6, 0, wx.EXPAND, 5 )


        self.SetSizer( bSizer5 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.m_button2.Bind( wx.EVT_BUTTON, self.updateButtonOnClick )
        self.pca_ipn.Bind( wx.EVT_COMBOBOX, self.ipnOnComboBox )
        self.pcb_ipn.Bind( wx.EVT_COMBOBOX, self.ipnOnComboBox )
        self.m_button3.Bind( wx.EVT_BUTTON, self.sendButtonOnClick )
        self.m_button4.Bind( wx.EVT_BUTTON, self.closeButtonOnClick )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def updateButtonOnClick( self, event ):
        event.Skip()

    def ipnOnComboBox( self, event ):
        event.Skip()


    def sendButtonOnClick( self, event ):
        event.Skip()

    def closeButtonOnClick( self, event ):
        event.Skip()
