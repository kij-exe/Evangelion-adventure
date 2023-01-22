import subprocesswd
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install("matplotlib")

import matplotlib