from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from blog.models import post
# Create your views here.

#html 
def home(request):
    return render(request, 'home/home.html')

def contact(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        print(name, email, phone, content)  
        
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact = Contact(name=name, phone=phone, email=email, content=content)
            contact.save()
            messages.success(request, "Your Message has been Sent Succesfully")
            
    return render(request, 'home/contact.html')

def search(request):
    query = request.GET['query']
    if len(query) > 78:
        allPosts = post.objects.none()
    else:
        allPostsTitle = post.objects.filter(title__icontains=query)
        allPostsContent = post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
        
    if allPosts.count() == 0:
         messages.error(request, "No search results found. Please refine your query")

    params = {'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)

def about(request): 
    messages.success(request, 'this is about')
    return render(request, 'home/about.html')    
    
# authentication APIs
def handleSignup(request):
    if request.method == 'POST':
        # Get the post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        # check for errorneous inputs
        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, "Username should only contain letters and Numbers")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('home')
        
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your CodeWall Account has been successfully Created")
        return redirect('/')
    else: 
        return HttpResponse('404 Not found')
    
    
def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpass']
        
        user = authenticate(username=loginusername, password=loginpassword)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully LoggedIN')
            return redirect('/')
        else:
            messages.error(request, "Invalid Credentials, Please Try again")
            return redirect('home')
        
        
    return HttpResponse('handleLOGIN')



def handleLogout(request):
        logout(request)
        messages.success(request, 'Successfully loggedOut')
        return redirect('/')
    
