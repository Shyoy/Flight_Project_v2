import os







print("os.environ: ENV_NAME =", os.environ.get("ENV_NAME"))


if os.environ.get("ENV_NAME") == 'Production':
    
    from .production import *
else:
    from .local import *