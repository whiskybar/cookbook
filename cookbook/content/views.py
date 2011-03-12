from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse


def homepage(request):
    return TemplateResponse(request, template='content/homepage.html')


def go_home(request):
    if request.user.is_authenticated():
        return redirect(reverse('user_homepage', kwargs=dict(username=request.user.username)))
    else:
        return redirect('homepage')
