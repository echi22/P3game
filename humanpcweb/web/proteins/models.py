from django.db.models import Sum
from web.utility import ClassLoader
from web.utility import Enumeration
from django.contrib.auth.models import User
from django.contrib.auth.models import UserManager
from django.core import serializers
from django.db import models
from django.db.models.fields.related import ManyToManyField
from django.db.models.fields.related import ManyToOneRel
#from Queue import join
from django.db.models.fields.related import OneToOneField

import settings
import itertools

# Create your models here.
class UserProfile(models.Model):
  user = models.OneToOneField(User)
  anonymous = models.BooleanField()
  game= models.IntegerField()
  #is the level of proteins (from 1 to 10) in wich the user is playing
  level= models.IntegerField()
  #is the real user level
  user_level = models.IntegerField()
  points =  models.IntegerField()
  birthday = models.DateField()
  knows_proteins = models.BooleanField()
  best_score_in_level = models.IntegerField()
  def json(self):
    anonymous = 'true' if self.anonymous else 'false'
    return '{ "user": %d, "anonymous": "%s", "proteins_compared": %d, "level": %d, "game": %d,"points": %d, "user_level":%d, "best_score_in_level":%d}'  % (self.user.id,anonymous, self.proteins_compared(),self.level,self.game,self.points,self.user_level,self.best_score_in_level)
  def proteins_compared(self):
    return Comparison.objects.filter(user=self.user).count()
  def get_correct_comparisons(self):
      return Score.objects.filter(user=self.user).aggregate(Sum('game_instances_correct'))["game_instances_correct__sum"]
  def get_score (self):
        return Score.objects.get(user=self.user, level=self.level, game=self.game)
  def get_scores_from_game(self,game):
      return Score.objects.filter(user=self.user).filter(game=game)
  def get_comparisons(self,game, level):
      return Comparison.objects.filter(user=self.user,game= game, level= level) 
  def get_points_from_game(self,game):
      game_scores = self.get_scores_from_game(game)
      points = 0
      for game_score in game_scores:
          points += game_score.game_instances_correct
      return points
  def new_game(self):
      self.game+=1
      self.level=0
      self.points = 0
      self.save()
      Score.for_user(self.user, self.game, self.level).save()    
  def reset_score(self):
      self.game=0
      self.level=0
      self.points = 0
      self.user_level = 0
      self.best_score_in_level = 0
      self.save()
      Score.for_user(self.user, self.game, self.level).save()
      
class Protein(models.Model):
  name = models.CharField(max_length=200)
  code = models.CharField(max_length=200)
  description = models.CharField(max_length=200)
  def scop_code(self):
    #detect astral codes
    if(len(self.code) == 7):
      return self.code[2:6]
    return self.code
  def cath(self):
      return  CathClassification.objects.get(protein=self)
  def scop(self):
      return  Classification.objects.get(protein=self)
  def json(self):
    scop= self.scop().json()
    cath=  self.cath().json()
    return '{"id": "%s", "description": "%s", "name": "%s", "code": "%s", "scop": %s, "cath": %s}'  % (self.id, self.description, self.name, self.code, scop, cath)
Result=Enumeration('Result',['win','tie','lose'])
class GameInstance(models.Model):
    different=models.ForeignKey(Protein,related_name="different")
    p1=models.ForeignKey(Protein,related_name="p1")
    p2=models.ForeignKey(Protein,related_name="p2")
    p3=models.ForeignKey(Protein,related_name="p3")
    level=models.IntegerField()
    game=models.IntegerField()
    times_played=models.IntegerField()
    ts=models.DateTimeField(auto_now_add=True)
    
    def proteins( self ):
      return [ self.p1, self.p2, self.p3]
    def __str__(self):
      return str(([  ("( "+p.name+ ","+Classification.objects.filter(protein=p)[0].level4+")") for p in self.proteins()]))

    def json( self ):
      classification1=Classification.objects.filter(protein=self.p1)[0]
      classification2=Classification.objects.filter(protein=self.p2)[0]
      classification3=Classification.objects.filter(protein=self.p3)[0]
      json_serializer = serializers.get_serializer("json")()
      json_serializer.serialize([self,self.p1,self.p2,self.p3,self.different,classification1,classification2,classification3], ensure_ascii=False)
      return json_serializer.getvalue()
    def get_different_according_to_cath(self):
        return ClassificationComparator(ClassificationComparator.CathClassification).get_different(self.p1,self.p2,self.p3)
    def json2(self):
        proteins=list_to_json([self.p1.json(),self.p2.json(),self.p3.json()])
        votes=list_to_json(map(lambda x:str(x),self.get_votes()))
        cath=self.get_different_according_to_cath()
        if cath != None:
            cath=cath.json()
        else:
            cath='"none"'
        result =  '{"id": %d, "game": %d, "level": %d, "proteins": %s, "votes"men called: %s, "scop": %s, "cath": %s}' % (self.id,self.game,self.level, proteins, votes, self.different.json(), cath)
        print result.replace("men called","")
        return result.replace("men called","")
    def get_votes(self):
        vote=[]
        vote.append(Comparison.objects.filter(game_instance=self).filter(selected=self.p1.id).count())
        vote.append(Comparison.objects.filter(game_instance=self).filter(selected=self.p2.id).count())
        vote.append(Comparison.objects.filter(game_instance=self).filter(selected=self.p3.id).count())
        return vote
    def choose(self,selected):
        if selected.id== self.different.id:
            return Result.win
        else:
            return Result.lose
    def choose2(self,selected):
        votes=self.get_votes()
        cath=self.get_different_according_to_cath()
        if not(cath == None):
            votes[self.index_of_protein(cath)]+=1
        votes[self.index_of_protein(self.different)]+=1
        max_number=max(votes)
        
        if(votes[self.index_of_protein(selected)] == max_number):
            if(votes.count(max_number) > 1):
                return Result.tie
            else:
                return Result.win
        else:
            
            return Result.lose
    def index_of_protein(self,protein):
        return self.proteins().index(protein)
class Comparison(models.Model):
  ts = models.DateTimeField(auto_now_add=True)
  user = models.ForeignKey(User)
  selected = models.ForeignKey(Protein, related_name="selected")
  game_instance = models.ForeignKey(GameInstance)
  order = models.CharField(max_length=100)
  user_level = models.IntegerField()
  accuracy = models.FloatField()
  game_type=models.CharField(max_length=20)
  def json(self):
      return '{"user": %d, "game_instance": %d}' % (self.user.id,self.game_instance.id)
class ComparisonProtein(models.Model):
  protein = models.ForeignKey(Protein)
  comparison = models.ForeignKey(Comparison)
class ComparisonPercentage(models.Model):
  ts = models.DateTimeField(auto_now_add=True)
  user = models.CharField(max_length=100)
  proteins = ManyToManyField(Protein, through="ComparisonPercentageProtein")
class ComparisonPercentageProtein(models.Model):
  protein = models.ForeignKey(Protein)
  comparison = models.ForeignKey(ComparisonPercentage)
  percentage = models.IntegerField()
class CathClassification(models.Model):
  protein = models.ForeignKey(Protein)
  code = models.CharField(max_length=200)
  level1 = models.CharField(max_length=200)
  level2 = models.CharField(max_length=200)
  level3 = models.CharField(max_length=200)
  level4 = models.CharField(max_length=200)
  def levels(self):
      return [self.level1,self.level2,self.level3,self.level4]
  def full_level(self):
      return  ".".join(self.levels())
  def json(self):
      levels=list_to_json(map(lambda x:'"'+x+'"',self.levels()))
      return '{"protein": %d, "levels": %s}' % (self.protein.id,levels)

class Classification(models.Model):
  protein = models.ForeignKey(Protein)
  #code = models.CharField(max_length=200)
  level1 = models.CharField(max_length=200)
  level2 = models.CharField(max_length=200)
  level3 = models.CharField(max_length=200)
  level4 = models.CharField(max_length=200)
  
  def levels(self):
      return [self.level1,self.level2,self.level3,self.level4]
  def full_level(self):
      return  self.level4
  def json(self):
      levels=list_to_json(map(lambda x:'"'+x+'"',[self.level1,self.level2,self.level3,self.level4]))
      return '{"protein": %d, "levels": %s}' % (self.protein.id,levels)



class Score(models.Model):
    user = models.ForeignKey(User,related_name="user")
    game_instances_played=models.IntegerField()
    game_instances_correct=models.IntegerField()
    game= models.IntegerField()
    level= models.IntegerField()
    user_level = models.IntegerField()
    @staticmethod
    def for_user(user, game, level):
        return Score(user=user,game_instances_played=0, game_instances_correct=0, game= game, level= level,user_level=user.get_profile().user_level)
    def chose(self, result):
     self.game_instances_played+=1     
     profile=self.user.get_profile() 
     if(result== Result.win):
        self.game_instances_correct+=1     
        profile.points+=1
        profile.save()      
     if(self.game_instances_played == settings.game_instances_per_level):
        profile.level+=1        
        if(profile.level== settings.levels_per_game):
            if(profile.points > profile.best_score_in_level):
                profile.best_score_in_level = profile.points
            if(profile.points >= settings.game_instances_correct_to_level_up):                
                profile.user_level+=1
                profile.best_score_in_level = 0
            profile.new_game()
        else:
            Score.for_user(self.user, profile.game, profile.level).save()            
        profile.save()

    def efficacy(self):
      return self.game_instances_correct*100/self.game_instances_played if not (self.game_instances_played==0) else 0
    def json(self):
        return '{"user": "%s", "game_instances_played": %d,"game_instances_correct": %d,"game": %d,"level": %d,"user_level": %d}' % (self.user.username,self.game_instances_played,self.game_instances_correct,self.game,self.level,self.user_level)
def list_to_json(l):
    return "["+(",".join(l))+"]"


class ClassificationComparator(object):
    (CathClassification, Classification)= ("CathClassification", "Classification")
    #(AllSimilar,AllDifferent)=("AllSimilar","AllDifferent")
    #possible methods are CathClassification, Classification
    def __init__(self, method):
        self.method= eval(method)

    def get_classification(self,p):
        return self.method.objects.get(protein=p)
#    def all_similar_or_different(self,proteins):
#        classifications= map(self.get_classification, proteins)
#        cs=itertools.combinations(classifications,2)
#        all_different= True
#        all_similar=True
#        for x in classifications:
#            print x.full_level()
#        for (c1,c2) in cs:
#            print  "c1: %s - c2:  %s" % (c1.full_level(),c2.full_level())
#            all_different= all_different and c1.level1!=c2.level1
#            all_similar= all_similar and c1.full_level()==c2.full_level
#        if(all_different):
#            return ClassificationComparator.AllDifferent
#        if(all_similar):
#            return ClassificationComparator.AllSimilar
#        return None
#    
    def get_distance_between_proteins(self,p1,p2):
        c1=self.get_classification(p1)
        c2=self.get_classification(p2)
        if(c1.level1 == c2.level1):
            if(c1.level2 == c2.level2):
                if(c1.level3 == c2.level3):
                    if(c1.level4 == c2.level4):
                        return 0
                    else:
                        return 1
                else:
                    return 2
            else:
                return 3
        else:
            return 4

    def get_different(self,p1,p2,p3):
        d1_2=self.get_distance_between_proteins(p1, p2)
        d2_3=self.get_distance_between_proteins(p2, p3)
        d1_3=self.get_distance_between_proteins(p1, p3)
        
        if(d1_2 < d2_3):
            return p3
        else:
            if(d1_3 < d2_3):
                return p2
            else:
                if(d1_3 > d2_3):
                    return p1
                else:
                    return None