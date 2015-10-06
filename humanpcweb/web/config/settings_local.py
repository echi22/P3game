#contains the settings for the local environment
#in this case, we are setting the path variables that depends on the local environment
#and importing the settings from the settings_local_dev_default.py file

import os.path

BASE_PATH='/home/hclass/webapps/p3tesina/humanpcweb/web/'
STATIC_PATH='/home/hclass/webapps/static_p3tesina/' #folder where the static files should be collected in
SETTINGS_PATH=os.path.join( BASE_PATH,"config/")


settings_path=os.path.join( SETTINGS_PATH, "settings_local_dev_default.py")
print  "Loading settings from: "+settings_path
execfile(settings_path)

