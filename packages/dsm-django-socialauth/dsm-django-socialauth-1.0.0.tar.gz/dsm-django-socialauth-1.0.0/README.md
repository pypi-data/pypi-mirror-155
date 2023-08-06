Djagno DSM Authentication
========================

Requirements
============
- python (2.7, 3.5)
- django (1.11, 2.0)
- social-app-django (2.1.0)

Installation
============
```
pip install git+https://gitlab.com/public-project2/dsm-django-oauth
```

Usage
=====
### Prerequisite

- must be ```PROTOCOL://HOST/oauth/complete/dsmauth/```
> note: Callback URL must be same with decarelation in urls.py
> 
> in this example use http://127.0.0.1/oauth/complete/dsmauth/

### in setting.py 
```python
INSTALLED_APPS = [
    ...
    'social_django',
    'dsmauth',
    ...
]
```
add authentication backend in setting.py
```python
AUTHENTICATION_BACKENDS = [
    ...
    'django.contrib.auth.backends.ModelBackend',
    'dsmauth.backend.dsmOAuth2',
    ...
]
```
set client id and client secret in setting.py
```python
SOCIAL_AUTH_DSMAUTH_KEY = '<client_id>'
SOCIAL_AUTH_DSMAUTH_SECRET = '<client_secret>'
```

Sample SOCIAL_AUTH_PIPELINE
```python
SOCIAL_AUTH_PIPELINE = [ 
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'social_core.pipeline.social_auth.associate_by_email',
]
```
Add login redirect
```python
LOGIN_REDIRECT_URL='<path to redirect>'
```
Setauth server name and url
```python
OAUTH_DSM_SERVER_BASEURL = 'auth.storemesh.com'
```
> See more detail about **social-app-django** in (https://github.com/python-social-auth/social-app-django)

### in urls.py
```
urlpatterns = [
    ...
    path('oauth/', include('social_django.urls', namespace='social')), # in django2
    ...
]
```

### in template
```
    ...
        <a href="{% url 'social:begin' 'dsmauth' %}">Login with ...</a>
    ...
```

# If use backend-frontend model
can use authentication with JWT
### in urls.py
```python
from dsmauth.complete import complete
urlpatterns = [
    ...
    path('oauth/complete/<str:backend>/', complete, name='complete'),
    path('oauth/', include('social_django.urls', namespace='social')),
    ...
]
```
### in settings.py
```python
BASE_FRONTEND_URL='http://localhost:3000/'
```