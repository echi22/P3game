import logging

from django.shortcuts import render_to_response
from django.template.context import RequestContext
logger = logging.getLogger(__name__)



def video(request):
        c={};
	return render_to_response('protein/video.html', c, context_instance=RequestContext(request))
