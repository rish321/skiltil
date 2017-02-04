from social.apps.django_app.middleware import SocialAuthExceptionMiddleware
from django.shortcuts import HttpResponse
from social import exceptions as social_exceptions
import traceback


class SocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def process_exception(self, request, exception):
        print "exception caught"
        print '%s (%s)' % (exception.message, type(exception))
        traceback.print_exc(file=open("errlog.txt", "a"))
        if hasattr(social_exceptions, 'AuthCanceled'):
            return HttpResponse("I'm the Pony %s" % exception)
        else:
            raise exception
