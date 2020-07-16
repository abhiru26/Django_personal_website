from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from blog.models import Post
from django.contrib.auth.models import User

# Create your views here.

def home(request):
    return render(request, 'home/home.html')
 
def about(request):
    return render(request, 'home/about.html')
    
def contact(request):
    
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        print(name,email,phone,content)

        if len(name) < 2 or len(email) < 3 or len(phone) < 10 or len(content) < 4:
        
            messages.warning(request, 'sorry wrong inputs')
        
        else:

            contact = Contact(name=name,email = email, phone = phone, content = content)
            contact.save()
            messages.success(request, 'your form has been sent')
    return render(request, 'home/contact.html')

def search(request):
    query = request.GET['query']
    if len(query) > 78 :
        allPosts = Post.objects.none()
    else:
         allPostsTitle = Post.objects.filter(title__icontains = query)
         allPostsContent = Post.objects.filter(content__icontains = query)
         allPosts = allPostsTitle.union(allPostsContent)
    if allPosts.count() == 0:
         messages.warning(request, 'no similar documents are found ')
    params = {"allPosts": allPosts, 'query': query}
    return render(request, 'home/search.html', params)
#authenticate apis

def handleSignup(request):
    if request.method == 'POST':
        #Get the post parameter
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # check
        if len(username) > 10:
            messages.warning(request, "username must be less than 10 characters")
            return redirect('home')

        if not username.isalnum():
            messages.warning(request, "username cannot contain special characters")
            return redirect('home')
        if pass1 != pass2:
            messages.warning(request, "password do not matches")
            return redirect('home')
        



        #

        #create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your account has been successfully created")
        return redirect('home')
        

                
    else:
        return HttpResponse('404 - not allowed')
def handleLogin(request):

    if request.method == 'POST':

        #Get the post parameter
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']

        user = authenticate(username = loginusername, password = loginpass)

        if user is not None:
            login(request, user)
            messages.success(request, 'succesfully logged in')
            return redirect('home')
        else:
            messages.warning(request, 'invalid credentials')
            return redirect('home')
    return HttpResponse('handleLogin')



def handleLogout(request):
    logout(request)
    messages.success(request, 'succesfully logged out')
    return redirect('home')
    
    return HttpResponse('handleLogout')


    
   
    
  

