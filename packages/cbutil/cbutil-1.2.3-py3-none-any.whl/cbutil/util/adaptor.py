__all__ = ['DictObjectAdaptor']

class DictObjectAdaptor:
    def __init__(self, o: object, keys = None):
        self.o = o
        if keys is None:
            self._keys = None
        else:
            self._keys = set(keys)

    def keys(self):
        if self._keys is None:
            return dir(self.o)
        else:
            return self._keys

    def items(self):
        for k in self.keys():
            yield k, getattr(self.o, k)

    def __getitem__(self, key):
        if self._keys is not None and key not in self._keys:
            raise KeyError
        return getattr(self.o, key)
            
    def __setitem__(self, key, value):
        if self._keys is not None:
            self._keys.add(key)
        setattr(self.o, key, value)

    def __delitem__(self, key):
        if self._keys is not None:
            del self._keys[key]
        delattr(self.o, key)

    def __contains__(self, key):
        if self._keys is not None:
            return key in self.keys
        else:
            return hasattr(self.o, key)

    def update(self, d: dict, cond=None):
        if cond is not None:
            for k, v in d.items():
                if cond(k, v):
                    self[k] = v
        for k, v in d.items():
            self[k] = v

    def get(self, key, default = None):
        if key in self:
            return self[key]
        else:
            return default
