from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from web.proteins.models import  Protein
import logging
import random

logger = logging.getLogger(__name__)


#prototype for classifying proteins in groups

def play(request):
  c={}
  return render_to_response('classification_game/play.html', c, context_instance=RequestContext(request))

def get_random_item(q):
  count=q.count()
  i=random.randint(0,count-1)
  return (q[i], i, count)

def get_game_instance(request):
  amount= int (request.GET[ "amount"])
  q=Protein.objects.all()
  result=[]
  for _ in range(0, amount ):
    result.append(get_random_item(q))
  proteins=",".join(map(lambda (p,a,b):p.json(), result))
  return  HttpResponse("[ "+ proteins+"]")