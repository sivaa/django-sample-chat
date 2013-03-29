from django.utils import translation
from django.contrib.auth import authenticate, login
from django.contrib.sessions.models import Session
from django.shortcuts import render_to_response, HttpResponse, render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from mychat.models import ChatMessage, LastActive, VideoSession
import datetime
import time
from django.contrib.auth.models import User

import OpenTokSDK

@csrf_exempt
def login_user(request):
    state = "Login Below...."
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = None
                #state = "You're successfully logged in!"
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."
#    print "========="
#    print state
    
    
    print "=" * 50
    print request.LANGUAGE_CODE
    print translation.get_language_from_request(request)        
    #translation.activate('de')
    print translation.get_language()

    print "=" * 50
    
    
    if state:
        return render_to_response('auth.html', locals(), context_instance=RequestContext(request))
    return render_to_response('chat.html', locals(), context_instance=RequestContext(request))
        
#    if state:
#        return render_to_response('auth.html',{'state':state, 'username': username})
#    return render_to_response('chat.html',{'state':state, 'username': username, 'session_id': session_id, 'token_id': token_id})
                          

@csrf_exempt
def post(request):
    time.sleep(2)
    if not request.is_ajax():
        HttpResponse (" Not an AJAX request ")
    if request.method == 'POST':
        if request.POST['message']:
            message = request.POST['message']
            to_user = request.POST['to_user']
            ChatMessage.objects.create(sender = request.user, receiver = User.objects.get(username = to_user), message = message,  session = Session.objects.get(session_key = request.session.session_key))
       
    return HttpResponse (" Not an POST request ")


@csrf_exempt
def find_online_users(username):
    last_active_list = LastActive.objects.filter(received_at__gt = datetime.datetime.now() - datetime.timedelta(seconds=5))
    users_list = []
    for last_active in last_active_list:
        users_list.append(last_active.user.username)    
    users_list.remove(username)
    return ",".join(users_list)


def get(request):
    if not request.is_ajax():
        return  HttpResponse (" Not an AJAX request ")  
    if request.method == 'GET':       
        
        last_active = None
        try:
            last_active = LastActive.objects.get(user = request.user)
        except:
            last_active = LastActive.objects.create(user = request.user, session = Session.objects.get(session_key = request.session.session_key))
        last_active.save()
        
        chat_list = ChatMessage.objects.filter(receiver = request.user, is_read = False)
        #session = Session.objects.get(session_key = request.session.session_key)        
        #print chat_list
        for chat in chat_list:  
            chat.is_read = True
            chat.save()
            return HttpResponse (chat.sender.username + ":" + chat.message)
    #print "========= After Scaling ==============="       
    return HttpResponse('ACTIVE:' + find_online_users(request.user.username))


def vchat_req(request):
    if request.GET:
        receiver = request.GET.get('to')         
        
        video_session = None
        try:
            video_session = VideoSession.objects.get(sender = request.user, receiver = User.objects.get(username = receiver))
        except:
            video_session = VideoSession.objects.create(sender = request.user, receiver = User.objects.get(username = receiver))
            

        api_key         = '24175212' # Replace with your OpenTok API key.
        api_secret      = '40f335ab2eb8bcd4c5f6c4c7cfa70638c1aff011'  # Replace with your OpenTok API secret.
        session_address = request.META.get('REMOTE_ADDR') # Replace with the representative URL of your session.
        
        opentok_sdk = OpenTokSDK.OpenTokSDK(api_key, api_secret)
        session     = opentok_sdk.create_session(session_address, {'p2p_preference':'enabled'})
        
        connectionMetadata  = 'username=' + request.user.username + ', userLevel=4'
        token               = opentok_sdk.generate_token(session.session_id, OpenTokSDK.RoleConstants.PUBLISHER, None, connectionMetadata)

        video_session.session_id    = session.session_id
        video_session.token_id      = token            
        video_session.save()
        
        session_id  = session.session_id
        token_id    = token
        message = 'VCHAT_REQ->' + request.user.username
        ChatMessage.objects.create(sender = request.user, receiver = User.objects.get(username = receiver), message = message,  session = Session.objects.get(session_key = request.session.session_key))
        
        return render_to_response('vchat.html', locals(), context_instance=RequestContext(request))
    
def vchat_join(request):
    if request.GET:
        receiver = request.GET.get('from')         
        
        video_session = None
        try:
            video_session = VideoSession.objects.get(receiver = request.user, sender = User.objects.get(username = receiver))
        except:
            return HttpResponse ("There is request now!")
            
        video_session
        
        session_id  = video_session.session_id
        token_id    = video_session.token_id
        
        return render_to_response('vchat.html', locals(), context_instance=RequestContext(request))