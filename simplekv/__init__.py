#!/usr/bin/env python
# coding=utf8

class KeyValueStorage(object):
    """The smallest API supported by all backends.

    Keys are ascii-strings and guaranteed to be properly handled up to a
    length of at least 256 characters.

    Any function that takes a key as an argument raises a ValueError if the
    key is incorrect.
    """
    def get(self, key):
        """Returns the key data as a string.

        Raises a `KeyError` if the key does not exist.
        """
        self._check_valid_key(key)
        self._get(key)

    def put(self, key, data_or_readable):
        """Store into key

        Stores data into a key, from a string or "somewhat filelike" object.
        If the object has a .read() method, data will be read from it as if it
        was a file, otherwise the result of a str() conversion is stored
        instead.

        Note that the object only needs to support read() and _may_ support
        a fileno() method as well.

        Raises an `IOError` if storing failed.
        """
        self._check_valid_key(key)
        if hasattr(data_or_readable, 'read'):
            self._put_readable(key, data_or_readable)
        else:
            self._put_data(key, data)

    def open(self, key):
        """Open key for reading.

        Returns a read-only file-like object for reading a key.

        Raises an `IOError` if storing failed.
        """
        self._check_valid_key(key)
        self._open(key)

    def _check_valid_key(self, key):
        try:
            key.decode('ascii')
            return True
        except UnicodeDecodeError, e:
            raise ValueError(str(e))
