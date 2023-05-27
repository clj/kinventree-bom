import pytest

from inventree_bom.bom_dialog.changes import BomBoard
from inventree_bom.bom_dialog.changes import BomItems
from inventree_bom.bom_dialog.changes import Create
from inventree_bom.bom_dialog.changes import Delete
from inventree_bom.bom_dialog.changes import Footprint
from inventree_bom.bom_dialog.changes import Ignore
from inventree_bom.bom_dialog.changes import InvalidReferenceError
from inventree_bom.bom_dialog.changes import Update
from inventree_bom.bom_dialog.changes import process_changes
from inventree_bom.vendored.inventree.part import BomItem
from inventree_bom.vendored.inventree.part import Part

bom_part = Part(None, None, {"pk": 999, "IPN": "999"})


class TestBomBoard:
    def test_pcb_ref(self):
        with pytest.raises(InvalidReferenceError):
            BomBoard([Footprint("PCB", "111")], "222")


def test_empty():
    board = BomBoard([], None)

    assert process_changes(board, bom_part, BomItems([], {})) == []


def test_only_bcp():
    board = BomBoard([], "111")
    items = BomItems([], {})

    changes = process_changes(board, bom_part, items)
    assert changes == [Create("111", {"PCB"}, 999)]


@pytest.mark.parametrize(
    "footprints, expected",
    [
        ([Footprint("R1", "111")], [Create("111", {"R1"}, 999)]),
        (
            [Footprint("R1", "111"), Footprint("R2", "112")],
            [Create("111", {"R1"}, 999), Create("112", {"R2"}, 999)],
        ),
        (
            [Footprint("R1", "111"), Footprint("R2", "111")],
            [Create("111", {"R1", "R2"}, 999)],
        ),
        ([Footprint("R1", None)], [Ignore({"R1"})]),
    ],
)
def test_new(footprints, expected):
    board = BomBoard(footprints, None)
    items = BomItems([], {})

    changes = process_changes(board, bom_part, items)
    assert set(changes) == set(expected)


def test_delete():
    board = BomBoard([], None)
    items = BomItems(
        [
            BomItem(
                None,
                None,
                {"pk": 1, "reference": "D1", "quantity": 1, "part": 2, "sub_part": 3},
            )
        ],
        {3: Part(None, None, {"pk": 3, "IPN": "111"})},
    )

    changes = process_changes(board, bom_part, items)
    assert changes == [Delete("111", {"D1"}, 1)]


def test_update_add_ref():
    board = BomBoard([Footprint("D1", "111"), Footprint("D2", "111")], None)
    items = BomItems(
        [
            BomItem(
                None,
                None,
                {"pk": 1, "reference": "D1", "quantity": 1, "part": 2, "sub_part": 3},
            )
        ],
        {3: Part(None, None, {"pk": 3, "IPN": "111"})},
    )

    changes = process_changes(board, bom_part, items)
    assert changes == [Update("111", {"D1", "D2"}, 1)]


def test_update_remove_ref():
    board = BomBoard([Footprint("D1", "111")], None)
    items = BomItems(
        [
            BomItem(
                None,
                None,
                {
                    "pk": 1,
                    "reference": "D1, D2",
                    "quantity": 1,
                    "part": 2,
                    "sub_part": 3,
                },
            )
        ],
        {3: Part(None, None, {"pk": 3, "IPN": "111"})},
    )

    changes = process_changes(board, bom_part, items)
    assert changes == [Update("111", {"D1"}, 1)]


def test_update_add_and_remove_ref():
    board = BomBoard([Footprint("D1", "111"), Footprint("D3", "111")], None)
    items = BomItems(
        [
            BomItem(
                None,
                None,
                {
                    "pk": 1,
                    "reference": "D1, D2",
                    "quantity": 1,
                    "part": 2,
                    "sub_part": 3,
                },
            )
        ],
        {3: Part(None, None, {"pk": 3, "IPN": "111"})},
    )

    changes = process_changes(board, bom_part, items)
    assert changes == [Update("111", {"D1", "D3"}, 1)]
