from django.contrib.auth import authenticate, login
from django.contrib.sessions.models import Session
from django.shortcuts import render_to_response, HttpResponse, render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from mychat.models import ChatMessage, LastActive
import datetime
import time
from django.contrib.auth.models import User


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
    print "========="
    print state
    if state:
        return render_to_response('auth.html',{'state':state, 'username': username})
    return render_to_response('chat.html',{'state':state, 'username': username})


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
    print "=" * 50
    
    print request.session.session_key
    #print request
    print "=" * 50
    if not request.is_ajax():
        return  HttpResponse (" Not an AJAX request ")  
    if request.method == 'GET':
        
        
        last_active = None
        try:
            last_active = LastActive.objects.get(user = request.user)
            last_active.session = Session.objects.get(session_key = request.session.session_key)
            last_active.save()
        except:
            last_active = LastActive.objects.create(user = request.user, session = Session.objects.get(session_key = request.session.session_key))        
        last_active.save()
        
        chat_list = ChatMessage.objects.filter(receiver = request.user, is_read = False)
        #session = Session.objects.get(session_key = request.session.session_key)        
        print chat_list
        for chat in chat_list:  
            chat.is_read = True
            print chat.is_read
            chat.save()
            print chat.is_read          
            return HttpResponse (chat.sender.username + ":" + chat.message)
    print "========= After Scaling ==============="
       
    return HttpResponse('ACTIVE:' + find_online_users(request.user.username))
