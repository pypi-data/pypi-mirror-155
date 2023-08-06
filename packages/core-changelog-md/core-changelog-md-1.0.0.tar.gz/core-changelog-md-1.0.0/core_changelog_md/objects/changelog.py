import datetime
import re
from typing import Optional, List

import packaging.version

from core_changelog_md.common.enums import ChangeTypes
from core_changelog_md.common.exceptions import UnCorrectTitleException, \
    MissedVersionsSymbolException, VersionOverTextException, NotDetectVersionException, VersionDateConvertException
from core_changelog_md.objects.changes import ChangeCollection, ChangeBlock
from core_changelog_md.objects.version import VersionCollection, VersionBlock


class Changelog(object):
    RE_VERSION_RAW_BLOCK = re.compile(r'##[^#]?(\[.+\]?.+$)', flags=re.MULTILINE)
    RE_CHANGELOG_NAME = re.compile(r'^#[^#]\s*?(.+)[\s]*$', flags=re.MULTILINE)

    def __init__(self, name='CHANGELOG', path=None):
        self.name: str = name
        self.path: Optional[str] = path
        self._versions: VersionCollection[VersionBlock] = VersionCollection()

    @property
    def unreleased(self) -> VersionBlock:
        """
        Возвращает версию с нерелизными изменениями
        """
        return self._versions["unreleased"]

    @property
    def versions(self) -> List[VersionBlock]:
        """
        Возвращает список версий отсортированных от большего к меньшему
        :return:
        """
        return sorted(list(self._versions.values()), reverse=True)

    @staticmethod
    def check_version_date(version_name: str) -> Optional[datetime.datetime]:
        """
        Возвращает дату версии в формате YYYY.MM.DD
        """
        _version_name = version_name.replace(" ", "")
        if '-' not in _version_name and len([item for item in _version_name.split("]") if item.strip()]) != 1:
            raise VersionOverTextException()

        if ']-' not in _version_name and len([item for item in _version_name.split("]") if item.strip()]) != 1:
            raise VersionOverTextException()

        if "-" not in _version_name:
            return None
        split = _version_name.split('-', maxsplit=1)
        try:
            return datetime.datetime.strptime(split[-1].strip(), "%Y-%m-%d")
        except Exception as e:
            raise VersionDateConvertException()

    @staticmethod
    def check_version_name(version_name: str) -> str:
        """
        Возвращает имя версии
        """
        _version_name = version_name.replace(" ", "")
        if not _version_name.startswith("##") or \
                _version_name.startswith("##") and _version_name.startswith("###") or \
                "[" not in _version_name and "]" not in _version_name:
            raise MissedVersionsSymbolException()

        if not _version_name.startswith('##['):
            raise MissedVersionsSymbolException(
                f'Version title must be "## [x.x.x]" or "## [version_name]"\nActual" {_version_name}')
        if '[unreleased]' in _version_name.lower():
            version = 'unreleased'
        else:
            versions = VersionBlock.RE_NUM_VERSION_BLOCK.findall(_version_name)
            version = versions[0] if len(versions) == 1 else None
        if not version:
            versions = VersionBlock.RE_NUM_VERSION_BLOCK.findall(_version_name)
            version = versions[0] if len(versions) == 1 else None
        if version:
            return version
        raise NotDetectVersionException(f"Cant detect version name from '{_version_name}'")

    @staticmethod
    def check_name(name_block: str) -> str:
        """
        Возвращает имя ChangeLog
        """
        _name_block = name_block.replace(" ", '')
        if not _name_block.startswith("#") or _name_block.startswith("#") and _name_block.startswith("##"):
            raise UnCorrectTitleException()
        return name_block.replace("#", "").strip()

    @classmethod
    def from_file(cls, path):
        obj = Changelog.from_str(data_string=open(path, 'r', encoding='UTF8').read(), file_path=path)
        obj.path = path
        return obj

    @classmethod
    def from_str(cls, data_string: str, file_path: str = None):
        """
        Преобразование текста changelog в объект
        """

        # Первая строчка должна быть именем
        clean_data = [item.strip() for item in data_string.replace("---", '').split('\n') if item.strip()]
        obj = cls(name=Changelog.check_name(clean_data[0]))
        clean_data = clean_data[1:]

        # Разбиваем на версии
        for item in clean_data:
            # Старт обработки новой версии
            if item.strip().startswith("##") and not item.strip().startswith("###"):
                version = Changelog.check_version_name(version_name=item)
                obj._versions[version] = VersionBlock(
                    version=version,
                    date=Changelog.check_version_date(version_name=item),
                    change_collection=ChangeCollection()
                )
                change_block = None
                continue
            # Старт обработки нового change-block
            elif item.strip().startswith("###"):
                change_tag = ChangeTypes.get_by_tag(tag=item.replace("#", '').strip())
                obj._versions[version].change_blocks[change_tag] = ChangeBlock(change_type=change_tag)
                continue
            elif item.strip().startswith("-"):
                obj._versions[version].change_blocks[change_tag].changes.append(item.strip()[1:].strip())
            else:
                raise NotImplementedError
        return obj

    @property
    def current_version(self) -> VersionBlock:
        """
        Возвращает текущую версию Changelog
        """
        if len(self._versions) > 1:
            return max(list(self._versions.values())[1:])
        return self.unreleased

    @property
    def next_version(self) -> str:
        """
        Возвращает строковый идентификатор возможной следующей версии
        """
        a = self.unreleased.get_priority()
        v = self.current_version if self.current_version.__class__.__name__ != "LegacyVersion" else \
            packaging.version.parse('0.0.0')

        if a == 0:
            return f'{v.version.major}.{v.version.minor + 1}.0'
        else:
            return f'{v.version.major}.{v.version.minor}.{v.version.micro + 1}'

    @property
    def has_unreleased_changes(self):
        """
        Возвращает True если в секции unreleased есть changes
        """
        if len(self.unreleased.change_blocks):
            for item in self.unreleased.change_blocks:
                if len(self.unreleased.change_blocks[item].changes) > 0:
                    return True
        return False

    def add(self, version: VersionBlock):
        """
        Добавляет версию в changelog
        """
        self._versions.update({version.version.base_version: version})

    def save(self, path: str = None):
        """
        Сохраняет changelog в файл. Если указан путь то по нему, если нет - то по адресу открытия
        :param path: Путь для нового сохранения
        """
        path = path if path else self.path
        if path:
            with open(path, 'w', encoding='UTF8') as fp:
                fp.write(self.text())

    def text(self):
        """
        Возвращает текстовое представление changelog
        """
        result = f'#{self.name.upper()}\n'
        for item in self.versions:
            result += item.text()
        return result.strip() + '\n'
