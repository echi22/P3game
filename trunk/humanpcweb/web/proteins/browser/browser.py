from django.http import HttpResponseRedirect
import random
from random import Random
from time import time

from datetime import datetime
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.template.context import RequestContext
from django.utils.itercompat import itertools
from web.proteins.models import Classification
from web.proteins.models import Protein
from web.proteins.models import UserProfile
from django.http import HttpResponse
from web.researcher.views import generate_image_from_proteins
from django.shortcuts import render_to_response

def id_parameter(func):
  def decorated(request):
    return func(request, request.GET["id"])
  return decorated


class Level():
  
  def __init__(self, id):
    self.images = self.get_images_for(id)
    self.id = id #self.normalize_id(id)

  def get_images_for(self, id):
    q = Classification.objects.filter(level4__startswith=id)
    amount = min(q.count(), 20)
    classifications = q[0:amount]
    return map(lambda c: c.protein, classifications)

  def get_images(self):
    q = Classification.objects.filter(level4__startswith=self.id)
    return map(lambda c: c.protein, q)

  def children(self):
    level = "level" + str(self.level() + 1)
    q = Classification.objects.filter(level4__startswith=self.id).values(level).distinct().order_by()
    child = self.child_constructor()
    return map(lambda c: child(c[level]), list (q))

  @staticmethod
  def all_children(levels):
    return itertools.chain.from_iterable(map(lambda level: level.children(), levels))
  
  @staticmethod
  def constructors():
    return [Class, Fold, SuperFamily, Family]

  def route(self):
    ''' generates a dictionary with the parents of the level (not including the level itself)'''
    codes = self.id.split(".")
    current_code = ""
    result = {}
    for i in range(0, len (codes)):
      current_code += codes[i]
      level = Level.constructors()[i](current_code)
      result[level.__class__.__name__] = level
      current_code += "."
    return result

class Root(Level):
  # not using this right now
  def __init__(self, id):
    self.images = []
    self.id = id
  def level(self):
    return 0
  def child_constructor(self):
    return Class
  def children(self):
    return map(lambda id: Class(id), ["a", "b", "c", "d"])

class Class(Level):
  @staticmethod
  def classes():
    return map(lambda id: Class(id), ["a", "b", "c", "d"])
  def level(self):
    return 1
  def child_constructor(self):
    return Fold

  
class Fold(Level):
  def level(self):
    return 2
  def child_constructor(self):
    return SuperFamily

class SuperFamily(Level):
  def level(self):
    return 3
  def child_constructor(self):
    return Family

class Family(Level):
  def children(self):
    raise Exception(" Families have no children levels")



def browse(request):
  c = map(lambda id: Class(id), ["a", "b", "c", "d"])
  return render_to_response('browser/browse.html', {"classes":c}, context_instance=RequestContext(request))


@id_parameter
def _class(request, id):
  c = Class.classes()
  _class = Class(id)
  f = _class.children()
  route = _class.route()
  print route
  return render_to_response('browser/class.html', {"classes":c, "folds":f, "class":_class}, context_instance=RequestContext(request))

@id_parameter
def fold(request, id):
  fold = Fold(id)
  route = fold.route()
  print route
  return render_to_response('browser/fold.html', {"route": route, "classes":Class.classes(), "level":fold}, context_instance=RequestContext(request))


@id_parameter
def superfamily(request, id):
  superfamily = SuperFamily(id)
  route = superfamily.route()
  context = {"route": route, "classes":Class.classes(), "level":superfamily}
  print context ["route"]
  return render_to_response('browser/superfamily.html', context, context_instance=RequestContext(request))

@id_parameter
def family(request, id):
  family = Family(id)
  route = family.route()
  context = {"route": route, "classes":Class.classes(), "level":family}
  return render_to_response('browser/family.html', context, context_instance=RequestContext(request))

@id_parameter
def protein(request, id):
  q=Protein.objects.filter(code=id)
  if(q.count()>0):
    protein=q[0]
    classification = Classification.objects.get(protein=protein.id)
    family = Family(classification.level4)
    route = family.route()
    context = {"route": route, "classes":Class.classes(), "protein":protein, "classification": classification}
    return render_to_response('browser/protein.html', context, context_instance=RequestContext(request))
  else:
    return HttpResponseRedirect('/browser')

def generate_images(request):
  generate_image_from_proteins()
  return HttpResponse("generated")