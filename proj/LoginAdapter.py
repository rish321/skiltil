from __future__ import print_function
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount
from django.core.mail import EmailMultiAlternatives

from django.db.models import Q
from django.template.loader import render_to_string

from customers.models import Customer


def sendWelcomeMail(customer):
    html = render_to_string('customers/new_customer.html', {'customer': customer})
    email = EmailMultiAlternatives(
        'Welcome to skiltil',
        'Hi ' + customer.customer_name + ',\n Your account has been activated. Now explore the endless learning experience only at Skiltil.',
        'support@skiltil.com', [customer.email],
        headers={'IsTransactional': "True"}, )
    email.attach_alternative(html, "text/html")
    email.send()
    pass


class LogAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):

        super(LogAdapter, self).save_user(request, sociallogin, form)

        print(sociallogin.user.id)

        print(sociallogin.user.email)
        response_email = sociallogin.user.email
        socialAccounts = SocialAccount.objects.filter(user_id=sociallogin.user.id)
        if len(socialAccounts) > 0:
            socialAccount = socialAccounts[0]
            print(socialAccount.provider)
            print(socialAccount)
            response_gender = "d"
            if socialAccount.provider == 'facebook':
                response_extra = socialAccount.extra_data
                response_gender = response_extra.get("gender")
                # print (response_gender)
                if response_gender == 'male':
                    response_gender = 'm'
                if response_gender == 'female':
                    response_gender = 'f'
                if response_email is None:
                    response_email = socialAccount.uid + "@facebook.com"
                # print (response_email)
                response_name = response_extra.get('name')
                # print (response_name)
                image_large = "http://graph.facebook.com/" + socialAccount.uid + "/picture?type=large"
                # print (image_large)
                self.save_customer_data(image_large, response_email, response_gender, response_name, socialAccount)

            if socialAccount.provider == 'google':
                response_extra = socialAccount.extra_data
                if hasattr(response_extra, 'gender'):
                    response_gender = response_extra.get("gender")
                    if response_gender == 'Male':
                        response_gender = 'm'
                    if response_gender == 'Female':
                        response_gender = 'f'
                    if response_email is None:
                        response_email = socialAccount.uid + "@gmail.com"
                response_name = response_extra.get('name')
                image_large = response_extra.get('picture')
                self.save_customer_data(image_large, response_email, response_gender, response_name, socialAccount)

    def save_customer_data(self, image_large, response_email, response_gender, response_name, socialAccount):
        if response_email is None:
            return
        customers = Customer.objects.filter(email=response_email)
        # print (customers)
        if len(customers) > 0:
            if len(customers) == 1:
                customer = customers[0]
                if customer.social is None:
                    customer.social = socialAccount
                customer.customer_name = response_name
                customer.gender = response_gender
                customer.image = image_large
                customer.save()
        else:
            # user doesn't exist in customers
            customer = Customer(email=response_email, social=socialAccount, customer_name=response_name,
                                image=image_large,
                                gender=response_gender)
            customer.save()
            sendWelcomeMail(customer)
