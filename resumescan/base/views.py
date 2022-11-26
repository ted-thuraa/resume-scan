from django.shortcuts import render
from pyresparser import ResumeParser
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import Cvuploads, User
from .forms import CvUploadsform
from .utils import handle_uploaded_file, pdf_reader, getkeyWords, keywordsSE



# Create your views here.

def loginpage(request):
    page = 'login'
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Wrong username or password')
        
    context = {'page': page}
    return render(request, "base/login_register.html", context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page = 'register'

    form = UserCreationForm
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Error: Not registered')

    context = {'page':page, 'form':form}
    return render(request, "base/login_register.html", context)


def home(request):
    context = {}
    return render(request, 'index.html', context) 


def scan(request):
    document = CvUploadsform()

    if request.method == 'POST':
        document = CvUploadsform(request.POST, request.FILES)
        if document.is_valid():
            #job_description = request.POST.get('job_description')
            handle_uploaded_file(request.FILES['file'])
           #Cvuploads.objects.create(
           #    user = request.user,
           #    file = request.FILES['file']
           #)
            model_instance = document.save(commit=False)
            #pkid = model_instance.file.id
            model_instance.user = request.user
            model_instance.job_description = request.POST.get('job_description')
            model_instance.save()
            pkid = Cvuploads.objects.get(id=model_instance.id)
            return redirect('analyseResume', pk=pkid.id)
        else:
            messages.error(request, 'Error: Upload failed')

    context = {'document': document}
    return render(request, 'base/uploadform.html', context)

def analyseResume(request, pk):
    resume_Doc = Cvuploads.objects.get(id=pk)
    
    pdf_path = resume_Doc.file.path
    if resume_Doc:
        resume_Data = ResumeParser(pdf_path).get_extracted_data()
        if resume_Data:
            resume_Text = pdf_reader(pdf_path)

            try:
                yourName = resume_Data['name']
                yourEmail = resume_Data['email']
                yourContact = resume_Data['mobile_number']
                yourSkills = resume_Data['skills']
            except:
                pass
            se_keyword = ['javascript','communication skills', 'rest', 'apis', 'git', 'aws', 'python', 'sql', 'css', 'software development', 'php', 'html5', 'devops', 'docker', 'linux', 'problem solving', 'quality assuarance']
            recommended_skills = []
            resume_Data_lower = []

            # job description keyword checking
            job_description = resume_Doc.job_description
            jobkeywords = getkeyWords(job_description, keywordsSE)

            #job_decription_handler(job_description)
            for i in resume_Data['skills']:
                list_item = i.lower()
                resume_Data_lower.append(list_item)

            for i in jobkeywords:
                #software engineer recomendation
                if i not in resume_Data_lower:
                    recommended_skills.append(i)
            skillstoadd = recommended_skills
            resume_Data_lower = []
            recommended_skills = []
            context = {'yourName':yourName, 'yourEmail':yourEmail, 'yourSkills':yourSkills, 'skillstoadd':skillstoadd }
            return render(request, 'base/cvDetails.html', context)

        else:
            messages.error(request, 'Error: resume parsing failed')

    else:
        messages.error(request, 'Error: Not in database or id not working')
