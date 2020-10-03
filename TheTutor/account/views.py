from django.shortcuts import render
from django.http import HttpResponse
from .models import User
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
import random
import csv
import os
import shutil

FILE_PATH = "/home/TheTutor/userData/"

# Create your views here.
@csrf_exempt
def account(request):
    return HttpResponse("HELLO")


@csrf_exempt
def signup(request):
    Userid = request.POST.get('userid')
    Password = request.POST.get('password')
    Name = request.POST.get('name')
    print(Userid, Password, Name)
    
    f = open(FILE_PATH + "userNum.txt", 'r')
    line = f.read()
    if(line == ''):
        line = '0'
    num = int(line)
    f.close()

    newUser = User(userid = Userid, password = Password, name = Name, idCode = num + 1)
    try:
        num = num + 1
        f = open(FILE_PATH + "userNum.txt", 'w')
        f.write(str(num))
        f.close()

        newUser.save(force_insert = True)

        makeWeight(str(num))

        return HttpResponse('1')
    
    except Exception as e:
        print(e)
        return HttpResponse('0')


@csrf_exempt
def makeWeight(idCode):
        try:
            if not(os.path.isdir(FILE_PATH + idCode)):
                os.makedirs(os.path.join(FILE_PATH + idCode))
        except Exception as e:
            print(e)

        f = open(FILE_PATH + idCode + "/weight1.csv", 'w', encoding='utf-8', newline='')
        wr = csv.writer(f)
        
        nodeList1 = [400, 3200, 7680, 40, 80, 96]
        nodeList2 = [8480, 1600, 200, 80, 20, 10]

        for _ in nodeList1:
            temp = list()
            for i in range(_):
                temp.append(str(random.random() / 5.0))
            wr.writerow(temp)
        
        f.close()
        
        f = open(FILE_PATH + idCode + "/weight2.csv", 'w', encoding='utf-8', newline='')
        wr = csv.writer(f)

        for _ in nodeList2:
            temp = list()
            for i in range(_):
                temp.append(str(random.random() / 5.0))
            wr.writerow(temp)

        f.close()


@csrf_exempt
def login(request):
    Userid = request.POST.get('userid')
    Password = request.POST.get('password')
    print(Userid, Password)

    if(not Userid):
        return HttpResponse('-1')

    queryset = User.objects.filter(userid = Userid, password = Password)
    query = User.objects.all()

    print(queryset)
    if(queryset):
        return HttpResponse('1')
    else:
        return HttpResponse('0')


@csrf_exempt
def delete(request):
    Userid = request.POST.get('userid')
    try:
        User_bp = User.objects.get(userid = Userid)
        IDCode = User_bp.idCode
        shutil.rmtree(FILE_PATH + str(IDCode) + "/")
        User_bp.delete()
        return HttpResponse('1')
    except Exception as e:
        print(e)
        return HttpResponse('0')


@csrf_exempt
def sendCode(request):
    code = random.randrange(100000, 1000000)
    Userid = request.POST.get('userid')
    EmailType = request.POST.get('emailType')
    #EMAIL CODE HERE
    if EmailType == "FIND":
        email = EmailMessage('The Tutor 비밀번호 재설정 인증 메일', ('안녕하세요 The Tutor 서비스입니다.\n\n이 메일은 비밀번호 재설정 메일입니다.\n\n확인 코드는 [' + str(code) + ']입니다. 앱에서 입력해주세요.\n\n본인이 메일을 전송한 것이 아니라면 무시해도 좋습니다.\n\nThe Tutor 서비스 드림.' ), to=[Userid])
    elif EmailType == "REGS":
        email = EmailMessage('The Tutor 회원가입 인증 메일', ('안녕하세요 The Tutor 서비스입니다.\n\n이 메일은 회원가입 인증 메일입니다.\n\n확인 코드는 [' + str(code) + ']입니다. 앱에서 입력해주세요. \n\n본인이 메일을 전송한 것이 아니라면 무시해도 좋습니다.\n\nThe Tutor 서비스 드림.'), to=[Userid])
    try:
        email.send()
        return HttpResponse(code)
    except Exception as e:
        print(e)
        return HttpResponse('0')


@csrf_exempt
def getNotification(request):
    #공지 여부 있으면 1 없으면 0
    isNoti = "1"
    # 제목
    title = "서버 공지 테스트입니다."
    # 내용 , 엔터는 //로 작성하기&는 빼기
    content = "안녕하세요//서버 Notification 공지 테스트입니다.//1234567890 !@#$%^*//감사합니다."
    # YYYYMMDD 형식
    notiDate = "20200718"
    try:
        return HttpResponse(isNoti + "\n" + title + "\n" + content + "\n" + notiDate)
    except Exception as e:
        print(e)
        return HttpResponse('NONE')


@csrf_exempt
def sendFeedback(request):
    Userid = request.POST.get('email')
    Title = request.POST.get('title')
    Content = request.POST.get('content')
    print(Userid, Title, Content)

    print("try to send Feedback...")
    emailToUser = EmailMessage("The Tutor 문의사항 접수 안내입니다", ("다음과 같은 내용으로 문의 사항이 접수 완료되었습니다.\n__________\n\n" + "제목 : " + Title + "\n문의 내용 : \n" + Content + "\n____________\n\n빠른 시일 내에 답변드릴 수 있도록 노력하겠습니다. 감사합니다. \n\nThe Tutor 서비스 드림."), to=[Userid])
    email = EmailMessage(("문의 메일 : " + Title), ("회신 주소 : " + str(Userid) + "\n\n" + Content), to=["thetutormailservice@gmail.com"])
    try:
        email.send()
        emailToUser.send()
        return HttpResponse('1')
    except Exception as e:
        print(e)
        return HttpResponse('0')


@csrf_exempt
def changePassword(request):
    Userid = request.POST.get('userid')
    newPassword = request.POST.get('password')
    try:
        User_bp = User.objects.get(userid = Userid)
        User_bp.password = newPassword
        User_bp.save()
        return HttpResponse('1')
    except Exception as e:
        print(e)
        return HttpResponse('0')


@csrf_exempt
def clearTime(request):
    Userid = request.POST.get('userid')
    try:
        User_bp = User.objects.get(userid = Userid)
        User_bp.time_day = "0-0-0-0-0-0-0"
        User_bp.time_sub = "0-0-0-0-0-0-0-0-0-0"
        User_bp.save()
        return HttpResponse('1')
    except Exception as e:
        print(e)
        return HttpResponse('0')


@csrf_exempt
def updateTime(request):
    Userid = request.POST.get('userid')
    dayTime = request.POST.get('dayTime')
    subTime = request.POST.get('subTime')
    try:
        User_bp = User.objects.get(userid = Userid)
        User_bp.time_day = dayTime
        User_bp.time_sub = subTime
        User_bp.save()
        return HttpResponse('1')
    except Exception as e:
        print(e)
        return HttpResponse('0')


@csrf_exempt
def saveSub(request):
    Userid = request.POST.get('userid')
    subNum = request.POST.get('subNum')
    subName = request.POST.get('subName')
    try:
        User_bp = User.objects.get(userid = Userid)
        IDCode = User_bp.idCode
        makeWeight(str(IDCode))
        User_bp.sub_name = subName
        User_bp.sub_num = subNum
        User_bp.save()
        return HttpResponse('1')
    except Exception as e:
        print(e)
        return HttpResponse('0')


@csrf_exempt
def loadSub(request):
    Userid = request.POST.get('userid')
    try:
        User_bp = User.objects.get(userid = Userid)
        return HttpResponse(str(User_bp.sub_num) + "\n" + User_bp.sub_name)
    except Exception as e:
        print(e)
        return HttpResponse('NONE')


@csrf_exempt
def saveTodo(request):
    Userid = request.POST.get('userid')
    todoNum = request.POST.get('todoNum')
    todoName = request.POST.get('todoName')
    try:
        User_bp = User.objects.get(userid = Userid)
        User_bp.todo_name = todoName
        User_bp.todo_num = todoNum
        User_bp.save()
        return HttpResponse('1')
    except Exception as e:
        print(e)
        return HttpResponse('0')


@csrf_exempt
def loadTodo(request):
    Userid = request.POST.get('userid')
    try:
        User_bp = User.objects.get(userid = Userid)
        return HttpResponse(str(User_bp.todo_num) + "\n" + User_bp.todo_name)
    except Exception as e:
        print(e)
        return HttpResponse('NONE')


@csrf_exempt
def userTime(request):
    Userid = request.POST.get('userid')
    try:
        User_bp = User.objects.get(userid = Userid)
        print(User_bp.name, User_bp.time_day, User_bp.time_sub)
        return HttpResponse(User_bp.name + "\n" + User_bp.time_day + "\n" + User_bp.time_sub)
    except Exception as e:
        print(e)
        return HttpResponse('0')


#인공지능 처리 함수
@csrf_exempt
def learn(request):
    Userid = request.POST.get('userid')
    Subject = request.POST.get('subject')
    StartHour = request.POST.get('startHour')
    StartMin = request.POST.get('startMin')
    EndHour = request.POST.get('endHour')
    EndMin = request.POST.get('endMin')
    Score = request.POST.get('score')

    print(Subject, StartHour, ':', StartMin, EndHour, ':', EndMin, Score)


@csrf_exempt
def goodMorning(request):
    Userid = request.POST.get('userid')
    NumSub = request.POST.get('numSub')
    nameSub = request.POST.get('nameSub')
    
    print(Userid, NumSub, nameSub)

    return HttpResponse('00:00-00:00')



