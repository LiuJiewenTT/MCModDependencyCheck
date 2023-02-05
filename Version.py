
class Version:
    ver: str
    VER_INCREASING = 1
    VER_EQUAL = 0
    VER_DECREASING = -1

    def __init__(self, ver: str):
        self.ver = ver

    def versionCompare(a: str, b: str):
        # This will automatically fits strs.
        # a < b, return 1
        # a == b, return 0
        # a > b , return -1
        if isinstance(a, Version):
            a = a.ver
        if isinstance(b, Version):
            b = b.ver
        l1 = a.split(sep='.')
        l2 = b.split(sep='.')
        len1 = len(l1)
        len2 = len(l2)
        len_min = min(len1, len2)
        flag: int = 0
        for i in range(0, len_min):
            if l1[i] > l2[i]:
                flag = -1
                break
            elif l1[i] < l2[i]:
                flag = 1
                break
        if flag == 0:
            if len1 == len2:
                pass
            elif len_min == len1:
                # a < b
                flag = 1
            else:
                # a > b
                flag = -1
        return flag