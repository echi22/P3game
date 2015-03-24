import os.path
import subprocess
import urllib

__author__ = "facundoq"
__date__ = "$24/10/2011 09:16:12$"

class ConversionException(Exception):
  pass

def pdb2img(source_path, target_path, overwrite, format, script_path):
  options=[ "java", "-jar", script_path, source_path, target_path,  str (overwrite), format]
  return_code= subprocess.call(options)
  if return_code!= 0:
    raise ConversionException( "Error generating images (code "+ str(return_code)+"), command: "+ " ".join(options))
  
#  return return_code;

if __name__ == "__main__":
  source_path= "F:\sharedhome\NetBeansProjects\pdb2img\proteins"
  target_path = "F:\sharedhome\NetBeansProjects\pdb2img\proteins\images2\\"
  overwrite=False
  format= "png"
  pdb2img(source_path, target_path, overwrite, format,"../tools/pdb2img/pdb2img.jar")
  

  
  
