try:
    import pcbnew
except ImportError:
    pass  # Can't import when running tests


from ..vendored.inventree.part import BomItem
from ..vendored.inventree.part import Part
from ..vendored.natsort import natsorted


class InvalidReferenceError(Exception):
    pass


class Footprint:
    def __init__(self, ref, ipn):
        self.reference = ref
        self.ipn = ipn

    @classmethod
    def from_footprint(cls, footprint):
        return cls(
            footprint.GetReference().upper(), footprint.GetProperties().get("IPN")
        )


class BomBoard:
    def __init__(self, footprints, pcb_ipn):
        self._footprints = footprints
        self.pcb_ipn = pcb_ipn

        for footprint in footprints:
            if footprint.reference == "PCB":
                raise InvalidReferenceError(
                    "A footprint is using the reference PCB, which is reserved."
                )

    @classmethod
    def from_board(cls, board, *, pcb_ipn):
        footprints = [Footprint.from_footprint(fp) for fp in board.Footprints()]
        if not pcb_ipn:
            title_block = board.GetTitleBlock()
            project = board.GetProject()
            for i in range(10):
                text = pcbnew.ExpandTextVars(title_block.GetComment(i), project).strip()
                if text.startswith("PCB IPN:"):
                    pcb_ipn = text.split(":", 1)[1].strip()
                    break

        return cls(footprints, pcb_ipn)

    @property
    def footprints(self):
        return self._footprints + (
            [Footprint("PCB", self.pcb_ipn)] if self.pcb_ipn else []
        )

    @property
    def references(self):
        return set(fp.reference for fp in self.footprints)

    @property
    def ipns(self):
        return set(fp.ipn for fp in self.footprints)

    def references_for_ipn(self, ipn):
        return set(fp.reference for fp in self.footprints if fp.ipn == ipn)


class BomItems:
    def __init__(self, items, parts):
        self.items = items
        self.parts = parts

    @classmethod
    def from_part(cls, part, *, api):
        items = part.getBomItems()
        parts = {item.sub_part: Part(api, item.sub_part) for item in items}

        return cls(items, parts)

    @property
    def references(self):
        return set(item.reference for item in self.items)

    @property
    def ipns(self):
        return set(part.IPN for part in self.parts.values())

    def item_for_ipn(self, ipn):
        sub_part_pk = None
        for key, part in self.parts.items():
            if part.IPN == ipn:
                sub_part_pk = part.pk
                break
        else:
            raise RuntimeError(f"IPN: {ipn!r} not found")

        for item in self.items:
            if item.sub_part == sub_part_pk:
                return item
        else:
            raise RuntimeError(f"sub_part pk: {sub_part_pk!r} not found")

    def pk_for_ipn(self, ipn):
        return self.item_for_ipn(ipn).pk

    def references_for_ipn(self, ipn):
        return set(ref.strip() for ref in self.item_for_ipn(ipn).reference.split(","))


class Change:
    def __init__(self, ipn, refs, pk):
        self.ipn = ipn
        self.refs = refs
        self.pk = pk

    def __repr__(self):
        return f"{self.__class__.__name__}({self.ipn!r}, {self.refs!r}, {self.pk!r})"

    def __eq__(self, other):
        return self.ipn == other.ipn and self.refs == other.refs and self.pk == other.pk

    def __hash__(self):
        return hash((self.ipn, tuple(sorted(self.refs)), self.pk))

    def reference_str(self):
        return ", ".join(natsorted(self.refs))


class Create(Change):
    def execute(self, api):
        sub_part = Part.list(api, IPN=self.ipn)
        if not sub_part:
            raise RuntimeError(f"No sub_part found for ipn: {self.ipn}")
        if len(sub_part) > 1:
            raise RuntimeError(f"Multiple sub_parts found for ipn: {self.ipn}")

        BomItem.create(
            api,
            data={
                "part": self.pk,
                "sub_part": sub_part[0].pk,
                "reference": self.reference_str(),
                "quantity": len(self.refs),
            },
        )


class Update(Change):
    def execute(self, api):
        item = BomItem(api, pk=self.pk)
        item["reference"] = self.reference_str()
        item["quantity"] = len(self.refs)
        item.save()


class Delete(Change):
    def execute(self, api):
        # Don't use the pk kw arg here to avoid fetching data
        BomItem(api, data={"pk": self.pk}).delete()


class Ignore(Change):
    def __init__(self, refs):
        super().__init__(None, refs, None)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.refs!r})"

    def execute(self, api):
        pass


def process_changes(bom_board, bom_part, bom_items):
    changes = []

    # Ignored items
    if no_ipn_refs := bom_board.references_for_ipn(None):
        changes.append(Ignore(no_ipn_refs))

    # New bom items
    if new_ipns := bom_board.ipns.difference(bom_items.ipns):
        for new_ipn in new_ipns:
            if new_ipn is None:
                continue
            changes.append(
                Create(new_ipn, bom_board.references_for_ipn(new_ipn), bom_part.pk)
            )

    # Deleted bom items
    if deleted_ipns := bom_items.ipns.difference(bom_board.ipns):
        for deleted_ipn in deleted_ipns:
            changes.append(
                Delete(
                    deleted_ipn,
                    bom_items.references_for_ipn(deleted_ipn),
                    bom_items.pk_for_ipn(deleted_ipn),
                )
            )

    # Updated bom items
    candidate_ipns = bom_items.ipns.intersection(bom_board.ipns)
    for candidate_ipn in candidate_ipns:
        board_refs = bom_board.references_for_ipn(candidate_ipn)
        if board_refs != bom_items.references_for_ipn(candidate_ipn):
            changes.append(
                Update(candidate_ipn, board_refs, bom_items.pk_for_ipn(candidate_ipn))
            )

    return changes
