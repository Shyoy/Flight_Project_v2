import os



if os.environ.get("ENV_NAME") == 'Production':
    print("os.environ:","Production")
    from .production import *

elif os.environ.get("ENV_NAME") == 'Stage':
    print("os.environ:","Stage")
    from .stage import *

else:
    print("os.environ:","Local")
    from .local import *