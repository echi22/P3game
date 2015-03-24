import os.path

import urllib

__author__ = "facundoq"
__date__ = "$24/10/2011 09:16:12$"

class Classification:
  @staticmethod
  def from_string(s):
    identifiers = s.strip().split(".")
    if len(identifiers) != 4:
      raise Exception("A classification string should have four identifiers separated by .")
    return Classification(identifiers[0], identifiers[1], identifiers[2], identifiers[3])

  def __init__(self, clas, fold, superfamily, family):
    self.clas = clas
    self.fold= fold
    self.superfamily = superfamily
    self.family = family
  def __str__(self):
    return  ".".join([self.clas, self.fold, self.superfamily, self.family])


class Domain:
  def __init__(self, code, classification):
    self.code = code
    self.classification = classification
  def __str__(self):
    return self.code + "(%s)" % ("unknown" if self.classification == None else str (self.classification))
  def generate_classification_string(self):
#    generate classification string in the format: d1ahdp_,a,a.4,a.4.1,a.4.1.1
    if self.classification == None:
      classifications= [ "Unknown"]*4
    else:
      classification= self.classification
      clas=classification.clas
      fold=clas+ "."+ classification.fold
      superfamily= fold+ "."+ classification.superfamily
      family= superfamily+ "."+ classification.family
      classifications=[clas, fold, superfamily, family ]

    return  ",".join ([self.code]+ classifications)

def parse_domain_classification(classification):
  domains = []
  current_classification = None
  for line in classification:
    line = line.split("\n")[0].strip()
    if len(line) > 0:
      if line.count("(") > 0:
        classification_string = line.split("(")[0].strip()
        try:
          current_classification = Classification.from_string(classification_string)
        except Exception:
          current_classification = None
      else:
        code = line.strip()
        domain = Domain(code, current_classification)
        domains.append(domain)
  return domains

def process_domain_classification(filepath):
  s = open(filepath, 'r')
  return parse_domain_classification(s)

def download_domains(domains):
  base_URL = "http://astral.berkeley.edu/pdbstyle.cgi?"
  for d in domains:
    parameters = "id=%s&output=text" % (d.code)
    URL = base_URL + parameters
    print  "Retrieving  %s from %s" % (d, URL)
    urllib.urlretrieve (URL, d.code + ".pdb")
    print  "Done"
def generate_classification_strings(domains):
  results=[]
  for domain in domains:
    results.append(domain.generate_classification_string())
  return results
    
def download_edvin_dataset():
  folder = "F:\sharedhome\NetBeansProjects\humanpcweb\samples\datasets\edvin-4levels"
  filename = "4_2_2_2_16_all_scop_random_set.txt";
  filepath = os.path.join(folder, filename);
  domains = process_domain_classification(filepath)
  print  "\n".join (generate_classification_strings(domains))

if __name__ == "__main__":
  download_edvin_dataset()

  
  
