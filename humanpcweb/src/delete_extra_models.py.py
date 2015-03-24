import os
import os.path

import urllib

__author__ = "facundoq"
__date__ = "$24/10/2011 09:16:12$"

def begins_model(line_with_number):
  line, number = line_with_number
  return line.startswith('MODEL')
def ends_model(line_with_number):
  line, number = line_with_number
  return line.startswith('ENDMDL')

def reduce_to_one_model(lines):
#    #beginings=filter(begins_model,lines_with_numbers)
#    endings=filter(ends_model,lines_with_numbers)
#    if (not(len(beginings) == len(endings)) or ((len(beginings)<=1) and(len(endings)<=1)) ):
#        return ''.join(lines)
#    else:
#        for i in range(1,len(beginings)):
#            line1,start=beginings[i]
#            line2,end=endings[i]
#            for j in range(start,end+1):
#                lines.pop(start)
#
#        return ''.join(lines)
  deleting = False
  added_first = False
  result = ""
  for line in lines:
    if(added_first):
      if(deleting):
        if(line.startswith('ENDMDL')):
          deleting = False
      else:

        if(line.startswith('MODEL')):
          deleting = True
        else:
          result += line
    else:
      result += line
      if(line.startswith('ENDMDL')):
        added_first = True
  return result
def reduce_file_to_one_model(filepath, output):
  outfile = open(filepath, 'r+')
  lines = [line for line in outfile]
  content = reduce_to_one_model(lines)
  outfile.close()
  outfile = open(output, 'w')
  outfile.write(content)
  outfile.close()
def reduce_files_to_one_model(folder, output_folder):
  if not os.path.isdir(folder):
    raise Exception("path %s is not a folder" % (folder))
  if not os.path.exists( output_folder):
    os.makedirs(output_folder)
  if not os.path.isdir(output_folder):
    raise Exception("path %s is not a folder" % (output_folder))
  domain_files = os.listdir(folder)
  for domain_file in domain_files:
    output_path = os.path.join(output_folder, domain_file)
    filepath=os.path.join(folder, domain_file)
    if not os.path.isdir(filepath):
      print "Reducing %s ..." % (filepath)
      reduce_file_to_one_model(filepath, output_path)
      print "Done"
    else:
      print  "Ignoring  %s " % (filepath)

if __name__ == "__main__":
  folder = "F:\\sharedhome\\NetBeansProjects\\humanpcweb\\samples\\datasets\\edvin-4levels\\proteins"
  output_folder = "F:\\sharedhome\\NetBeansProjects\\humanpcweb\\samples\\datasets\\edvin-4levels\\proteins\\small\\"
  folder= "proteins"
  output_folder= "proteins\\small\\"
  reduce_files_to_one_model(folder, output_folder)
  

