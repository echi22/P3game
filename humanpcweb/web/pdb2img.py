import os.path
import subprocess
import urllib
from subprocess import CalledProcessError
from compiler.pycodegen import TRY_FINALLY
from compiler.ast import TryExcept

__author__ = "facundoq"
__date__ = "$24/10/2011 09:16:12$"

class ConversionException(Exception):
  pass
       
def pdb2img(source_path, target_path, overwrite, format, script_path,size):
  size="%dx%d" % (size[0],size[1])
  options=[ "java", "-jar", script_path, source_path, target_path,  str (overwrite).lower(), format,size]
  try:
    output = subprocess.check_output(options)
    f = lambda l: (l.count("Processed")>0)
    important=filter( f,output.split("\n"))
    if (len(important)==0):
      return "Unknown error converting proteins"
    else:
      return important[0]
  except CalledProcessError as e:   
    raise ConversionException( "Error generating images (code "+ e.returncode +"), command: "+ " ".join(options))
  
#  return return_code;

if __name__ == "__main__":
  source_path= "F:\sharedhome\NetBeansProjects\pdb2img\proteins"
  target_path = "F:\sharedhome\NetBeansProjects\pdb2img\proteins\images2\\"
  overwrite=False
  format= "gif"
  size=(800,800)
  print pdb2img(source_path, target_path, overwrite, format,"../tools/pdb2img/pdb2img.jar",size)
  

  
  
