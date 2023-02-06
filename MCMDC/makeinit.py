import os.path as osp
import os

dir = osp.dirname(__file__)
l = os.listdir(dir)
l2 = []
print(l)
for i in range(0, l.__len__()):
    if l[i] != 'makeinit.py' and l[i] != '__init__.py' and l[i] != 'main.py':
        t = l[i].rpartition('.')[0]
        if t != '':
            l2.append(t)
print(f'__all__ = {l2}')