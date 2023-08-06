import datetime
import re
import packaging.version


class VersionCollection(dict):
    pass


class VersionBlock(object):
    RE_NUM_VERSION_BLOCK = re.compile(r'\[([0-9\.]+)\]')
    RE_VERSION_BLOCK = re.compile(r'\[([A-Za-z0-9])\]')

    def __init__(self, version, date, change_collection=None):
        self.change_blocks = change_collection
        self.version: packaging.version.Version = packaging.version.parse(version)
        self.date: datetime.datetime = date

    def __str__(self):
        return self.version.public

    def __gt__(self, other):
        if 'unreleased' in [self.version.base_version, other.version.base_version]:
            return other.version.base_version.lower() != 'unreleased'
        return self.version > other.version

    def __lt__(self, other):
        if 'unreleased' in [self.version.base_version.lower(), other.version.base_version.lower()]:
            return self.version.base_version.lower() != 'unreleased'
        return self.version < other.version

    def get_priority(self) -> int:
        """
        Возвращает приоритет поднятия версии согласно типам изменений
        Fixed, Misc (Приоритет 1) - меняет patch версию
        Featured, Changed (Приоритет 0) - меняет minor версию
        """
        return min([item.change_type.priority for item in self.change_blocks.values()])

    def text(self):
        """
        Возвращает приведенный к тексту элемент
        """
        result = f"## [{self.version.base_version.capitalize()}]"
        result = result + f' - {self.date.strftime("%Y-%m-%d")}\n' if self.date else result + '\n'
        for item in self.change_blocks:
            result += self.change_blocks[item].text()
        if self.version.public.lower() == 'unreleased':
            result += '\n---\n\n'
        else:
            result += '\n'
        return result
