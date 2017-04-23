# from django.shortcuts import render

# Create your views here.
from allauth.socialaccount.models import SocialAccount
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect

from django.template import loader
from django.template.defaulttags import register

from .models import Skill, SkillTopic, CustomerRequest, Event
from customers.models import Customer, SkillMatch
from .forms import ContactForm
from django.shortcuts import render
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.shortcuts import redirect
from django.template import Context
from django.template.loader import get_template, render_to_string
from django.shortcuts import render_to_response
from django.http import Http404
from django.db.models import Q
# import operator
import traceback
from django.db.models import F
import re
import operator
import json


class PreDefStrings(object):
    def __init__(self, string, code, image_url):
        self.string = string
        self.code = code
        self.image_url = image_url

    def __str__(self):
        return self.string


PreDefTrending = PreDefStrings("Trending", "trending", "static/images/topic/trending.png")
PreDefNewArrival = PreDefStrings("New Arrivals", "new_arrivals", "static/images/topic/new_arrival.png")
PreDefExclusive = PreDefStrings("Skiltil Exclusive", "exclusive", "static/images/topic/exclusive.png")


def index(request):
    try:
        template = loader.get_template('proj/index.html')
        context = {
            # 'skill_list': skill_list,
            # 'skill_topic_list': skill_topics,
        }
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print "exception caught"
        print '%s (%s)' % (e.message, type(e))
        traceback.print_exc(file=open("errlog.txt", "a"))


def sendConfirmationMail(customerRequest):
    if customerRequest.contact_email is None:
        return
    html = render_to_string('customers/new_customer_request.html', {'customer_request': customerRequest})
    email = EmailMultiAlternatives(
        'Your request for ' + customerRequest.skill + " has been received",
        'Hi ' + customerRequest.contact_name + ",\n We have received your request. We\'ll contact you on " + customerRequest.contact_phone + " at your preferred time. Now explore the endless learning experience only at Skiltil.",
        'support@skiltil.com', [customerRequest.contact_email],
        headers={'IsTransactional': "True"}, )
    email.attach_alternative(html, "text/html")
    email.send()
    pass


def details(request, skill_code):
    try:
        data = {'skill': ""}
        form_class = ContactForm(initial=data)

        # print skillName
        skills = Skill.objects.filter(skill_code=skill_code)

        if request.user.is_authenticated():
            user = request.user
            socialAccounts = SocialAccount.objects.filter(user_id=user.id)
            if len(socialAccounts) > 0:
                socialAccount = socialAccounts[0]
                customer = Customer.objects.filter(social=socialAccount)[0]

                data['contact_name'] = customer.customer_name
                data['contact_email'] = customer.email
                data['contact_phone'] = customer.phone_number
                form_class = ContactForm(initial=data)

        if len(skills) > 0:
            skill = skills[0]
            # data = {'skill': skill.skill_name}
            data['skill'] = skill.skill_name
            form_class = ContactForm(initial=data)
            Skill.objects.filter(skill_name=skill.skill_name).update(clicks=skill.clicks + 1)
            SkillTopic.objects.filter(topic_name=skill.topic).update(clicks=F('clicks') + 1)

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
            customerRequest = CustomerRequest(contact_name=contact_name, contact_phone=contact_phone,
                                              contact_email=contact_email, skill=skill_entered,
                                              preferred_communication_time=preferred_communication_time,
                                              content=form_content, default_skill=skill.skill_name)
            customerRequest.save()
            sendConfirmationMail(customerRequest)

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
                "Your website" + '',
                ['help.skiltil@gmail.com'],
                headers={'Reply-To': contact_email}
            )
            # email.send()
            # return redirect('contact')
            # return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')
            # return HttpResponse('<script>'
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
        traceback.print_exc(file=open("errlog.txt", "a"))

def request(request):
    try:
        data = {'skill': ""}
        form_class = ContactForm(initial=data)

        if request.user.is_authenticated():
            user = request.user
            socialAccounts = SocialAccount.objects.filter(user_id=user.id)
            if len(socialAccounts) > 0:
                socialAccount = socialAccounts[0]
                customer = Customer.objects.filter(social=socialAccount)[0]

                data['contact_name'] = customer.customer_name
                data['contact_email'] = customer.email
                data['contact_phone'] = customer.phone_number
                form_class = ContactForm(initial=data)

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
            customerRequest = CustomerRequest(contact_name=contact_name, contact_phone=contact_phone,
                                              contact_email=contact_email, skill=skill_entered,
                                              preferred_communication_time=preferred_communication_time,
                                              content=form_content)
            customerRequest.save()
            sendConfirmationMail(customerRequest)

            return HttpResponseRedirect('/thanks/')
        return render(request, 'proj/request_new.html', {
            'form': form_class,
        })
    except Exception as e:
        print "exception caught"
        print '%s (%s)' % (e.message, type(e))
        traceback.print_exc(file=open("errlog.txt", "a"))

def event(request, topic_code):
    try:

        # print skillName
        events = Event.objects.filter(topic_code=topic_code)

        if len(events) > 0:
            event = events[0]
            skills = Skill.objects.filter(events__in=[event])
            print skills

            return render(request, 'proj/event.html', {
                'skill_list': skills,
                'event_name': event.topic_name,
            })

        else:
            return HttpResponse("Wrong Event Topic")


    except Exception as e:
        print "exception caught"
        print '%s (%s)' % (e.message, type(e))
        traceback.print_exc(file=open("errlog.txt", "a"))


class CustomerSkill(object):
    def __init__(self, customer):
        self.customer = customer
        self.skillMatchs = []


def teachers(request):
    try:
        customers = Customer.objects.filter(no_subjects__gt=0).filter(classes_given__gt=0).extra(
            order_by=('-no_subjects', '-classes_given'))
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
        traceback.print_exc(file=open("errlog.txt", "a"))


def thanks(request):
    return render_to_response('proj/thanks.html')


def updated(request):
    return render_to_response('customers/profile-updated.html')


def ajax_skill_search(request):
    results = []
    q = request.GET.get('q')
    # print q
    if q is not None:
        results = Skill.objects.filter(
            Q(skill_name__icontains=q) | Q(topic__topic_name__icontains=q)
        ).order_by('-classes_given', '-no_teachers', '-clicks')
        # print results
        return render_to_response('proj/results_new.html', {'results': results, })
    return HttpResponse("Some error occurred")


def ajax_skill_topics(request):
    try:
        q = request.GET.get('q')
        if q is None:
            q = ""
        skill_topic_list = SkillTopic.objects.extra(order_by=('-classes_given', '-clicks'))
        skill_parent_topics = []
        predef_list = []
        parent_topic_dict = {}
        if len(q) <= 0:
            predef_list.append(PreDefTrending)
            predef_list.append(PreDefExclusive)
            predef_list.append(PreDefNewArrival)

        for skillTopic in skill_topic_list:
            skills = Skill.objects.filter(topic=skillTopic).filter(visible=True)
            if re.search(q, skillTopic.topic_name, re.IGNORECASE) and len(skills) > 0:
                populate_skill_topics(parent_topic_dict, skillTopic, skill_parent_topics)
            else:
                skills = skills.filter(Q(skill_name__icontains=q)).filter(visible=True)
                if len(skills) > 0:
                    populate_skill_topics(parent_topic_dict, skillTopic, skill_parent_topics)
        template = loader.get_template('proj/results_main_list.html')
        context = {
            'pre_def_list': predef_list,
            'skill_topic_list': skill_parent_topics,
        }
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print "exception caught"
        print '%s (%s)' % (e.message, type(e))
        traceback.print_exc(file=open("errlog.txt", "a"))


def populate_skill_topics(parent_topic_dict, skillTopic, skill_parent_topics):
    parent_topic = skillTopic.parent_topic
    if parent_topic is None and not skill_parent_topics.__contains__(skillTopic):
        skill_parent_topics.append(skillTopic)
    elif not skill_parent_topics.__contains__(parent_topic):
        skill_parent_topics.append(parent_topic)
    '''if parent_topic in parent_topic_dict:
        skill_topics = parent_topic_dict[parent_topic]
    else:
        skill_topics = []
        parent_topic_dict[parent_topic] = skill_topics
    skill_topics.append(skillTopic)'''


def ajax_skills(request, skill_topic_code):
    try:
        q = request.GET.get('q')
        if q is None:
            q = ""
        skillTopics = SkillTopic.objects.filter(topic_code=skill_topic_code)
        skillTopic = skillTopics[0]
        subTopics = SkillTopic.objects.filter(parent_topic=skillTopic)
        topic_list = []
        topic_skill_dict = {}
        skills = []
        for topic in subTopics:
            skills.extend(getSkillsTopics(q, topic, topic_list, topic_skill_dict))

        skills.extend(getSkillsTopics(q, skillTopic, topic_list, topic_skill_dict))
        #print skills
        #print topic_list
        #print topic_skill_dict
        if len(skills) > 0:
            context, template = process_skill_list(skills, topic_list, topic_skill_dict, skillTopic)
            return HttpResponse(template.render(context, request))
        # return HttpResponse(call)
        else:
            return HttpResponse("Wrong skill topic")
    except Exception as e:
        print "exception caught"
        print '%s (%s)' % (e.message, type(e))
        traceback.print_exc(file=open("errlog.txt", "a"))


def getSkillsTopics(q, skillTopic, topic_list, topic_skill_dict):
    if re.search(q, skillTopic.topic_name, re.IGNORECASE):
        skills = Skill.objects.filter(topic__topic_code=skillTopic.topic_code).filter(visible=True).extra(
            order_by=('-classes_given', '-no_teachers', '-clicks'))
    else:
        skills = Skill.objects.filter(topic__topic_code=skillTopic.topic_code).filter(Q(skill_name__icontains=q)).filter(visible=True).extra(
            order_by=('-classes_given', '-no_teachers', '-clicks'))
    if len(skills) > 0:
        topic_list.append(skillTopic)
        topic_skill_dict[skillTopic] = skills
    return skills


def process_skill_list(skills, topic_list, topic_skill_dict, skill_topic, all_events=False):
    skill_match_list = get_skill_match_list(skills)
    if all_events:
        event_list = get_event_list()
    else:
        event_list = get_event_list(skills)
    print event_list
    template = loader.get_template('proj/results_skill_topic.html')
    context = {
        'skill_list': skills,
        'skill_match_list': skill_match_list,
        'topic_list': topic_list,
        'topic_skill_dict': topic_skill_dict,
        'skill_topic': skill_topic,
        'event_list': event_list,
    }
    return context, template

def get_event_list(skills=None):
    if skills:
        event_list = []
        #print skills
        for skil in skills:
            #print skil
            events = skil.events
            #print events
            #print skill_matches
            event_list.extend(events.all())
            #print skill_match_list
        return set(event_list)
    else:
        return Event.objects.all()


def get_skill_match_list(skills):
    skill_match_list = []
    #print skills
    for skil in skills:
        #print skil
        skill_matches = SkillMatch.objects.filter(skill=skil).filter(classes_given__gt=0).filter(visible=True).order_by('-classes_given')
        #print skill_matches
        skill_match_list.extend(skill_matches)
        #print skill_match_list
    return sorted(skill_match_list, key=operator.attrgetter('classes_given'), reverse=True)


# return skill_match_list


def ajax_skills_predef(request, predef_name):
    try:
        # print predef_name
        if predef_name.lower() == PreDefTrending.code.lower():
            orderskills = Skill.objects.filter(exclusive=False).filter(visible=True).extra(
                order_by=('-classes_given', '-no_teachers', '-clicks'))[:20]
            if len(orderskills) > 0:
                topic_list = []
                topic_list.append(PreDefTrending)
                topic_skill_dict = {}
                topic_skill_dict[PreDefTrending] = orderskills
                context, template = process_skill_list(orderskills, topic_list, topic_skill_dict, PreDefTrending, True)
                return HttpResponse(template.render(context, request))
            else:
                return HttpResponse("Wrong topic")
        elif predef_name.lower() == PreDefNewArrival.code.lower():
            newArrivals = Skill.objects.filter(exclusive=False).filter(visible=True).extra(order_by=('-created_date', 'clicks'))[:20]
            if len(newArrivals) > 0:
                topic_list = []
                topic_list.append(PreDefNewArrival)
                topic_skill_dict = {}
                topic_skill_dict[PreDefNewArrival] = newArrivals
                context, template = process_skill_list(newArrivals, topic_list, topic_skill_dict, PreDefNewArrival, True)
                return HttpResponse(template.render(context, request))
            else:
                return HttpResponse("Wrong topic")
        elif predef_name.lower() == PreDefExclusive.code.lower():
            exclusives = Skill.objects.filter(exclusive=True).filter(visible=True).extra(
                order_by=('-classes_given', '-no_teachers', '-clicks'))
            if len(exclusives) > 0:
                topic_list = []
                topic_list.append(PreDefExclusive)
                topic_skill_dict = {}
                topic_skill_dict[PreDefExclusive] = exclusives
                context, template = process_skill_list(exclusives, topic_list, topic_skill_dict, PreDefExclusive, True)
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


def skill_lookup(request):
    try:
        # Default return list
        results = []
        model_results = Skill.objects.filter(visible=True)
        results = [{"skill_name": x.skill_name, "skill_code": x.skill_code, "topic_name": x.topic.topic_name} for x in model_results]
        json1 = json.dumps(results)
        #print json1
        return HttpResponse(json1, content_type = 'application/json')
        #return JsonResponse(dict(names=list(Skill.objects.filter(visible=True).values('skill_name'))))
    except Exception as e:
        print "exception caught"
        print '%s (%s)' % (e.message, type(e))
        traceback.print_exc(file=open("errlog.txt", "a"))

#@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
register.filter('get_item', get_item)

