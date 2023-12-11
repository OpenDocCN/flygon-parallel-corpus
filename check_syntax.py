import os
import yaml
from os import path

fnames = os.listdir('done')

for f in fnames:
    print(f)
    ff = path.join('done', f)
    yaml.safe_load(open(ff, encoding='utf8').read())