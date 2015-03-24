
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render_to_response('site/realIndex.html',context_instance=RequestContext(request))
def login(request):
    return render_to_response('site/index.html',context_instance=RequestContext(request))
@csrf_exempt
def redirect(request):
    """Unfuck Facebook's initial request."""
    return HttpResponseRedirect('/')
  