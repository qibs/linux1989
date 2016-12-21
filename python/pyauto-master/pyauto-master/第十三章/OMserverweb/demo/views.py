from django.utils.log import logging
from django.http import HttpResponse  

def index(request):
    logging.error('Test Django Logging')
    return HttpResponse("Hello world Django.")
