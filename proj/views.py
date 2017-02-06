#from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.template import loader
from .models import Skill, SkillTopic, CustomerRequest
from customers.models import Customer, SkillMatch
from .forms import ContactForm
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.http import Http404
from django.db.models import Q
#import operator
import traceback
from django.db.models import F
import re
from django.contrib.auth import logout as auth_logout

from django.contrib.auth import authenticate

class SkillCount(object):
	def __init__(self, skill_name, count):
		self.skill_name = skill_name
		self.count = count

class PreDefStrings(object):
	def __init__(self, string, code):
		self.string = string
		self.code = code
	def __str__(self):
		return self.string

PreDefTrending = PreDefStrings("Trending", "trending")
PreDefNewArrival = PreDefStrings("New Arrivals", "new_arrivals")

TRENDING = "Trending"
NEW_ARRIVALS = "New Arrivals"

def index(request):
	try:
		template = loader.get_template('proj/index.html')
		context = {
			#'skill_list': skill_list,
			#'skill_topic_list': skill_topics,
		}
		return HttpResponse(template.render(context, request))
	except Exception as e:
		print "exception caught"
		print '%s (%s)' % (e.message, type(e))
		traceback.print_exc(file=open("errlog.txt","a"))


def contact(request, skill_code):
	try:
		data = {'skill': ""}
		form_class = ContactForm(initial=data)


		#print skillName
		skills = Skill.objects.filter(skill_code = skill_code)
		if len(skills) > 0:
			skill = skills[0]
			data = {'skill': skill.skill_name}
			form_class = ContactForm(initial=data)
			Skill.objects.filter(skill_name = skill.skill_name).update(clicks=skill.clicks+1)
			SkillTopic.objects.filter(topic_name = skill.topic).update(clicks=F('clicks') + 1)


		# new logic!
		if request.method == 'POST':
	        	form = ContactForm(data=request.POST)



	        	if form.is_valid():
        	    		contact_name = request.POST.get(
               				'contact_name'
		        	, '')
				contact_phone = request.POST.get(
                	                'contact_phone'
                        	, '')
	            		contact_email = request.POST.get(
        	        		'contact_email'
	        	    	, '')
	            		skill_entered = request.POST.get(
        	        		'skill'
				, '')
				preferred_communication_time = request.POST.get(
	                                'preferred_communication_time'
        	                , '')

        		form_content = request.POST.get('content', '')
			customerRequest = CustomerRequest(contact_name=contact_name, contact_phone=contact_phone, contact_email=contact_email, skill=skill_entered, preferred_communication_time=preferred_communication_time, content=form_content, default_skill=skill.skill_name)
			customerRequest.save()

        	    	template = get_template('proj/contact_template.txt')
            		context = Context({
				'skill_name': skill.skill_name,
	                	'contact_name': contact_name,
				'contact_phone': contact_phone,
	        	        'contact_email': contact_email,
				'skill': skill,
				'preferred_communication_time': preferred_communication_time,
	        	        'form_content': form_content,
        	    	})
	        	content = template.render(context)

			# Email the profile with the
        	    	# contact information


            		email = EmailMessage(
                		"New contact form submission",
	                	content,
        	        	"Your website" +'',
                		['help.skiltil@gmail.com'],
                		headers = {'Reply-To': contact_email }
	            	)
        	    	email.send()
            		#return redirect('contact')
			#return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')
			#return HttpResponse('<script>'
			#					'$("#alert-success").show();'
			#					'alert("Success! Thanks for your interest. We\'ll get back to you.");'
			#					'window.close(); window.parent.location.href = "/";'
			#					'</script>')
			return HttpResponseRedirect('/thanks/')
		return render(request, 'proj/contact.html', {


			'form': form_class,
			'skill': skill,
		})
	except Exception as e:
		print "exception caught"
		print '%s (%s)' % (e.message, type(e))
		traceback.print_exc(file=open("errlog.txt","a"))

class CustomerSkill(object):
        def __init__(self, customer):
                self.customer = customer
		self.skillMatchs = []


def teachers(request):
        try:
		customers = Customer.objects.filter(no_subjects__gt=0).filter(classes_given__gt=0).extra(order_by = ('-no_subjects', '-classes_given'))
		customerSkillList = []
		for customer1 in customers:
			customerSkill = CustomerSkill(customer1)
			customerSkillList.append(customerSkill)
		        skillMatchs = SkillMatch.objects.filter(customer=customer1).order_by('-classes_given')
			customerSkill.skillMatchs.extend(skillMatchs)
		template = loader.get_template('proj/teachers.html')
                context = {
                        'teachers': customerSkillList,
                }
                return HttpResponse(template.render(context, request))
	except Exception as e:
                print "exception caught"
                print '%s (%s)' % (e.message, type(e))
                traceback.print_exc(file=open("errlog.txt","a"))

def thanks(request):
	return render_to_response( 'proj/thanks.html')

def ajax_skill_search( request ):
	results = []
        q = request.GET.get( 'q' )
	print q
        if q is not None:
	        results = Skill.objects.filter(
	               	Q( skill_name__icontains = q ) | Q( topic__topic_name__icontains = q )
		).order_by('-classes_given','-no_teachers','-clicks')
		print results
	        return render_to_response( 'proj/results_new.html', { 'results': results, } )
	return HttpResponse("Some error occurred")

def ajax_skill_topics(request):
	try:
		q = request.GET.get('q')
		# q = "f"
		if q is None:
			q = ""
		skill_topic_list = SkillTopic.objects.extra(order_by=('-classes_given', '-clicks'))
		skill_topics = []
		# skill_list = []
		other_skill_list = []
		# orderskills = Skill.objects.extra(order_by = ('-classes_given','-no_teachers','-clicks'))[:20]
		if len(q) <= 0:
			skill_topics.append(PreDefTrending)
		# skill_list.append(orderskills)
		# newArrivals = Skill.objects.extra(order_by = ('-created_date', 'clicks'))[:20]
		if len(q) <= 0:
			skill_topics.append(PreDefNewArrival)
		# skill_list.append(newArrivals)
		for skillTopic in skill_topic_list:
			skills = Skill.objects.filter(topic=skillTopic)
			if re.search(q, skillTopic.topic_name, re.IGNORECASE) and len(skills) > 0:
				skill_topics.append(skillTopic)
			else:
				skills = skills.filter(Q(skill_name__icontains=q))
				if len(skills) > 0:
					skill_topics.append(skillTopic)

			# skill_list.append(skills)
			# else:
			#	if len(skills) > 0:
			#		other_skill_list.extend(skills)
			# if len(other_skill_list) > 0:
			#	skill_topics.append("Others")
			#	other_skill_list1 = sorted(other_skill_list, key = lambda x: (x.classes_given, x.no_teachers, x.clicks), reverse = True)
			# skill_list.append(other_skill_list1)
		template = loader.get_template('proj/results_main_list.html')
		context = {
			'skill_topic_list': skill_topics,
		}
		return HttpResponse(template.render(context, request))
	except Exception as e:
		print "exception caught"
		print '%s (%s)' % (e.message, type(e))
		traceback.print_exc(file=open("errlog.txt", "a"))

def ajax_skills(request, skill_topic_code):
	try:
		q = request.GET.get('q')
		if q is None:
			q = ""
		skillTopics = SkillTopic.objects.filter(topic_code=skill_topic_code)
		skillTopic = skillTopics[0]
		if re.search(q, skillTopic.topic_name, re.IGNORECASE):
			skills = Skill.objects.filter(topic__topic_code=skill_topic_code).extra(
				order_by=('-classes_given', '-no_teachers', '-clicks'))
		else :
			skills = Skill.objects.filter(topic__topic_code=skill_topic_code).filter(Q(skill_name__icontains=q)).extra(
				order_by=('-classes_given', '-no_teachers', '-clicks'))
		if len(skills) > 0:
			context, template = process_skill_list(skills)
			return HttpResponse(template.render(context, request))
		# return HttpResponse(call)
		else:
			return HttpResponse("Wrong skill topic")
	except Exception as e:
		print "exception caught"
		print '%s (%s)' % (e.message, type(e))
		traceback.print_exc(file=open("errlog.txt", "a"))


def process_skill_list(skills):
	skill_match_list = get_skill_match_list(skills)
	template = loader.get_template('proj/results_skill_topic.html')
	context = {
		'skill_list': skills,
		'skill_match_list': skill_match_list,
	}
	return context, template


def get_skill_match_list(skills):
	skill_match_list = []
	for skil in skills:
		skill_matches = SkillMatch.objects.filter(skill=skil)
		skill_match_list.extend(skill_matches)
	return skill_match_list


def ajax_skills_predef(request, predef_name):
	try:
		#print predef_name
		if predef_name.lower() == PreDefTrending.code.lower() :
			orderskills = Skill.objects.extra(order_by=('-classes_given', '-no_teachers', '-clicks'))[:20]
			if len(orderskills) > 0:
				context, template = process_skill_list(orderskills)
				return HttpResponse(template.render(context, request))
			else:
				return HttpResponse("Wrong topic")
		elif predef_name.lower() == PreDefNewArrival.code.lower() :
			newArrivals = Skill.objects.extra(order_by=('-created_date', 'clicks'))[:20]
			if len(newArrivals) > 0:
				context, template = process_skill_list(newArrivals)
				return HttpResponse(template.render(context, request))
			else:
				return HttpResponse("Wrong topic")
		# return HttpResponse(call)
		else:
			return HttpResponse("Wrong skill topic")
	except Exception as e:
		print "exception caught"
		print '%s (%s)' % (e.message, type(e))
		traceback.print_exc(file=open("errlog.txt", "a"))

#def login(request):


#def logout(request):
#    auth_logout(request)
#    return redirect('/')
