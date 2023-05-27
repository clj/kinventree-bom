import os
import sys

import pcbnew
import wx

if __name__ == "__main__":
    # Circumvent the "scripts can't do relative imports because they are not
    # packages" restriction by asserting dominance and making it a package!
    dirname = os.path.dirname(os.path.abspath(__file__))
    __package__ = os.path.basename(dirname)
    sys.path.insert(0, os.path.dirname(dirname))
    __import__(__package__)

from inventree_bom.bom_dialog import BomDialog


class InventreeBom(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Inventree BOM"
        self.category = "BOM"
        self.description = "A plugin to create and sync BOMs for PCBs in InvenTree"
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(
            os.path.dirname(__file__), "inventree_out.png"
        )

    def Run(self):
        dlg = BomDialog()

        dlg.ShowModal()

        dlg.Destroy()


def main(filename):
    class InventreeBomApp(wx.App):
        def OnInit(self):
            frame = BomDialog(filename=filename)
            frame.SetSize(700, 500)
            if frame.ShowModal() == wx.ID_OK:
                print("Should generate bom")
            frame.Destroy()
            return True

    app = InventreeBomApp()
    app.MainLoop()

    print("Done")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Expected one argument (a .kicad_pcb file)")
    main(sys.argv[1])
