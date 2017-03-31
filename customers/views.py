import traceback

from allauth.socialaccount.models import SocialAccount
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.http import HttpResponse

from django.template import loader

# Create your views here.
from customers.forms import ProfileForm
from customers.models import Customer, SkillMatch
from proj.models import Skill
from session.models import Session
import json


def show_profile(request):
    try:
        if request.user.is_authenticated():
            user = request.user
            socialAccount = SocialAccount.objects.filter(user_id = user.id)[0]
            customer = Customer.objects.filter(social = socialAccount)[0]
            skillMatches = SkillMatch.objects.filter(customer = customer)
            skillMatchesVerified = skillMatches.filter(verified = True)
            skillMatchesUnverified = skillMatches.filter(verified=False)

            classes = Session.objects.filter(Q(student = customer) | Q(skill_match__customer = customer)).order_by('start_time')


            data = {'contact_name': customer.customer_name, 'contact_email': customer.email, 'contact_phone': customer.phone_number}
            form_class = ProfileForm(initial=data)

            template = loader.get_template('customers/profile.html')
            context = {
                'customer': customer,
                'form': form_class,
                'skill_matches_verified': skillMatchesVerified,
                'skill_matches_unverified': skillMatchesUnverified,
                'classes': classes,
            }

            if request.method == 'POST':
                #form = ProfileForm(data=request.POST)

                #if form.is_valid():
                contact_name = request.POST.get(
                        'contact_name'
                        , '')
                contact_phone = request.POST.get(
                        'contact_phone'
                        , '')

                #form_content = request.POST.get('content', '')
                customer.customer_name=contact_name
                customer.phone_number=contact_phone
                customer.save()

                return HttpResponseRedirect('/profile-updated/')

            return HttpResponse(template.render(context, request))
        else:
            return HttpResponseRedirect('/accounts/login')
    except Exception as e:
        print "exception caught"
        print '%s (%s)' % (e.message, type(e))
        traceback.print_exc(file=open("errlog.txt", "a"))


def update_skills(request):
    try:
        if request.user.is_authenticated():
            user = request.user
            socialAccount = SocialAccount.objects.filter(user_id=user.id)[0]
            customer = Customer.objects.filter(social=socialAccount)[0]

            json1 = json.loads(request.POST['msg'])
            for skill_name in json1:
                skills = Skill.objects.filter(skill_name = skill_name)
                if len(skills) > 0:
                    skill = skills[0]
                    if len(SkillMatch.objects.filter(skill = skill).filter(customer = customer)) <= 0:
                        skillMatch = SkillMatch(customer=customer, skill=skill)
                        skillMatch.save()

            return HttpResponseRedirect('/profile-updated/')
        else:
            return HttpResponseRedirect('/accounts/login')

    except Exception as e:
        print "exception caught"
        print '%s (%s)' % (e.message, type(e))
        traceback.print_exc(file=open("errlog.txt", "a"))