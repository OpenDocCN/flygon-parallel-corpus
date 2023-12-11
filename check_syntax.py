import os
import yaml
from os import path

fnames = [
    f for f in os.listdir('done')
    if f.endswith('.yaml')
]

for f in fnames:
    print(f)
    ff = path.join('done', f)
    yaml.safe_load(open(ff, encoding='utf8').read())