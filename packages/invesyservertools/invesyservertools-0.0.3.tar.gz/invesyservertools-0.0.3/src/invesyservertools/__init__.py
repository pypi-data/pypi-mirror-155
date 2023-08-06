import os
from pathlib import Path

package_path = os.path.split(
    os.path.realpath(__file__)
)[0]

files = os.listdir(package_path)

for file in files:
    module = Path(file).stem

    if not module.endswith('tools'):  # specific to this package
        continue

    exec(
        f'from .{module} import *'
    )
