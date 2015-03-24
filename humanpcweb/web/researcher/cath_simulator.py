
import random
from web.proteins.models import ClassificationComparator
from web import settings
import itertools
import os


class SimulationStatistics(object):
    def __init__(self, agreement=0, invalid=0, count=0):
        self.agreement=agreement
        self.invalid= invalid
        self.count= count
    def add_all(self, simulation_statistics):
        self.agreement+= simulation_statistics.agreement
        self.invalid+=simulation_statistics.invalid 
        self.count+= simulation_statistics.count
    def wrong(self):
        return (self.count- self.invalid)- self.agreement
    def reset(self):
        self.agreement=0
        self.invalid=0
        self.count=0
    def update(self, different, game_instance):
       if different!= None:
           if different.code== game_instance.different.code:
               self.count_agreement()
           else:
               self.count_wrong()
       else:
            self.count_invalid()
    def __str__(self):
        return "Agreement: %d, invalid: %d, wrong: %d, total: %d \n"  % (self.agreement, self.invalid, self.wrong(),self.count)     
    def count_agreement(self):
        self.agreement+=1
        self.count+=1
    def count_invalid(self):
        self.count+=1
        self.invalid+=1
    def count_wrong(self):
        self.count+=1
            
class SimulationStatisticsByGameAndMission(object):
    def __init__(self, statistics, game, mission):
        self.statistics= statistics
        self.game= game
        self.mission =mission


        
class  CathSimulator(object):
    def __init__(self, games):
        self.games= games
    
    @staticmethod
    def get_classification(game_instance, selector):
        result= map(lambda p: ",".join(selector(p).level4.split( ".")),game_instance.proteins())
        return result
        #return  list (itertools.chain.from_iterable(result))
    @staticmethod
    def get_classifications(game_instance):
        cath= CathSimulator.get_classification(game_instance, lambda p:p.cath())
        scop= CathSimulator.get_classification(game_instance, lambda p:p.scop())
        return scop+ cath
    @staticmethod
    def result_header():
         result="trio_id, game, level,shared, not_shared"
         result+= ",p0,p1,p2,scop, cath,cluster,"
         result+= ",".join( [ "scop-p%d-l%d" % (i,j+1) for i in range(3) for j in range(4)])
         result+= ","+ ( ",".join( [ "cath-p%d-l%d" % (i,j+1) for i in range(3) for j in range(4)]))
         return result
    @staticmethod
    def get_different_cluster(game_instance,cluster):
        for p in game_instance.proteins():
            if (not p.code[1:] in cluster.from_scop):
                return None
        a,b,c= map(lambda p: cluster.from_scop[p.code[1:]],game_instance.proteins())
        if(a==b and b!=c):
            return game_instance.proteins()[2]
        if(a==c and b!=c):
            return game_instance.proteins()[1]
        if(c==b and b!=c):
            return game_instance.proteins()[0]
        return None
    @staticmethod
    def game_instance_to_row(game_instance, generator,cluster):
        classifications=CathSimulator.get_classifications(game_instance)
        comparator= ClassificationComparator(ClassificationComparator.CathClassification)
        different_cath=game_instance.get_different_according_to_cath()
        level=generator.user_level_to_level( game_instance.level)
        different_clusters=CathSimulator.get_different_cluster(game_instance, cluster)
        cluster_choice= str(different_clusters.code) if (different_clusters != None) else  "invalid"
        if different_cath!= None:
           #cath=" %s(%d)"  % (different_cath.code, game_instance.index_of_protein(different_cath))
           cath= str(different_cath.code)
        else:
           cath= ""+str(4-comparator.get_distance_between_proteins(game_instance.p1,game_instance.p2))
        #scop= "%s(%d)"  % (game_instance.different.code, game_instance.index_of_protein(game_instance.different))
        scop= str(game_instance.different.code)
        result =[game_instance.id, game_instance.game, game_instance.level,str(level.level),str(level.sublevel)] 
        result+=map(lambda p:p.code,game_instance.proteins()) +[ scop, cath, cluster_choice]+ classifications 
        return result,different_cath, different_clusters
    
    def simulate(self, generator):
        
        result=[]
        statistics_by_game_and_mission=[]
        statistics_by_mission_cath=[SimulationStatistics(0,0,0) for _ in range(settings.levels_per_game)]
        statistics_by_mission_clusters=[SimulationStatistics(0,0,0) for _ in range(settings.levels_per_game)]
        cluster= Cluster(Cluster.default_path())
        total_cath= SimulationStatistics()
        total_clusters= SimulationStatistics()
        for game in range(self.games):
           for mission in range(settings.levels_per_game):
               cath= SimulationStatistics(0,0,0)
               clusters= SimulationStatistics(0,0,0)
               game_instances =generator.get_game_instances(game, mission)
               for game_instance in game_instances:
                   row, different_cath, different_cluster=CathSimulator.game_instance_to_row(game_instance, generator, cluster)
                   cath.update(different_cath, game_instance)
                   clusters.update(different_cluster, game_instance)
                   result.append(row)
               s = SimulationStatisticsByGameAndMission(cath, game, mission)
               total_cath.add_all(cath)
               total_clusters.add_all(clusters)
               statistics_by_mission_cath[mission].add_all(cath)
               statistics_by_mission_clusters[mission].add_all(clusters)
               statistics_by_game_and_mission.append(s)
           print  " simulation of game %d finished"  % ( game)   
        return result,total_cath, total_clusters, statistics_by_game_and_mission, statistics_by_mission_cath,  statistics_by_mission_clusters


class Cluster(object):
    @staticmethod
    def default_path():
        return os.path.join(settings.BASE_PATH, "..", "samples", "datasets", "scop-cath",  "clusters.csv")
     
    def __init__(self,path): 
        self.from_scop={}
        for line in file(path):
            if(not line.startswith( "#")):
                s= line.split(" ")
                self.from_scop[s[1]]=s[0]
        print self.from_scop
    