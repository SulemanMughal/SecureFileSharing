import json
import requests
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .shorten import Shortener
from django.conf import settings
import datetime
from datetime import timedelta
from django.http import HttpResponse, HttpResponseNotFound

import uuid
from .choices import FILE_EXPIRE_OPTIONS, DESTROY_AFTER_DOWNLOAD
import traceback
from django.contrib import messages

from django.http import FileResponse


from .models import *
import os
from .send_email import email_send

from filehash import FileHash
sha1hasher = FileHash('sha1')


# gmail configurations


import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request 


from master_app.middleware import get_client_ip



def redirect_to_original_url(request, token , filename=None):
    # print(filename)
    try:
        uploaded_document = Document.objects.get(token=token)
    except : 
        traceback.print_exc()
        return render(request, "master_app/FileNotFound.html", status=404)
    file_location = uploaded_document.document.path
    ip, user_agent = get_client_ip(request)
    DocumentLogs.objects.create(document=uploaded_document, public_ip_address=ip, user_agent=user_agent)
    try:    
        if (uploaded_document.valid_link is False):
            return render(request, "master_app/FileNotFound.html", status=404)
        elif uploaded_document.valid_link is True:
            if uploaded_document.destroyAfterDownload is True:
                uploaded_document.valid_link = False
                uploaded_document.save()
                return FileResponse(open(file_location, 'rb'), as_attachment=True, filename=f"{uploaded_document.name}")
            else : 
                current_timestamp = datetime.datetime.now().timestamp()
                file_created_timestamp = uploaded_document.uploaded_at.timestamp()
                file_expires_timestamp = uploaded_document.expires_at.timestamp()
                if file_created_timestamp < current_timestamp < file_expires_timestamp : 
                    return FileResponse(open(file_location, 'rb'), as_attachment=True, filename=f"{uploaded_document.name}")
                else : 
                    uploaded_document.valid_link = False
                    uploaded_document.save()
                    return render(request, "master_app/FileNotFound.html", status=404)
    except :
        traceback.print_exc()
        return render(request, "master_app/FileNotFound.html", status=404)



def manage_files(request, document_id):
    template_name="master_app/manage.html"
    try:
        uploaded_document = Document.objects.get(id = document_id)
        if uploaded_document.valid_link is False:
            return render(request, "master_app/FileNotFound.html", status=404)
        if request.GET.get("delete", None) == "1" :
            uploaded_document.delete()
            messages.success( request, "File has been deleted Successfully")
            return redirect("index")
        
        if request.GET.get("toggleautodestroy", None) == "1" :
            messages.success( request, "File will be destroy after downloading.")
            uploaded_document.destroyAfterDownload = True
            uploaded_document.save()
        elif request.GET.get("toggleautodestroy", None) == "0" :
            messages.success( request, "Destroy File After Download has been disabled")
            uploaded_document.destroyAfterDownload = False
            uploaded_document.save()
            # uploaded_document.delete()
            # return redirect("index")

        if request.GET.get("expire", None):
            uploaded_document.expires_at = uploaded_document.uploaded_at + timedelta( seconds=FILE_EXPIRE_OPTIONS[request.GET.get("expire", "2")])

            uploaded_document.save()
            messages.success( request, "The file expiry has been updated")
        
        context = {
            "uploaded_document" : uploaded_document
        }
        return render(request, template_name, context)
    except :
        traceback.print_exc()
        return render(request, "master_app/FileNotFound.html", status=404)


async  def send_notification_to_telegram(message):
    TOKEN = f"{settings.TOKEN}"
    chat_id = f"{settings.CHAT_ID}"
    message = f"{message}"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url).json()
    return JsonResponse({'message': 'Notification sent successfully'})


@csrf_exempt
def index(request):
    template_name="master_app/index.html"
    # print(request.method, request.POST)
    context={
    }
    if request.method == "GET":
        return render(request, template_name, context)
    elif request.method == 'POST' and request.FILES.get('file'):
        # print(request.POST)
        # print(request.POST.get("randomizefn", False) )
        # shorturl
        random_filename = False
        enable_shorturl = True
        if request.POST.get("randomizefn", False) == "true"  or request.POST.get("randomizefn", False) is True:
            random_filename = True
        if request.POST.get("shorturl", False) == "false"  or request.POST.get("shorturl", False) is False:
            enable_shorturl = False
        ip, user_agent = get_client_ip(request)
        token = Shortener().generate_token()
        myFile = request.FILES.get('file')
        # print(myFile)
        # name, extension = os.path.splitext(myFile.name)
        # print("Filename:", name)
        # print("Extension:", extension)
        uploaded_document = Document.objects.create(
            document=myFile, 
            name=myFile.name, 
            token=token, 
            file_type=myFile.content_type, 
            user_agent=user_agent, 
            ip_address=ip, 
            random_filename=random_filename,
            enable_shorturl = enable_shorturl
        )
        try:
            print("File Upload")
            uploaded_document.short_url= f'{settings.HTTP_PROTOCOL}://{settings.DOMAIN_NAME_OR_IP_ADDRESS}/t/{token}' 
            uploaded_document.long_url= f'{settings.HTTP_PROTOCOL}://{settings.DOMAIN_NAME_OR_IP_ADDRESS}{uploaded_document.document.url}'
            randomFileName = Shortener().generate_token() +  "." +  myFile.name.split(".")[-1]
            if random_filename is True:
                uploaded_document.name =  randomFileName

            # check short url is not enable
            if enable_shorturl is False:
                if random_filename is True:
                    uploaded_document.short_url= f'{settings.HTTP_PROTOCOL}://{settings.DOMAIN_NAME_OR_IP_ADDRESS}/t/{token}/{randomFileName}' 
                else:
                    uploaded_document.short_url= f'{settings.HTTP_PROTOCOL}://{settings.DOMAIN_NAME_OR_IP_ADDRESS}/t/{token}/{myFile.name}' 
            uploaded_document.file_hash= sha1hasher.hash_file(uploaded_document.document.path)
            uploaded_document.expires_at = uploaded_document.uploaded_at + timedelta( seconds=FILE_EXPIRE_OPTIONS[request.POST.get("expire", "2")])
            uploaded_document.file_size = uploaded_document.document.size
            uploaded_document.destroyAfterDownload = DESTROY_AFTER_DOWNLOAD[request.POST.get(  'autodestroy', 'false')]
            uploaded_document.save()
            data=f"User-Agent:\t{user_agent}\nIP Address:\t{ip}\nUploaded Document:\t{uploaded_document.long_url}"
            # url = f"{settings.HTTP_PROTOCOL}://{settings.DOMAIN_NAME_OR_IP_ADDRESS}/send_notification/?message={data}"
            # requests.get(url, timeout=3).json()
            # Send Gmail
            email_send(data)

        except Exception as e: 
            traceback.print_exc()
        return JsonResponse({'File Access URL': uploaded_document.short_url , "File ID" : str(uploaded_document.pk)})
    else :
        return JsonResponse({'error':'Method not found'})

def abuse(request):
    template_name="master_app/abuse.html"

    if request.method == "POST":
        # print(request.POST)
        if request.POST.get("url", None) is None:
            messages.error(request, "Abusive file url is required")
        else:
            Reports.objects.create(
                url = request.POST.get("url", None),
                email = request.POST.get("email", None),
                comments = request.POST.get("comment", None)
            )
            messages.success(request, "The file has been successfully reported.")
    context={
    
    }
    return render(request, template_name, context)



def privacy_policy(request):
    template_name="master_app/privacy_policy.html"
    context={
    
    }
    return render(request, template_name, context)







def media_access(request, path):
    """
    When trying to access :
    myproject.com/media/uploads/passport.png

    If access is authorized, the request will be redirected to
    myproject.com/protected/media/uploads/passport.png

    This special URL will be handle by nginx we the help of X-Accel
    """

    # access_granted = False

    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            response = HttpResponse()
            del response['Content-Type']
            response['X-Accel-Redirect'] = '/protected/media/' + path
            return response
    
    # return HttpResponseForbidden('Not authorized to access this media.')
    return render(request, "master_app/FileNotFound.html", status=404)






# sudo journalctl -u gunicorn
# sudo systemctl restart gunicorn
# sudo systemctl daemon-reload
# sudo systemctl restart gunicorn.socket gunicorn.service
# sudo nginx -t && sudo systemctl restart nginx
# sudo tail /var/log/nginx/error.log
