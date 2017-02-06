from profile import Profile
from customers.models import Customer
from django.db.models import Q

def save_profile(backend, social, response, *args, **kwargs):
    if backend.name == 'facebook':
        print social
        if not social is None:
            print social._meta.get_fields()
            print social.uid
            print social.user
            if not social.user is None:
                print social.user._meta.get_fields()
                print social.user.is_authenticated()
                print social.user.is_superuser
                print social.user.is_staff
        #print user.id
        #print user.password
        #print user.last_login
        #print user.is_superuser
        #user.is_superuser = False
        #print user.username
        #print user.first_name
        #print user.last_name
        #print user.email
        #print user.is_staff
        #user.is_staff = False
        #print user.is_active
        #print user.date_joined
        #print user.groups
        #print user.user_permissions
        #print response
        #for key in response:
        #    print key
        response_gender = response.get('gender')
        print response_gender
        if response_gender == 'male':
            response_gender = 'm'
        if response_gender == 'female':
            response_gender = 'f'

        print response.get('link')
        response_email = response.get('email')
        print response_email
        if response_email is None:
            response_email = response.get('id')+"@facebook.com"
        response_name = response.get('name')
        print response_name
        email = response_email
        customers = Customer.objects.filter(Q(email=email) | Q(gmail_id=email))
        image_large = "http://graph.facebook.com/" + response.get("id") + "/picture?type=large"
        print image_large
        if len(customers) > 0:
            # user exists in customers
            if len(customers) == 1:
                # user exists only once
                customer = customers[0]
                if customer.social is None:
                    customer.social = social
                customer.customer_name = response_name
                customer.gender = response_gender
                customer.image = image_large
                customer.save()
        else:
            #user doesn't exist in customers
            customer = Customer(email=response_email, social=social, customer_name=response_name, image =image_large, gender =response_gender)
            customer.save()

    else:
        print social
        if not social is None:
            print social._meta.get_fields()
            print social.uid
            print social.user
            if not social.user is None:
                print social.user._meta.get_fields()
                print social.user.is_authenticated()
                print social.user.is_superuser
                print social.user.is_staff
