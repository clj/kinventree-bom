try:
    from .dialog import BomDialog  # noqa
except ImportError as error:
    # wx and pcbnew can't be imported when running tests
    if error.name not in ["wx", "pcbnew"]:
        raise
