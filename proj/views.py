#from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from django.template import loader
from .models import Skill, SkillTopic
from customers.models import Customer, SkillMatch
from .forms import ContactForm
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template import Context
from django.template.loader import get_template
from django.http import Http404
#import operator
import traceback
from django.db.models import F

class SkillCount(object):
	def __init__(self, skill_name, count):
        	self.skill_name = skill_name
		self.count = count

def index(request):
	try:
		skill_topic_list = SkillTopic.objects.extra(order_by = ('-classes_given', '-clicks'))
		skill_topics = []
		skill_list = []
		other_skill_list = []
		newArrivals = Skill.objects.extra(order_by = ('-created_date', '-clicks'))[:20]
		skill_topics.append("New Arrivals")
		skill_list.append(newArrivals)
		orderskills = Skill.objects.extra(order_by = ('-classes_given','-no_teachers','-clicks'))[:20]
		skill_topics.append("Trending")
		skill_list.append(orderskills)
		for skillTopic in skill_topic_list:
			skills = Skill.objects.filter(topic = skillTopic).extra(order_by = ('-classes_given','-no_teachers','-clicks'))
			if len(skills) > 5:
				skill_topics.append(skillTopic.topic_name)
				skill_list.append(skills)
			else:
				if len(skills) > 0:
					other_skill_list.extend(skills)
		if len(other_skill_list) > 0:
			skill_topics.append("Others")
			other_skill_list1 = sorted(other_skill_list, key = lambda x: (x.classes_given, x.no_teachers, x.clicks), reverse = True)
			skill_list.append(other_skill_list1)
		template = loader.get_template('proj/index.html')
		context = {
			'skill_list': skill_list,
			'skill_topic_list': skill_topics,
		}
		return HttpResponse(template.render(context, request))
	except Exception as e:
		print "exception caught"
		print '%s (%s)' % (e.message, type(e))
		traceback.print_exc(file=open("errlog.txt","a"))

def contact(request):
	try:
		form_class = ContactForm
	
		skillName = request.GET.get('skill', '')
		#print skillName
		skills = Skill.objects.filter(skill_name = skillName)
		if len(skills) > 0:
			skill = skills[0]
			Skill.objects.filter(skill_name = skillName).update(clicks=skill.clicks+1)
			SkillTopic.objects.filter(topic_name = skill.topic).update(clicks=F('clicks') + 1)
	

		# new logic!
		if request.method == 'POST':
	        	form = form_class(data=request.POST)

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
				preferred_communication_time = request.POST.get(
	                                'preferred_communication_time'
        	                , '')
        		form_content = request.POST.get('content', '')
	
        	    	template = get_template('proj/contact_template.txt')
            		context = Context({
				'skill_name': skillName,
	                	'contact_name': contact_name,
				'contact_phone': contact_phone,
	        	        'contact_email': contact_email,
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
			return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')

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
		customers = Customer.objects.filter(no_subjects__gt=0).extra(order_by = ('-no_subjects', '-classes_given'))
		customerSkillList = []
		for customer in customers:
			customerSkill = CustomerSkill(customer)
			customerSkillList.append(customerSkill)
		        skillMatchs = SkillMatch.objects.filter(customer=customer)
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
