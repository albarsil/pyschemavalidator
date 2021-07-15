class BaseParameter(object):

    def __init__(self, key, keytype, innertype, isrequired, max, min, constrain):
        self._key = key
        self._keytype = keytype
        self._innertype = innertype
        self._isrequired = isrequired
        self._max = max
        self._min = min
        self._constrain = constrain

    @property
    def key(self):
        return self._key

    @property
    def keytype(self):
        return self._keytype

    @property
    def innertype(self):
        return self._innertype

    @property
    def isrequired(self):
        return self._isrequired

    @property
    def defaultValue(self):
        return self._defaultValue

    @property
    def max(self):
        return self._max

    @property
    def min(self):
        return self._min

    @property
    def constrain(self):
        return self._constrain