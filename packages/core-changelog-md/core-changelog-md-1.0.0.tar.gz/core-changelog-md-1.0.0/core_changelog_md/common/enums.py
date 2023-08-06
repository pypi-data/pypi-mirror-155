import enum
from typing import List

from core_changelog_md.common.exceptions import UnsupportedTagException


class ChangeTypes(enum.Enum):
    """
    Список возможных тегов (типов)
    Приоритет 1 - меняет patch версию
    Приоритет 0 - меняет minor версию
    major версия меняется только через метод bump
    """
    def __init__(self, values):
        self.tag = values['tag']
        self.priority = values['priority']

    FEATURED = {"tag": "Featured", "priority": 0}
    CHANGED = {"tag": "Changed", "priority": 0}
    FIXED = {"tag": "Fixed", "priority": 1}
    MISC = {"tag": "Misc", "priority": 1}

    @staticmethod
    def get_by_tag(tag: str) -> "ChangeTypes":
        """
        Поиск по тегу
        """
        for item in ChangeTypes:
            if item.tag.lower() == tag.lower():
                return item
        raise UnsupportedTagException(f'Tag "{tag}" not supported!')

    @staticmethod
    def get_by_type(change_type: "ChangeTypes") -> "ChangeTypes":
        """
        Поиск по типу
        """
        for item in ChangeTypes:
            if item == change_type:
                return item
        raise UnsupportedTagException(f'Type "{change_type}" not supported!')

    @staticmethod
    def accept_tag() -> List[str]:
        """
        Возвращает список доступных тегов
        """
        return [item.tag for item in ChangeTypes]
