import pandas as pd
from pyxtal.symmetry import Group, Hall
import re
import numpy as np

def abc2matrix(abc):
    """
    convert the abc string representation to matrix
    Args:
        abc: string like 'a, b, c' or 'a+c, b, c' or 'a+1/4, b+1/4, c'

    Returns:
        4*4 affine matrix
    """
    rot_matrix = np.zeros((3, 3))
    trans = np.zeros(3)
    toks = abc.strip().replace(" ", "").lower().split(",")
    re_rot = re.compile(r"([+-]?)([\d\.]*)/?([\d\.]*)([a-c])")
    re_trans = re.compile(r"([+-]?)([\d\.]+)/?([\d\.]*)(?![a-c])")
    for i, tok in enumerate(toks):
        # build the rotation matrix
        for m in re_rot.finditer(tok):
            factor = -1.0 if m.group(1) == "-" else 1.0
            if m.group(2) != "":
                factor *= float(m.group(2)) / float(m.group(3)) if m.group(3) != "" else float(m.group(2))
            j = ord(m.group(4)) - 97
            rot_matrix[i, j] = factor
        # build the translation vector
        for m in re_trans.finditer(tok):
            factor = -1 if m.group(1) == "-" else 1
            num = float(m.group(2)) / float(m.group(3)) if m.group(3) != "" else float(m.group(2))
            trans[i] = num * factor
    return rot_matrix, trans

df = pd.read_csv('HM_Full.csv',sep=',')
spg = [int(tmp.split(':')[0]) for tmp in df['Spg_full']]
name = [] 
for tmp in df['Spg_full']:
    tmp0 = tmp.split(':')
    if len(tmp0) == 2:
        name.append(tmp0[1])
    else:
        name.append('abc')
perm = []
for s, n in zip(spg, name):
    if 2<s<16:
        if n[0]=='b' or n[:2]=='-b':
            perm.append(0)
        else:
            perm.append(1)
    elif 15<s<75:
        if n=='abc' or n=='1' or n=='2':
            perm.append(0)
        else:
            perm.append(1)
    else:
        perm.append(0)
print(perm)
df.insert(6, "Permutation", perm)
#df.insert(0, "Hall", list(range(1,531)))
#df.insert(1, "Spg_num", spg)
df.to_csv('HM_Full.csv', index=False)


