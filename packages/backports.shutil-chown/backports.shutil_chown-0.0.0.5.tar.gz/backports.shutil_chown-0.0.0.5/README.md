```py
try:
    from shutil import chown
except ImportError:
    from backports.shutil_chown import chown
```
