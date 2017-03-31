import json

from allauth.socialaccount.models import SocialAccount
from django.shortcuts import render

# Create your views here.

import traceback
from django.http import HttpResponse, HttpResponseRedirect

from django.template import loader
from django.template.loader import render_to_string

from customers.models import Customer
from .models import Session, Call
from django.core.mail import EmailMultiAlternatives


def call_invoice(request, session_id):
    try:
        sessions = Session.objects.filter(id=session_id)
        if len(sessions) > 0:
            session = sessions[0]
            calls = Call.objects.filter(belong_session=session).order_by('start_time', )
            template = loader.get_template('session/invoice.html')
            context = {
                'session': session,
                'calls': calls,
            }
            return HttpResponse(template.render(context, request))
        # return HttpResponse(call)
        else:
            return HttpResponse("Wrong session id")
    except Exception as e:
        print "exception caught"
        print '%s (%s)' % (e.message, type(e))
        traceback.print_exc(file=open("errlog.txt", "a"))


def call_invoice_student(request, session_id):
    try:
        sessions = Session.objects.filter(id=session_id)
        if len(sessions) > 0:
            session = sessions[0]
            calls = Call.objects.filter(belong_session=session).order_by('start_time', )
            # template = loader.get_template('session/invoice.html')
            '''context = {
                'session': session,
                'calls': calls,
            }'''
            # render = template.render(context, request)
            html = render_to_string('session/student_invoice.html', {'session': session, 'calls': calls, })
            email = EmailMultiAlternatives(
                'Invoice for your recent ' + session.skill_match.skill.skill_name + ' session with Skiltil',
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
            # template = loader.get_template('session/invoice.html')
            '''context = {
                'session': session,
                'calls': calls,
            }'''
            # render = template.render(context, request)
            html = render_to_string('session/teacher_invoice.html', {'session': session, 'calls': calls, })
            email = EmailMultiAlternatives(
                'Invoice for your recent ' + session.skill_match.skill.skill_name + ' session with Skiltil',
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
                                           'Hope you have a great teaching experience',
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


def send_feedback_student(request, session_id):
    try:
        sessions = Session.objects.filter(id=session_id)
        if len(sessions) > 0:
            session = sessions[0]
            html = render_to_string('session/student_feedback.html', {'session': session})
            subject = 'Thanks for your ' + session.skill_match.skill.skill_name + ' session with Skiltil'
            email = EmailMultiAlternatives(subject,
                                           'Hope you had a great learning experience',
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


def send_feedback_teacher(request, session_id):
    try:
        sessions = Session.objects.filter(id=session_id)
        if len(sessions) > 0:
            session = sessions[0]
            html = render_to_string('session/teacher_feedback.html', {'session': session})
            subject = 'Thanks for your ' + session.skill_match.skill.skill_name + ' session with Skiltil'
            email = EmailMultiAlternatives(subject,
                                           'Hope you had a great teaching experience',
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


def feedback(request, session_id):
    try:
        if request.user.is_authenticated():
            user = request.user
            socialAccount = SocialAccount.objects.filter(user_id=user.id)[0]
            customer = Customer.objects.filter(social=socialAccount)[0]

            sessions = Session.objects.filter(order_id=session_id)
            if len(sessions) > 0:
                session = sessions[0]
                # print session


                rating = 0
                comments = ""
                if request.method == 'GET':
                    rating = int(request.GET.get('rating', 0))
                    comments = ""

                elif request.method == 'POST':
                    json1 = json.loads(request.POST.get('msg'))
                    rating = int(json1.get('rating'))
                    comments = str(json1.get('comments'))

                if customer == session.student:

                    template = loader.get_template('session/feedback.html')

                    if session.teacher_rating > 0:
                        if not session.teacher_comments:
                            session.teacher_comments = comments
                        context = {
                            'already_rated': True,
                        }
                    else:
                        session.teacher_rating = rating
                        session.teacher_comments = comments
                        context = {
                            'customer': customer,
                            'session': session,
                            'rating': rating,
                            'student': True,
                            'already_rated': False,
                        }
                    session.save()
                    return HttpResponse(template.render(context, request))

                elif customer == session.skill_match.customer:
                    template = loader.get_template('session/feedback.html')
                    if session.student_rating > 0:
                        if not session.student_comments:
                            session.student_comments = comments
                        context = {
                            'already_rated': True,
                        }
                    else:
                        session.student_rating = rating
                        session.student_comments = comments
                        context = {
                            'customer': customer,
                            'session': session,
                            'rating': rating,
                            'student': False,
                            'already_rated': False,
                        }
                    session.save()
                    return HttpResponse(template.render(context, request))

                else:
                    return HttpResponseRedirect('/')

            else:
                return HttpResponse("Wrong session id")
        else:
            return HttpResponseRedirect('/accounts/login')
    except Exception as e:
        print "exception caught"
        print '%s (%s)' % (e.message, type(e))
        traceback.print_exc(file=open("errlog.txt", "a"))
