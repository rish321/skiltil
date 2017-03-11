import traceback

from allauth.socialaccount.models import SocialAccount
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.http import HttpResponse

from django.template import loader

# Create your views here.
from customers.forms import ProfileForm
from customers.models import Customer


def show_profile(request):
    try:
        if request.user.is_authenticated():
            user = request.user
            socialAccount = SocialAccount.objects.filter(user_id = user.id)[0]
            customer = Customer.objects.filter(social = socialAccount)[0]

            data = {'contact_name': customer.customer_name, 'contact_email': customer.email, 'contact_phone': customer.phone_number}
            form_class = ProfileForm(initial=data)

            template = loader.get_template('customers/profile.html')
            context = {
                'customer': customer,
                'form': form_class,
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
            return HttpResponseRedirect('/login')
    except Exception as e:
        print "exception caught"
        print '%s (%s)' % (e.message, type(e))
        traceback.print_exc(file=open("errlog.txt", "a"))

