from __future__ import division
import ast
from datetime import *
from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.core import serializers
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils import simplejson
import json
import logging
import os
from random import random
from random import shuffle
from web import settings
from web.proteins.models import Classification
from web.proteins.models import Comparison
from web.proteins.models import ComparisonPercentage
from web.proteins.models import ComparisonPercentageProtein
from web.proteins.models import ComparisonProtein
from web.proteins.models import GameInstance
from web.proteins.models import Protein
from web.proteins.models import Score
from web.proteins.models import list_to_json
from web.utility import ClassLoader
logger = logging.getLogger(__name__)


def get_game_settings(request):
  result = '{"game_instances_per_level": %d,  "levels_per_game": %d, "game_instances_correct_to_level_up": %d }' % (settings.game_instances_per_level, settings.levels_per_game, settings.game_instances_correct_to_level_up)
  return HttpResponse(result, mimetype='application/json')

def minutes_since_last_time_played(request):
  try:
    last_comparison = Comparison.objects.filter(user=request.user).filter(game_instance__game=request.user.get_profile().game).order_by('ts').reverse()[0]
    diff = datetime.now() - last_comparison.ts
    diff = diff.seconds // 60 % 60
    return diff
  except Exception:     
    return 0
def consensus_game(request):
  #Comparison.objects.all().delete()  
  if request.user.is_anonymous():
    return HttpResponseRedirect('/users/login_or_register')
  if(Protein.objects.count() < 3):
    messages.error(request, "We are sorry, but the game hasn't been configured properly; our admins have been notified, the problem will be fixed in a short time.")
    return HttpResponseRedirect('/')
  if(minutes_since_last_time_played(request) > 120):
    profile = request.user.get_profile()
    profile.new_game()
  c = {"comparisons_needed": 5000000, "comparisons_made": Comparison.objects.count()}
  c.update(csrf(request))
  return render_to_response('consensus_game/play.html', c, context_instance=RequestContext(request))
  
def show_score(request):
  if request.user.is_anonymous():
    return HttpResponseRedirect('/users/login_or_register')
  game_scores = request.user.get_profile().get_scores_from_game(request.user.get_profile().game -1)
  #print game_scores
  c = {"game_scores": game_scores, "score":request.user.get_profile().get_points_from_game(request.user.get_profile().game -1)}
  c.update(csrf(request))
  return render_to_response('site/highscores.html', c, context_instance=RequestContext(request))
def get_user(request):
  try:
    return "" + request.META['HTTP_X_FORWARDED_FOR']
  except KeyError:
    return "AnonymousUser"

class ChooseProteinForm(forms.Form):
  selected = forms.IntegerField()
  game_instance = forms.IntegerField()
  order = forms.CharField(max_length=100)
def choose(request):  
  form = ChooseProteinForm(request.POST)
  if form.is_valid():
    selected = Protein.objects.get(id=form.cleaned_data["selected"])
    game_instance = form.cleaned_data["game_instance"]
    order = form.cleaned_data["order"]
    save_comparison(selected, game_instance, request.user, order)
    p = User.objects.get(id=request.user.id).get_profile()
    result = '{"profile": %s,  "score": %s }'  % (p.json(), p.get_score().json())
    return HttpResponse(result)
  return HttpResponse(status=400)
  

def save_comparison(selected, game_instance, user, order):
  game_instance = GameInstance.objects.get(id=game_instance)
  game_instance.times_played += 1
  game_instance.save()
  profile = user.get_profile()
  try:
    percentage = round((profile.get_correct_comparisons() * 100) / profile.proteins_compared(), 2)
  except ZeroDivisionError:
    percentage = 0
  c = Comparison(selected=selected, game_instance=game_instance, user=user, order=order, user_level=profile.user_level, accuracy=percentage)
  c.save()
  score = user.get_profile().get_score()
  score.chose(game_instance.choose(selected))
  score.save()


def get_game_instances_json(request):
  generator = ClassLoader().load(settings.game_instances_generator_module, settings.game_instances_generator_klass)()
  profile = request.user.get_profile()
  level = profile.level 
  game = profile.game
#  game_instances = list(generator.get_game_instances_not_played(game, level, request.user))
  game_instances = list();
  for x in range(level, 10):
    game_ins = list(generator.get_game_instances_not_played(game, x, request.user))
    game_instances.append(game_ins.pop())
#  shuffle(game_instances) 
  result = [game_instance.json2() for game_instance in game_instances]
  
  result = ",".join(result)
  result = "[" + result + "]"
  #print  " returning game instances..."
  return HttpResponse(result, mimetype='application/json')

class GetGameScore(forms.Form):
  level = forms.IntegerField()
  game = forms.IntegerField()
  
def get_game_score(request):
  form = GetGameScore(request.GET)
  if form.is_valid():
    level = form.cleaned_data['level']
    game = form.cleaned_data['game']
    game_score = Score.objects.get(user=request.user, level=level, game=game)
    result = game_score.json()
    return HttpResponse(result, mimetype='application/json')
  else:
    return HttpResponse(status=400)

class GameLevel(forms.Form):
  level = forms.IntegerField()
  game = forms.IntegerField()

class GameForm(forms.Form):
  game = forms.IntegerField()  
def get_game_score_for_game(request):
  form = GameForm(request.GET)
  print  "game"
  if form.is_valid():
    game = form.cleaned_data['game']
    result = get_game_score_previous_levels_json(request, game)      
    return HttpResponse(result, mimetype='application/json')
  else:
    return HttpResponse(status=400)
def get_game_score_for_user(profile): 
  try:
    percentage = round((profile.get_correct_comparisons() * 100) / profile.proteins_compared(), 2)
  except ZeroDivisionError:
    percentage = 0
  result = '{"best_score": "%d", "user_level": %d, "avg_score":%f}' % (profile.best_score_in_level, profile.user_level, percentage)
  return result 
def get_game_scores_for_user(request):
  profile = request.user.get_profile()    
  result = get_game_score_for_user(profile)     
  return HttpResponse(result, mimetype='application/json')

def get_game_scores_for_user_old(request):
  number_of_games = Score.objects.filter(user=request.user).order_by("-game")[0].game
  print number_of_games
  best_score = 0
  total_score = 0
  total_played = 0
  for i in range(0, number_of_games + 1):
    game_instances_played = 0
    game_instances_correct = 0    
    scores = Score.objects.filter(user=request.user, game=i)
    for s in scores:
      game_instances_played += s.game_instances_played
      game_instances_correct += s.game_instances_correct
    total_score += game_instances_correct    
    total_played += game_instances_played
    if(game_instances_correct > best_score):
      best_score = game_instances_correct
  result = '{"best_score": "%d", "total_score": %d,"avg_score": %f}' % (best_score, total_score, round(((total_score * 100) / total_played), 2))      
  return HttpResponse(result, mimetype='application/json')
          
def get_game_score_for_game_and_level(request):
  form = GameLevel(request.GET)
  if form.is_valid():
    print  "game on level"
    level = form.cleaned_data['level']
    game = form.cleaned_data['game']
    result = Score.objects.get(user=request.user, game=game, level=level).json()      
    return HttpResponse(result, mimetype='application/json')
  else:
    return HttpResponse(status=400)
def get_game_score_previous_levels_json(request, game):
  game_scores = request.user.get_profile().get_scores_from_game(game)    
  result = [game_score.json()for game_score in game_scores]
  result = ",".join(result)
  result = "[" + result + "]"
  return result
def get_comparison(request):
  form = GameLevel(request.GET)
  if form.is_valid():
    level = form.cleaned_data['level']
    game = form.cleaned_data['game']
    profile = request.user.get_profile()
    result = get_comparisons_json(profile, game, level)      
    return HttpResponse(result, mimetype='application/json')
  else:
    return HttpResponse(status=400)
def get_comparisons_json(profile, game, level):
  comparisons = profile.get_comparisons(game, level)    
  result = [comparison.json()for comparison in comparisons]
  result = ",".join(result)
  result = "[" + result + "]"
  return result

def show_highscore_table(request):
  scores = []
  newList = []
  for p in User.objects.all():      
        
    try:
      score = ast.literal_eval(get_game_score_for_user(p.userprofile))
      score["username"] = p.username
      scores.append(score)
    except:
      print ""      
  sorted_scores = sorted(scores, key=lambda k: (-k['user_level'], -k['avg_score']))
  c = {"sorted_scores":sorted_scores}
  c.update(csrf(request))
  print c
  return render_to_response('consensus_game/highscore_table.html', c, context_instance=RequestContext(request))