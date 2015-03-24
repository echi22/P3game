import sys

# 1) load environment dependent configuration variables from config.settings_local
# the file settings_local.py must never be committed to subversion
# Check out settings_local_example.py for an example file for settings_local.py
from config.settings_local import *

# 2) load environment-independent configuration variables for the application
settings_application_path=os.path.join( SETTINGS_PATH, "settings_application.py")
print  "Loading application settings from: "+settings_application_path
execfile(settings_application_path)

print BASE_PATH


PROJECT_PATH = os.path.normpath(os.path.join(BASE_PATH, '..'))
SRC_PATH = os.path.join(PROJECT_PATH, 'src')
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)
