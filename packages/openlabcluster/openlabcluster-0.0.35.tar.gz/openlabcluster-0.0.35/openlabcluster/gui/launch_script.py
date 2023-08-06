
import os
from os.path import dirname as dirname
import wx

# TODO MOISHE FIGURE OUT WHATS WRONG
import sys
print(sys.path)
sys.path.insert(1, dirname(dirname(dirname(os.path.realpath(__file__)))))

from openlabcluster.gui.create_new_project import Create_new_project
from openlabcluster.gui.welcome import Welcome
from openlabcluster.utils import auxiliaryfunctions


class MainFrame(wx.Frame):
    def __init__(self):
        # initilaize main frame
        displays = (
            wx.Display(i) for i in range(wx.Display.GetCount())
        )  # Gets the number of displays
        screenSizes = [
            display.GetGeometry().GetSize() for display in displays
        ]  # Gets the size of each display
        index = 0  # For display 1.
        screenWidth = screenSizes[index][0]
        screenHeight = screenSizes[index][1]
        self.gui_size = (screenWidth * 0.9, screenHeight * 0.85)

        wx.Frame.__init__(
            self,
            None,
            wx.ID_ANY,
        "OpenLabCluster",
            size=wx.Size(self.gui_size),
            pos=wx.DefaultPosition,
            style=wx.RESIZE_BORDER | wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL,
        )

        # initialize statusbar to show status of points
        self.statusBar = wx.StatusBar(self, -1)
        self.SetStatusBar(self.statusBar)
        self.statusBar.SetFont( wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.NORMAL))
        self.statusBar.SetMinHeight(30)
        self.statusBar.SetBackgroundColour((175, 255, 212, 156))
        # set font size
        self.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL, False, 'MS Shell Dlg 2'))
        dlcparent_path = auxiliaryfunctions.get_deeplabcut_path()

        self.SetSizeHints(
            wx.Size(self.gui_size)
        )  #  This sets the minimum size of the GUI. It can scale now!
        # Here we create a panel and a notebook on the panel
        self.panel = wx.Panel(self)
        self.nb = wx.Notebook(self.panel, style=wx.NB_TOP)
        # create the page windows as children of the notebook and add the pages to the notebook with the label to show on the tab
        page1 = Welcome(self.nb, self.gui_size)
        self.nb.AddPage(page1, "Welcome")

        page2 = Create_new_project(self.nb, self.gui_size, self.statusBar)
        self.nb.AddPage(page2, "Manage Project")

        self.sizer = wx.BoxSizer()
        self.sizer.Add(self.nb, 1, wx.EXPAND)
        self.panel.SetSizer(self.sizer)

def  launch_dlc():
    app = wx.App()
    frame = MainFrame().Show()
    app.MainLoop()

if __name__ == '__main__':

    app = wx.App()
    frame = MainFrame().Show()
    app.MainLoop()
