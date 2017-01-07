from django.shortcuts import render

# Create your views here.

import traceback
from django.http import HttpResponse

from django.template import loader
from .models import Session, Call

def call_invoice(request, session_id):
        try:
		sessions = Session.objects.filter(id = session_id)
		if len(sessions) > 0:
			session = sessions[0]
			calls = Call.objects.filter(belong_session = session).order_by('start_time',)
			template = loader.get_template('session/invoice.html')
                	context = {
                        	'session': session,
				'calls': calls,
        	        }
                	return HttpResponse(template.render(context, request))
			#return HttpResponse(call)
		else:
			return HttpResponse("Wrong session id")
        except Exception as e:
                print "exception caught"
                print '%s (%s)' % (e.message, type(e))
                traceback.print_exc(file=open("errlog.txt","a"))                
