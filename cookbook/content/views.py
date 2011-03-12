from django.views.generic.simple import direct_to_template


def homepage(request):
    return direct_to_template(request, template='content/homepage.html')

