import os



if os.environ.get("ENV_NAME") == 'Production':
    print("os.environ:","Production")
    from .production import *

elif os.environ.get("ENV_NAME") == 'Staging':
    print("os.environ:","Staging")
    from .staging import *

else:
    print("os.environ:","Local")
    from .local import *