from django.shortcuts import render

# Create your views here.

import traceback
from django.http import HttpResponse

from django.template import loader
from django.template.loader import render_to_string
from .models import Session, Call
from django.core.mail import EmailMultiAlternatives

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


def call_invoice_student(request, session_id):
	try:
		sessions = Session.objects.filter(id=session_id)
		if len(sessions) > 0:
			session = sessions[0]
			calls = Call.objects.filter(belong_session=session).order_by('start_time', )
			#template = loader.get_template('session/invoice.html')
			'''context = {
				'session': session,
				'calls': calls,
			}'''
			#render = template.render(context, request)
			html = render_to_string('session/student_invoice.html', {'session': session, 'calls': calls, })
			email = EmailMultiAlternatives('Invoice for your recent ' + session.skill_match.skill.skill_name +  ' session with Skiltil',
										   'Thanks for taking a session with us',
										   'support@skiltil.com', [session.student.email],
										   headers={'IsTransactional': "True"}, )
			email.attach_alternative(html, "text/html")
			email.send()
			print html
			return HttpResponse(html)
		# return HttpResponse(call)
		else:
			return HttpResponse("Wrong session id")
	except Exception as e:
		print "exception caught"
		print '%s (%s)' % (e.message, type(e))
		traceback.print_exc(file=open("errlog.txt", "a"))


def call_invoice_teacher(request, session_id):
	try:
		sessions = Session.objects.filter(id=session_id)
		if len(sessions) > 0:
			session = sessions[0]
			calls = Call.objects.filter(belong_session=session).order_by('start_time', )
			#template = loader.get_template('session/invoice.html')
			'''context = {
				'session': session,
				'calls': calls,
			}'''
			#render = template.render(context, request)
			html = render_to_string('session/teacher_invoice.html', {'session': session, 'calls': calls, })
			email = EmailMultiAlternatives('Invoice for your recent ' + session.skill_match.skill.skill_name +  ' session with Skiltil',
										   'Thanks for taking a class with us',
										   'support@skiltil.com', [session.skill_match.customer.email],
										   headers={'IsTransactional': "True"}, )
			email.attach_alternative(html, "text/html")
			email.send()
			print html
			return HttpResponse(html)
		# return HttpResponse(call)
		else:
			return HttpResponse("Wrong session id")
	except Exception as e:
		print "exception caught"
		print '%s (%s)' % (e.message, type(e))
		traceback.print_exc(file=open("errlog.txt", "a"))

def call_schedule_student(request, session_id):
	try:
		sessions = Session.objects.filter(id=session_id)
		if len(sessions) > 0:
			session = sessions[0]
			html = render_to_string('session/student_schedule.html', {'session': session})
			subject = 'Schedule for your ' + session.skill_match.skill.skill_name + ' session with Skiltil'
			if session.rescheduled_time != session.scheduled_time:
				subject = "Updated Time " + '{:%I:%M %p, (%d-%m-%Y)}'.format(session.rescheduled_time) + " - " + subject
			email = EmailMultiAlternatives(subject,
										   'Hope you have a great learning experience',
										   'support@skiltil.com', [session.student.email],
										   headers={'IsTransactional': "True"}, )
			email.attach_alternative(html, "text/html")
			email.send()
			print html
			return HttpResponse(html)
		# return HttpResponse(call)
		else:
			return HttpResponse("Wrong session id")
	except Exception as e:
		print "exception caught"
		print '%s (%s)' % (e.message, type(e))
		traceback.print_exc(file=open("errlog.txt", "a"))

def call_schedule_teacher(request, session_id):
	try:
		sessions = Session.objects.filter(id=session_id)
		if len(sessions) > 0:
			session = sessions[0]
			html = render_to_string('session/teacher_schedule.html', {'session': session})
			subject = 'Schedule for your ' + session.skill_match.skill.skill_name + ' session with Skiltil'
			if session.rescheduled_time != session.scheduled_time:
				subject = "Updated Time " + '{:%I:%M %p, (%d-%m-%Y)}'.format(session.rescheduled_time) + " - " + subject
			email = EmailMultiAlternatives(subject,
										   'Hope you have a great learning experience',
										   'support@skiltil.com', [session.skill_match.customer.email],
										   headers={'IsTransactional': "True"}, )
			email.attach_alternative(html, "text/html")
			email.send()
			print html
			return HttpResponse(html)
		# return HttpResponse(call)
		else:
			return HttpResponse("Wrong session id")
	except Exception as e:
		print "exception caught"
		print '%s (%s)' % (e.message, type(e))
		traceback.print_exc(file=open("errlog.txt", "a"))