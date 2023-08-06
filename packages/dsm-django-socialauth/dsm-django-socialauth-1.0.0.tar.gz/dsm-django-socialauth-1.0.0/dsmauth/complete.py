
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import REDIRECT_FIELD_NAME
from social_core.actions import do_complete
from social_django.views import _do_login
from social_django.utils import psa
from social_core.utils import setting_name

from rest_framework_simplejwt.tokens import RefreshToken

NAMESPACE = getattr(settings, setting_name('URL_NAMESPACE'), None) or 'social'

@never_cache
@csrf_exempt
@psa('{0}:complete'.format(NAMESPACE))
def complete(request, backend, *args, **kwargs):
    """Authentication complete view"""
    do_complete(request.backend, _do_login, user=request.user,
                       redirect_name=REDIRECT_FIELD_NAME, request=request,
                       *args, **kwargs)
    user = request.user
    token = getToken(user)
    return HttpResponseRedirect("{}callback/?token={}".format(settings.BASE_FRONTEND_URL,token))

def getToken(user):
    refresh = RefreshToken.for_user(user)
    '''
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    '''
    return str(refresh)