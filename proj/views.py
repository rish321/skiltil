#from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from django.template import loader
from .models import Skill, SkillTopic
from .forms import ContactForm
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template import Context
from django.template.loader import get_template

def index(request):
	skill_topic_list = SkillTopic.objects.all()
	skill_topics = []
	skill_list = []
	for skillTopic in skill_topic_list:
		skills = Skill.objects.filter(topic = skillTopic)
		print skills
		if len(skills) > 0:
			skill_topics.append(skillTopic)
			skill_list.append(skills)
	template = loader.get_template('proj/index.html')
	context = {
		'skill_list': skill_list,
		'skill_topic_list': skill_topics,
	}
	return HttpResponse(template.render(context, request))


def contact(request):
	form_class = ContactForm
	
	skillName = request.GET.get('skill', '')
	print skillName
	skills = Skill.objects.filter(skill_name = skillName)
	if len(skills) > 0:
		skill = skills[0]

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
                	['ris.90s@gmail.com'],
                	headers = {'Reply-To': contact_email }
            	)
            	email.send()
            	#return redirect('contact')
		return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')

	return render(request, 'proj/contact.html', {
		'form': form_class,
		'skill': skill,
	})

