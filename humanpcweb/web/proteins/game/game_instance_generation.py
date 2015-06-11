from django.db.models.aggregates import Count
from web.proteins.models import GameInstance
from web import settings
from django.db.models import Avg, Max, Min
from web.proteins.models import Classification
from web.proteins.models import Comparison
import random
import logging
from web.utility import ClassLoader
logger = logging.getLogger(__name__)



class InvalidClassification(Exception): 
  pass
class Level():
  '''
  represents level with with 2 values (level, sublevel):
    level: represents how similar are the 2 similar proteins (how many levels they share )
      level 1 means they share class but maybe not fold, super family, or family (w - - -)
      level 2 means they share class and fold but maybe not super family, or family (w x - -)
    sublevel: represents how similar the 2 proteins with respect to the different one (how many parents they share until they differ)
      sublevel 1 means they have a different class (w' - - -)
      sublevel 2 means they have the same class, but come from a different fold (w x' - -)
  '''
  def __init__(self,level, sublevel):
    if sublevel> level:
      raise Exception(" cannot generate a Level with a greater sub level value than the level value")
    self.level=level
    self.sublevel= sublevel
  def __str__(self):
      return  "(%d,%d)" % ( self.level, self.sublevel)
class InvalidGameInstance(Exception):
    pass
class GameInstanceGenerator():
    @staticmethod
    def get_default_generator():
        return ClassLoader().load(settings.game_instances_generator_module, settings.game_instances_generator_klass)()
    def max_level(self):
        return 10
    def generate_game_instance(self, level, level_attempt):
      q1, q2, q3, c1,c1_index= self.generate_queries(level)
      list,different=self.generate_classifications_from_queries(q1, q2, q3, c1,c1_index)      
      gi=GameInstance(p1=list[0].protein,p2=list[1].protein,p3=list[2].protein,different=different.protein,different_movies=different.protein,different_static=different.protein,level=level,level_attempt=level_attempt,times_played=0)
      return gi
    def is_repeated( self,game_instance):
      return GameInstance.objects.filter(p1= game_instance.p1).filter(p2= game_instance.p2).filter(p3= game_instance.p3).count()>0


    def generate_game_instances(self,level_attempt,level,n):
      result=[]
      attempts=0
      print  " Generating  game instances for game %d, mission  %d..." % (level_attempt, level)
      for i in range(0, n):
            finished=False
            while not finished:
              try:
                  attempts+=1
                  game_instance= self.generate_game_instance(level, level_attempt)
                  if self.is_repeated(game_instance):
                      raise InvalidGameInstance('game instance repeated: proteins ( %s) ' % ( game_instance))
                  else:
                      #print "protein created"
                      finished=True
              except InvalidGameInstance, e:
                  #print str(e)
                  a=0
            result.append(game_instance)
      print  " generation complete,  %d instances generated,  %d attempts made " % (n, attempts)
      return result

    def generate_and_save_game_instances( self,level_attempt,level,n):
      game_instances=self.generate_game_instances(level_attempt,level,n)
      for game_instance in game_instances:
        game_instance.save()

    def get_all_game_instances(self, level,level_attempt):
      q=GameInstance.objects.filter(level_attempt= level_attempt, level = level)
      #q=q.annotate(comparisons=Count('comparison'))
      #q=q.filter(comparisons__lte=maximum_comparisons)
      return q

    def get_game_instances_not_played( self,level_attempt,level, user):
      
        max = Comparison.objects.filter(user=user,game_instance__level_attempt=level_attempt,game_instance__level=level).annotate(number_of_entries=Count("game_instance__id",  distinct=True)).order_by('number_of_entries')
        if(not max or max.count()== settings.levels_per_game):
          user_comparisons = []          
        else:
          max = max[0].number_of_entries
          user_comparisons =Comparison.objects.filter(user=user).annotate(number_of_entries=Count("game_instance__id",  distinct=True)).filter(number_of_entries=max)
        #user_comparisons = Comparison.objects.filter(user=user).values( "game_instance_id")
        game_instances=self.get_game_instances(level_attempt, level)
        
        q=game_instances.exclude(id__in = user_comparisons)
        return  q
        
    def get_game_instances( self,level_attempt,level):
      game_instances=self.get_all_game_instances(level,level_attempt).count()
      if(game_instances == 0):
        random.seed(level_attempt+ level)
        game_instances_to_generate=settings.levels_per_game
        self.generate_and_save_game_instances(level_attempt,level, game_instances_to_generate)
      return self.get_all_game_instances(level,level_attempt)
      
    def get_random_item(self,q):
      count=q.count()
      i=random.randint(0,count-1)
      return (q[i], i, count)

    def get_random_item_except(self,q,j):
      count=q.count()
      offset=random.randint(1,count-1)
      i=(j+ offset)% count
      return (q[i], i, count)

    def generate_classifications_from_queries(self,q1,q2,q3, c1,c1_index):
      c2=self.get_random_item(q2)[0]
      c3=q3[random.randint(0,q3.count()-1)]
      l=[c1,c2]
      #put the proteins in lexicographical order according to their name so that
      # the check for repeated instances is simpler (does not need to check for permutations of p1,p2,p3)
      l.sort(key=lambda c: c.protein.name)
      l.append(c3)
      return l,c3
    def generate_queries(self):
       pass
    def generate_same_protein_query(self):
       pass
class ScopGameInstanceGenerator(GameInstanceGenerator):
    def mapping(self):
      '''
      maps user levels to levels.the current mapping follows the total ordering  defined by:
      (a,b)<(c,d) iff a-b < c-d and a<c
      '''
      return   [
      
      Level(2, 2),
      Level(2, 2),
      Level(4, 3),
      Level(4, 3),
      Level(3, 3),
      Level(3, 3),
      Level(4, 4),
      Level(4, 4),
      ]
    def user_level_to_level(self,level):
      return self.mapping()[level]
    def level_to_user_level(self,level):
      user_level=filter(lambda l: l.level == level.level and l.sublevel== level.sublevel)
      return (user_level[0] if len(user_level)>0 else -1)
  
    

    def generate_queries(self,level):

      level= self.user_level_to_level(level)
      level_to_guarantee= "level%d" % ( level.level )
      q=Classification.objects.values( level_to_guarantee).annotate(count=Count(level_to_guarantee)).order_by( level_to_guarantee).filter(count__gt=1).values(level_to_guarantee)
    
      
      filter={level_to_guarantee+"__in":q}
      q1=Classification.objects.filter(**filter)
  
      if(q1.count()<2):
        raise InvalidClassification()
        
      c1, c1_index,n=self.get_random_item(q1)
      q2=self.generate_same_protein_query( level,c1 )
      q3=self.generate_different_protein_query(level, c1)
      if(q3.count() == 0):
          raise InvalidGameInstance('Could not find different protein for %s (level: %s)' %(c1,level))
  
      return (q1, q2, q3, c1, c1_index)



    def generate_same_protein_query(self,level,c1):
      filter2={}
      for i in range(1,level.level+1):
        current_level="level"+str(i)
        filter2[current_level]=vars(c1)[current_level]
      current_level="level"+str(level.level)
      q2=Classification.objects.filter(**filter2).exclude(id=c1.id)
      if(level.level<4):
        current_level="level"+str(level.level+1)
        exclude={current_level:vars(c1)[current_level]}
        q2=q2.exclude(**exclude)
      if(q2.count() == 0):
          raise InvalidGameInstance('Could not find similar protein for %s (level: %s)' %(c1,level))
      return q2

    def generate_different_protein_query(self,level,c1):
      filter3={}
      for i in range(1,level.sublevel):
        current_level="level"+str(i)
        filter3[current_level]=vars(c1)[current_level]
      current_level="level"+str(level.sublevel)
      exclude3={current_level:vars(c1)[current_level]}
      q3=Classification.objects.filter(** filter3).exclude(**exclude3)
      return q3

