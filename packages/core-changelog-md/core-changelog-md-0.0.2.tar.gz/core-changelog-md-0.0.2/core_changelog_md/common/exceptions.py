class ChangeLogException(Exception): pass
class UnsupportedTagException(ChangeLogException): pass
class UnCorrectTitleException(ChangeLogException): pass


class MissedVersionsSymbolException(ChangeLogException): pass
class NotDetectVersionException(ChangeLogException): pass
class VersionOverTextException(ChangeLogException): pass
class VersionDateConvertException(ChangeLogException): pass
