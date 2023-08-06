import importlib
import os
import sys


def add_sys_path(path):
    sys.path.insert(0, path)


def del_sys_path(path, max=-1, cmp=None):
    if not cmp:
        cmp = lambda l, r: l == r
    tmp = []
    cnt = 0
    for p in sys.path:
        if 0 <= max <= cnt:
            break
        if not cmp(p, path):
            tmp.append(p)
            cnt += 1
    sys.path = tmp


class TmpSysPath(object):

    def __init__(self, path=None):
        super(TmpSysPath, self).__init__()
        self.__path = os.path.abspath(path) if path is not None else None

    def __enter__(self):
        if self.__path is not None:
            add_sys_path(self.__path)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__path is not None:
            del_sys_path(self.__path)


def import_module(name, package=None, path=None):
    with TmpSysPath(path):
        return importlib.import_module(name, package)


def _resolve_name(name, package, level):
    import importlib._bootstrap as bs
    bs._sanity_check(name, package, level)
    if level > 0:
        return bs._resolve_name(name, package, level)
    else:
        return name


def _import_object(name):
    tokens = name.split(".")
    is_module = True
    mod = importlib.import_module(tokens[0])
    for tk in tokens[1:]:
        if is_module:
            try:
                mod = importlib.import_module(f".{tk}", mod.__name__)
            except:
                is_module = False
        if not is_module:
            mod = getattr(mod, tk)
    return mod


def import_object(name, package=None, path=None):
    level = 0
    if name.startswith('.'):
        if not package:
            msg = ("the 'package' argument is required to perform a relative "
                   "import for {!r}")
            raise TypeError(msg.format(name))
        for character in name:
            if character != '.':
                break
            level += 1
    name = _resolve_name(name[level:], package, level)
    with TmpSysPath(path):
        return _import_object(name)
