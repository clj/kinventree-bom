import os

import pcbnew
import wx.grid
import wx.propgrid

from .base import BomDialogBase
from .changes import BomBoard
from .changes import BomItems
from .changes import Create
from .changes import Delete
from .changes import Ignore
from .changes import process_changes
from .config import Config
from ..vendored.inventree.api import InvenTreeAPI
from ..vendored.inventree.part import Part
from ..vendored.inventree.part import PartCategory
from ..vendored.natsort import natsorted


def split_refs(refs):
    return refs.replace(",", " ").split()


class BomDialog(BomDialogBase):
    def __init__(self, /, filename=None):
        super().__init__(None)

        if filename:
            board = pcbnew.LoadBoard(filename)
        else:
            board = pcbnew.GetBoard()

        self.config = Config(os.path.dirname(board.GetFileName()))
        self.config.load_from_ini()

        property_names = set()
        for fp in board.Footprints():
            props = fp.GetProperties()
            property_names.update(props.keys())

        self.ipn_field_name.Append(sorted(property_names))

        self.board = board
        self.api = InvenTreeAPI(
            self.config.inventree_server,
            username=self.config.inventree_username,
            password=self.config.inventree_password,
        )

        if self.pre_process():
            self.process()

    def pre_process(self):
        result = True
        fetch_pca_ipns = False
        fetch_pcb_ipns = False

        project = self.board.GetProject()

        title_block = self.board.GetTitleBlock()
        for i in range(10):
            text = pcbnew.ExpandTextVars(title_block.GetComment(i), project).strip()
            if text.startswith("PCA IPN:"):
                pca_ipn = text.split(":", 1)[1].strip()
                self.pca_ipn.SetValue(pca_ipn)
                self.pca_ipn.Disable()
                break
        else:
            self.pca_ipn.Enable()
            # Somehow instruct user to enter a PCA IPN or add it to schematic

            result = False
            fetch_pca_ipns = True

        # for drawing in self.board.GetDrawings():
        #     if not isinstance(drawing, pcbnew.PCB_TEXT):
        #         continue
        #     text = drawing.GetShownText().strip()
        #     if text.startswith('PCB IPN:'):
        #         pcb_ipn = text.split(':', 1)[1].strip()

        #         self.pcb_ipn.SetValue(pcb_ipn)
        #         self.pcb_ipn.Disable()
        #         break
        # else:
        #     self.pcb_ipn.Enable()
        #     # Somehow instruct user to enter a PCB IPN or add it to schematic

        title_block = self.board.GetTitleBlock()
        for i in range(10):
            text = pcbnew.ExpandTextVars(title_block.GetComment(i), project).strip()
            if text.startswith("PCB IPN:"):
                pcb_ipn = text.split(":", 1)[1].strip()
                self.pcb_ipn.SetValue(pcb_ipn)
                self.pcb_ipn.Disable()
                break
        else:
            self.pcb_ipn.Enable()
            # Somehow instruct user to enter a PCA IPN or add it to schematic

            result = False
            fetch_pcb_ipns = True

        if fetch_pca_ipns or fetch_pcb_ipns:
            categories = PartCategory.list(self.api)

            if fetch_pca_ipns:
                pca_category = None
                for category in categories:
                    if category.name == self.config.inventree_pca_category:
                        pca_category = category.pk

                if pca_category:
                    parts = Part.list(self.api, category=pca_category)
                    for part in parts:
                        self.pca_ipn.Append(f"{part.IPN} - {part.description}", part)
                else:
                    pass  # Tell the user we could not find the category

            if fetch_pcb_ipns:
                pca_category = None
                for category in categories:
                    if category.name == self.config.inventree_pcb_category:
                        pcb_category = category.pk

                if pcb_category:
                    parts = Part.list(self.api, category=pcb_category)
                    for part in parts:
                        self.pcb_ipn.Append(f"{part.IPN} - {part.description}", part)
                else:
                    pass  # Tell the user we could not find the category

        return result

    def process(self):
        pca_ipn = self.pca_ipn.GetValue().strip()
        part = Part.list(self.api, IPN=pca_ipn)
        if not part:
            wx.MessageBox(
                f"No assembly with PCA IPN: {pca_ipn} found in InvenTree",
                "Error",
                wx.OK | wx.ICON_ERROR,
            )
            return
        part = part[0]

        pcb_ipn = self.pcb_ipn.GetValue().strip() or None

        bom_board = BomBoard.from_board(self.board, pcb_ipn=pcb_ipn)
        bom_items = BomItems.from_part(part, api=self.api)

        self.changed = process_changes(bom_board, part, bom_items)

        self.update_change_list()

    def update_change_list(self):
        self.changes.ClearColumns()
        col = self.changes.AppendTextColumn("IPN")
        col.SetWidth(wx.COL_WIDTH_AUTOSIZE)
        col = self.changes.AppendTextColumn("Change")
        col.SetWidth(wx.COL_WIDTH_AUTOSIZE)
        col = self.changes.AppendTextColumn("References")
        col = col.SetWidth(wx.COL_WIDTH_AUTOSIZE)

        rows = []
        for change in self.changed:
            row = [change.ipn]
            if isinstance(change, Create):
                row += ["New IPN"]
            elif isinstance(change, Delete):
                row += ["Removed IPN"]
            elif isinstance(change, Ignore):
                row += ["Refs without an IPN"]
            else:
                # XXX: Rather than just showing all refs, it could show
                # what ref was added or removed
                row += ["Changed IPN"]

            row += [change.reference_str()]

            rows.append(row)

        rows = natsorted(rows)

        for row in rows:
            self.changes.AppendItem(row)

    def updateButtonOnClick(self, event):
        self.changes.DeleteAllItems()
        self.process()

    def save(self):
        for change in self.changed:
            change.execute(self.api)

    def sendButtonOnCClick(self, event):
        self.save()

    def closeButtonOnClick(self, event):
        self.Close()

    def ipnOnComboBox(self, event):
        part = event.EventObject.GetClientData(event.GetSelection())
        event.EventObject.SetValue(part.IPN)
