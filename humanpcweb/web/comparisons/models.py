from django.db.models.fields.related import ManyToManyField, OneToOneField
from django.db import models
from django.contrib.auth.models import User, UserManager

from django.core import serializers


# Create your models here.
class UserProfile(models.Model):
    user=models.OneToOneField(User)
    anonymous=models.BooleanField()
    points=models.IntegerField()
    attempts=models.IntegerField()
    score=models.IntegerField()
    def json( self ):
      anonymous='true' if self.anonymous else 'false'
      return '{"anonymous": "%s", "points": %d, "attempts": %d, "score":  %d, "proteins_compared": %d}'  % (anonymous,self.points, self.attempts, self.score, self.proteins_compared())
    def proteins_compared(self):
      return Comparison.objects.filter(user=self).count()
    
    
class Protein(models.Model):
    name=models.CharField(max_length=200)
    code=models.CharField(max_length=200)
    description=models.CharField(max_length=200)
    def scop_code(self):
      #detect astral codes
      if(len(self.code)==7):
        return self.code[2:6]
      return self.code
    def json( self ):

      return '{"id": "%s", "description": "%s", "name": "%s", "code": "%s"}'  % (self.id, self.description, self.name, self.code)

class Comparison(models.Model):
    ts=models.DateTimeField(auto_now_add=True)
    user_id=models.CharField(max_length=100)
    selected=models.ForeignKey(Protein, related_name="selected")
    proteins=ManyToManyField(Protein,through="ComparisonProtein")


class ComparisonProtein(models.Model):
    protein=models.ForeignKey(Protein)
    comparison=models.ForeignKey(Comparison)
class ComparisonPercentage(models.Model):
    ts=models.DateTimeField(auto_now_add=True)
    user=models.CharField(max_length=100)
    proteins=ManyToManyField(Protein,through="ComparisonPercentageProtein")
class ComparisonPercentageProtein(models.Model):
    protein=models.ForeignKey(Protein)
    comparison=models.ForeignKey(ComparisonPercentage)
    percentage=models.IntegerField()
class Classification(models.Model):
    protein=models.ForeignKey(Protein)
    level1=models.CharField(max_length=200)
    level2=models.CharField(max_length=200)
    level3=models.CharField(max_length=200)
    level4=models.CharField(max_length=200)
class GameInstance(models.Model):
    different=models.ForeignKey(Protein,related_name="different")
    p1=models.ForeignKey(Protein,related_name="p1")
    p2=models.ForeignKey(Protein,related_name="p2")
    p3=models.ForeignKey(Protein,related_name="p3")
    level=models.IntegerField()
    user=models.ForeignKey(User,null=True)
    ts=models.DateTimeField(auto_now_add=True)
    def json( self ):
      json_serializer = serializers.get_serializer("json")()
      json_serializer.serialize([self,self.p1,self.p2,self.p3,self.different], ensure_ascii=False)
      return json_serializer.getvalue()

class Highscore(models.Model):
    user=models.ForeignKey(User,related_name="user")
    points=models.IntegerField()