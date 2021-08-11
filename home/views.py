from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from blog.models import Post


# Create your views here.

def home(request):
    return render(request,"home/home.html")

def contact(request):
   
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']

        if len(name)<2 or len(email)<3 or len(phone)<10 or len(message)<4:
             messages.error(request, 'Please fill the form correctly')
        
        else:
            
            contact = Contact(name=name, email=email, phone=phone, message=message)
            contact.save()
            messages.success(request, 'Your form successfully send!')              
      
    return render(request,"home/contact.html")


def about(request):
    return render(request,"home/about.html")


def search(request):
    query = request.GET['search']
    if len(query)>30:
        allPost = Post.objects.none()
    else:    
        allPostTitle = Post.objects.filter(title__icontains=query)
        allPostContent = Post.objects.filter(content__icontains=query)
        allPost = allPostTitle.union(allPostContent)
    
    if allPost.count()==0:
        messages.error(request, 'No serach result found. Please refine your query')
    params = {'allPost': allPost, 'query': query}

    return render(request,"home/search.html", params)

def handelSignup(request):
    if request.method =="POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm']

        if len(username)<10:
             messages.error(request, "Your Username must be 10 characters")
             return redirect("/")

        if not username.isalnum():
             messages.error(request, "Your Username shoud only contain letters and numbers")
             return redirect("/")
        
        if password != confirm:
            messages.error(request, "Password do not match")
            return redirect("/")          
             
        #Create User
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your account has been successfully created")
        return redirect("/")
    else:
        return HttpResponse("Error 404 Not Found")
    
def handelLogin(request):
     if request.method =="POST":
        loginusername = request.POST['loginusername']        
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, f"Successfully logged In {user.username} ")
            return redirect('/')
        
        else:
            messages.error(request, "Invalid account , please try again")
            return redirect('/')
     return HttpResponse("Error 404 Not Found")      
        

def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logout")
    return redirect('/')
    
       




    
    
    