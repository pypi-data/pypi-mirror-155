__all__ = ["styles"]


import pathlib
from typing import Dict


__here__ = pathlib.Path(__file__).parent
styles_dir = __here__ / "styles"
styles: Dict[str, Dict[str, str]] = dict()


for path in styles_dir.glob("**/*.qss"):
    name = path.parent.stem
    if name not in styles:
        styles[name] = dict()
    key = path.stem
    with open(path) as f:
        styles[name][key] = f.read().replace("%__here__%", path.parent.as_posix())
