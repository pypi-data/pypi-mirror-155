import hashlib


class MD5:
    @staticmethod
    def get(b):
        m = hashlib.md5()
        m.update(b)
        return m.hexdigest()
