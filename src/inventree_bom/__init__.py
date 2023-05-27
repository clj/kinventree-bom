try:
    from .inventree_bom_action import InventreeBom

    InventreeBom().register()
except ImportError:
    pass  # wx and pcbnew can't be imported when running tests
    # Would be nice to raise if not running tests
