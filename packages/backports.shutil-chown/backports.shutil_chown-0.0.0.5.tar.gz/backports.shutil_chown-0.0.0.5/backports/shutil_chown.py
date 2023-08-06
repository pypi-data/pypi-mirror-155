# Backport of shutil.chown from Python 3.3

from __future__ import absolute_import  # Import system's os, not backports.os

from shutil import _get_uid, _get_gid
import os

def backport_chown(path, user=None, group=None):
    """Change owner user and group of the given path.
    user and group can be the uid/gid or the user/group names, and in that case,
    they are converted to their respective uid/gid.
    """
    # sys.audit('shutil.chown', path, user, group)

    if user is None and group is None:
        raise ValueError("user and/or group must be set")

    _user = user
    _group = group

    # -1 means don't change it
    if user is None:
        _user = -1
    # user can either be an int (the uid) or a string (the system username)
    elif not isinstance(user, int):
        _user = _get_uid(user)
        if _user is None:
            raise LookupError("no such user: {!r}".format(user))

    if group is None:
        _group = -1
    elif not isinstance(group, int):
        _group = _get_gid(group)
        if _group is None:
            raise LookupError("no such group: {!r}".format(group))

    os.chown(path, _user, _group)

try:
    from shutil import chown
except ImportError:
    chown = backport_chown
