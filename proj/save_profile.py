from profile import Profile
from customers.models import Customer


def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        print user
        print user._meta.get_fields()
        print user.id
        print user.password
        print user.last_login
        print user.is_superuser
        #user.is_superuser = False
        print user.username
        print user.first_name
        print user.last_name
        print user.email
        print user.is_staff
        #user.is_staff = False
        print user.is_active
        print user.date_joined
        print user.groups
        print user.user_permissions
        print response
        for key in response:
            print key
        print response.get('gender')
        print response.get('link')
        print response.get('email')