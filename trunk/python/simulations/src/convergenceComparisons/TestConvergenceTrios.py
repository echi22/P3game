'''
Created on 05/03/2012

@author: facundoq
'''
import os
from numpy import *
import pygame, random
from pygame import Color
import copy
from mimetypes import init
from copy_reg import constructor
import time
from convergenceComparisons.TestConvergence import Element
from numpy.matlib import rand
from matplotlib.pyplot import pcolor
import numpy
from matplotlib import pyplot
from numpy.oldnumeric.rng import random_sample
from numpy.numarray import random_array
from numpy.oldnumeric.random_array import random_integers
from matplotlib import cm
import itertools

class DataGenerator():
  def generate(self,element_count):
    raise "Not Implemented"
  def title(self):
    raise "Not Implemented"

  def as_folder_name(self):
    raise "Not Implemented"


class PoissonDataGenerator(DataGenerator):
  def __init__(self, l):
    self.l = l
  def generate(self, element_count):
    return numpy.random.poisson(self.l, element_count)
  def title(self):
    return "Poisson(l=%d)" % (self.l)
  def as_folder_name(self):
    return "poisson-l-%04d" % (self.l)


class NormalDataGenerator(DataGenerator):
  def __init__(self, u,d):
    self.u=u
    self.d=d
  def generate(self, element_count):
    return numpy.random.normal(self.u,self.d,element_count)
  def title(self):
    return "Normal(%d,%04.1f)" % (self.u,self.d)
  def as_folder_name(self):
    return "normal-u%d-d%04.1f"  % (self.u,self.d)


class UniformDataGenerator(DataGenerator):
  def __init__(self, min,max):
    self.min=min
    self.max=max
    
  def generate(self, element_count):
    return numpy.random.uniform(self.min,self.max,element_count)
  def title(self):
    return "Uniform(%d,%04d)" % (self.min,self.max)
  def as_folder_name(self):
    return "uniform-%d-%04d"  % (self.min,self.max)

class SimulationData():
  def __init__(self, element_count, element_generator, votes_to_simulate,p):
    self.votes_to_simulate= votes_to_simulate
    self.element_generator = element_generator
    self.elements = sort(element_generator.generate(element_count))
    self.votes = zeros([element_count, element_count])
    self.appearences = zeros([element_count, element_count])
    self.distances = zeros([element_count, element_count])
    self.not_inspected = 0
    self.p=p
        

class Simulation():  
  
  def simulate_votes(self, sd):
    for trios in range(0, sd.votes_to_simulate):
      original_ti = numpy.random.randint(0, len(sd.elements), 3)
      ti = sort(original_ti)
      t = sd.elements[ti]
      if (random.random() <= sd.p): #vote correctly
        if (t[1] - t[0] < t[2] - t[1]):
          sd.votes[ti[0], ti[1]] += 1
        else:
          sd.votes[ti[1], ti[2]] += 1
      else: # vote incorrectly
        if (t[1] - t[0] > t[2] - t[1]):
          sd.votes[ti[0], ti[1]] += 1
        else:
          sd.votes[ti[1], ti[2]] += 1    
      sd.appearences[ti[0], ti[1]] += 1
      sd.appearences[ti[1], ti[2]] += 1
      sd.appearences[ti[0], ti[2]] += 1
      
  def distance_matrix(self, sd):
    for i in range(len(sd.elements)):
      for j in range(len(sd.elements)):
        if sd.appearences[i, j] > 0:
          sd.distances[i, j] = sd.votes[i, j] / sd.appearences[i, j]
        else:
          if (i < j):
            sd.not_inspected += 1
            #print (i, j)   

    
def set_figure_info(sd):
  cb = pyplot.colorbar()
  cb.set_label('mean value')
  xlabel= 'Similarity matrix for %d randomly selected numbers \n' % (len(sd.elements))
  xlabel+=  "from %s after %d votes, \n " % (sd.element_generator.title(),sd.votes_to_simulate)
  xlabel+= "with p=%0.2f of voting correctly" % (sd.p)
  pyplot.xlabel(xlabel)     

def save_figure(sd):
  directory="trios/%s/" % (sd.element_generator.as_folder_name())
  if not (os.path.exists(directory)):
    os.makedirs(directory)
  path= os.path.join(directory, ("p-%0.2f-votes-%07d.png" % (sd.p,sd.votes_to_simulate)))
  pyplot.savefig(path)

def generate_and_save_figure(sd):         
  print 'Clearing plot window...'
  pyplot.clf()
  print 'Plotting..'    
  pcolor(sd.distances)
  print 'Adding figure info..'        
  set_figure_info(sd)
  print "Saving figure.."
  save_figure(sd)
  
def run_simulation_iteration(sd, s, i):
  print 'Simulating votes..'
  s.simulate_votes(sd)
  print 'Calculating distance matrix..'    
  s.distance_matrix(sd)
  print "Pairs that where not inspected: %d of %d" % (sd.not_inspected, len(sd.elements) ** 2)
  generate_and_save_figure(sd)

def run_simulation(data_generator_parameters,data_generator_maker):
  s = Simulation()
  votes_to_simulate= [1000,10000,50000,100000]
  p=[0.3,0.6,0.9,1]
  parameters=list(itertools.product(data_generator_parameters,p,votes_to_simulate))
  for i in range(len(parameters)):
    parameter= parameters[i]
    print "\n********* Iteration %03d/%03d ******** " % (i+1,len(parameters))
    print "Generating simulation data (parameter: %s) ..." % (str(parameter))
    data_generator=  data_generator_maker(parameter[0])
    sd = SimulationData(200, data_generator,parameter[2],parameter[1])
    #print sd.elements
    run_simulation_iteration(sd, s, i)
  print "Done."
        
if __name__ == '__main__':
    import matplotlib as mpl
    mpl.rcParams['figure.figsize'] = (14,14)
    
    l = [1, 10, 50, 100];
    #run_simulation(l,lambda l: PoissonDataGenerator(l))
    min_max=[(0,10),(0,100),(0,1000),(0,100000)]
    #run_simulation(min_max,lambda min_max: UniformDataGenerator(min_max[0],min_max[1]))
    u_d=[(0,1.0),(0,0.5),(0,10.0),(0,1000.0)]
    run_simulation(u_d,lambda u_d: NormalDataGenerator(u_d[0],u_d[1]))
    

