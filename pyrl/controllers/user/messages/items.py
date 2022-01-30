from __future__ import annotations

from collections.abc import Sequence

from pyrl.controllers.user.messages.generic import get_article
from pyrl.creature.item import Item

def item_description(items: Sequence[Item], *, use_verb: bool = False, use_article: bool = True) -> str:
    if len(items) == 1:
        verb = "is"
        description = f"{items[0].name}"
        article = get_article(description)
    elif 1 < len(items) <= 10:
        verb = "are"
        description = "several items"
        article = ""
    else:
        verb = "is"
        description = "collection of items"
        article = "a"
    article = f"{article} " if use_article else ""
    verb = f"{verb} " if use_verb else ""
    return f"{verb}{article}{description}"
