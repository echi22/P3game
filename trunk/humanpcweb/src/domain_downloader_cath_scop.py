import os.path

import urllib

__author__ = "facundoq"
__date__ = "$24/10/2011 09:16:12$"

def download_domains(domains):
  base_URL = "http://astral.berkeley.edu/pdbstyle.cgi?"
  
  length= len(domains)
  i=0
  missing=[]
  for d in domains:
    d= "d"+d.strip()
    i=i+1
    parameters = "id=%s&output=text" % (d)
    URL = base_URL + parameters
    print  "Retrieving  %s from %s ( %d/ %d)" % (d, URL,i, length)
    try:
      urllib.urlretrieve (URL, d + ".pdb")
      print  "Done'"
    except:
      print  " error downloading domain  %s \n"  % (d)
      missing.append(d)
  return missing
    
def download_scop_cath_dataset():
  folder = "F:\sharedhome\NetBeansProjects\humanpcweb\samples\datasets\scop-cath"
  filename = "domain-names.txt";
  filepath = os.path.join(folder, filename);
#  missing=download_domains(list(open(filepath, 'r')))
#  print  " domains missing (could not be downloaded ):\n"
#  print  "\n".join (missing)
  download_domains([ "1itha_","1fcdc2","1p42a1"])

if __name__ == "__main__":
  download_scop_cath_dataset()

  
  
