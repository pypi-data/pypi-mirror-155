from typing import List

from core_changelog_md.common.enums import ChangeTypes


class ChangeCollection(dict):
    pass


class ChangeBlock(object):
    def __init__(self, change_type):
        self.change_type: ChangeTypes = change_type
        self.changes: List[str] = []

    def text(self):
        """
        Возвращает приведенный к тексту элемент
        """
        result = f'### {self.change_type.tag.capitalize()}\n'
        result += ''.join([f"- {item}\n" for item in self.changes])
        return result
