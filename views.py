from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
import json


from .forms import UploadFileForm
import os
from os import path
#initialize the pirebase

import pyrebase

config = {
  "apiKey" : "AIzaSyCmmu5iJ8QcJrSpHC4QzgBscGCABKUJkro",
    "authDomain" : "blog-news-5ab92.firebaseapp.com",
    "databaseURL" : "https://blog-news-5ab92.firebaseio.com",
    "projectId" : "blog-news-5ab92",
    "storageBucket" : "blog-news-5ab92.appspot.com",
    "messagingSenderId" : "788704898160",
    "appId" : "1:788704898160:web:06d49f0169f46a0e3598b5",
    "measurementId" : "G-6M0KCMW8WJ"
}

firebase = pyrebase.initialize_app(config)


db = firebase.database()



#def imagehandle(f  , name) :
 #   with open('static/video'+name+'png', 'wb+') as destination:
  #      for chunk in f.chunks():
   #         destination.write(chunk)


# Create your views here.
storage = firebase.storage()


def aboutus( request ) : 
    desc = wordart( db.child("aboutus").get().val() )
    if not  desc :
        desc = "" 

    try : 
        sd = request.session['username'] 
    except : 
        request.session['username'] = None 
        
    return render(request, 'aboutus.html' , {'username' :  request.session['username']  , 'desc' :desc  , 'icon' : storage.child("icon.jpg").get_url(None ) , 'background' : storage.child("background.jpg").get_url(None )} )

def addaboutus(request) :
    desc = request.POST.get('aboutus') 
    print("ok")
    print(desc)
    
    db.child("aboutus").set(desc) 
    return redirect('/control')


def wordart( strings ) : 
    stringy = []

    addr = ""  

    for  i in strings : 
        if i == '\n' :
            stringy.append(addr) 
            addr ="" 

        else : 
            addr = addr + i 
    
    return stringy

def getcount() :
    with open('count.json', 'r') as outfile:
            data = json.load(outfile)
    s = data['count']
    s = str( int(s) +1 )
    data['count'] = str(s)
    with open('count.json', 'w') as outfile:
            json.dump(data, outfile)

    return data['count']

def imagehandle(f  , name) :
    with open('static/image/'+"name"+'.png', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    storage.child("images/"+name+".png" ).put('static/image/'+"name"+'.png')



def videohandle(f  , name) :
    with open('static/video/'+name+'.mp4', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def search(request) :
    tx =str(  request.GET.get('search') )
    if tx =='' :
        return redirect('/campgrounds-index')



    sd = db.child('tags').get().val()
    vallied = []
    
    if sd != None  : 
        for tag in sd :
            x = len(tx)
            pos = 1
            if x > len(tag)  :
                continue

            for i in range(0 , x ) :
                if tag[i] != tx[i] :
                    pos = 0
                    break
            if pos ==1 :
                vallied.append(tag)





    ret = []

    for tag  in  vallied :
        vs = db.child("tags").child(tag).get().val()
        for count in vs :
            
            try : 
                makeit = {} 
                i = count 

                makeit["id"]  = i 
                makeit["title"] = db.child("detail").child(i).child("title").get().val() 
                makeit["desc"] = db.child("detail").child(i).child("desc").get().val() 
                print("ok")

                makeit["imgurl"] = storage.child("images/"+i+".png" ).get_url(None)
        
                ret.append(makeit) 
            except : 
        
        

                print("error")

                continue 





    viewadd = 0
    user = request.session['username']
    vs = db.child('permission').child('post').child(user).get().val()
    if vs != None :
        viewadd = 1



    return render(request , 'campgrounds/index.html' , {'campgrounds' : ret , 'doi' : viewadd , 'username' :  request.session['username'] , 'icon' : storage.child("icon.jpg").get_url(None ) , 'background' : storage.child("background.jpg").get_url(None )     } )









def submit(request) :




    image = request.FILES['image']
  #  video = request.FILES['video']
    desc = request.POST.get('description')
    tag = request.POST.get('tag')
    title = request.POST.get('title')
    count = getcount()
    author = request.POST.get('author')
    imagehandle( image ,  count )
 #   videohandle( video ,  count )






    sd = {

            'id' : count ,
            'title' : title ,
            'desc' : desc ,
            'author' :  author 


    }

    tagss = []
    cur = ""

    for i in tag :
        if i == " " :
            tagss.append(cur)
            cur =""
        else :
            cur = cur+ i

    if cur != "" :
        tagss.append(cur)

    for tag in tagss :
        db.child('tags').child(tag).child(count).set(count)
        db.child('desctag').child(count).child(tag).set(tag)








    try :

        db.child("name").child(count).set(count) 
        db.child("detail").child(count).set(sd)
        
        
        
    except : 
        print("/error")





    return redirect('/')
def add(request) :
    return  render(request , 'campgrounds/new.html' , { 'username' :  request.session['username'] , 'icon' : storage.child("icon.jpg").get_url(None ) , 'background' : storage.child("background.jpg").get_url(None )})

def descadd(request) :
    data = request.POST.get('desc')





    with open('static/desc.json', 'w') as outfile:
            des = { "des" :  data }
            json.dump(des , outfile)
    return redirect('/control')

def imgchange(request) :

    f = request.FILES['img']
    with open('static/backgroundimage.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    
    storage.child("background.jpg" ).put('static/backgroundimage.jpg')

    return redirect('/control')

def  iconchange(request) :

    f = request.FILES['img']
    with open('static/icon.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    
    storage.child("icon.jpg" ).put('static/icon.jpg')





    return redirect('/control')

def home(request):

    with open('static/desc.json', 'r') as outfile:
            des = json.load(outfile)
    desc = des['des']

    try :
        sas = request.session['username']
    except :
        request.session['username'] = None
    
    desc = wordart(desc) 


    return render(request, 'landing.html' , {'username' :  request.session['username']  , 'desc' :desc  , 'icon' : storage.child("icon.jpg").get_url(None ) , 'background' : storage.child("background.jpg").get_url(None )} )


def campgroundsindex(request) :





    ret = []


    list_ids = db.child("name").get().val()  # get the list of count 
    print(list_ids)
    try : 
        for i in list_ids : 
            if i == None :
                continue 

            makeit = {} 

            makeit["id"]  = i 
            makeit["title"] = db.child("detail").child(i).child("title").get().val() 

            print("p")

            makeit["imgurl"] = storage.child("images/"+i+".png" ).get_url(None)

            ret.append(makeit)

    except : 
        print("error occured")
    
    print(ret) 
    ret.reverse()
    print(ret)
    
        
    
    
    viewadd = 0
    try  : 
        user = request.session['username']
    except  : 
        user = None 
        request.session['username'] = None 

        
    vs = db.child('permission').child('post').child(user).get().val()
    if vs != None :
        viewadd = 1

    return render(request , 'campgrounds/index.html' , {'campgrounds' : ret , 'doi' : viewadd , 'username' :  request.session['username'] , 'icon' : storage.child("icon.jpg").get_url(None ) , 'background' : storage.child("background.jpg").get_url(None ) } )


def campgroundopen(request):
    global storage 

    if request.method == 'GET' :
        i =  request.GET.get('ids')
        makeit = {} 

        makeit["id"]  = i 
        makeit["title"] = db.child("detail").child(i).child("title").get().val() 
        makeit["desc"] = db.child("detail").child(i).child("desc").get().val() 
        makeit["imgurl"] = storage.child("images/"+i+".png" ).get_url(None )

        makeit["author"] = db.child("detail").child(i).child("author").get().val()

        
        makeit["desc"] = wordart(makeit["desc"])

    

        print(makeit) 

        
        count = i 

        # now make it ready
        commen = {}
        try :


            commen = db.child("comment").child(count).child("comments").get().val()


        except :
            commen = {}



        recomended =  []
        pcd = []

        tag = db.child('desctag').child(count).get().val()
        print(tag)

        if tag != None :
            for tagss in tag :
                if tagss == None  :
                    continue  

                print(tagss)

                x = db.child('tags').child(tagss).get().val()

                print(x)
                if x != None  :


                    for i in x  :
                        


                        if i == None :

                            continue

                        if i == count :
                            continue
                        
                        pcd.append(i )
        pcd = set(pcd)

        print( pcd )


        for i in pcd :
            if i == None :
                continue  


            try : 
                makeit2 = {} 

                makeit2["id"]  = i 
                makeit2["title"] = db.child("detail").child(i).child("title").get().val() 

                makeit2["imgurl"] = storage.child("images/"+i+".png" ).get_url(None )

        
                recomended.append(makeit2) 
            except : 
                continue 

            #if not (path.exists('static/description/'+i+'.json')  ) :
            #    continue
            #with open('static/description/'+i+'.json', 'r') as outfile :
            #    ass = json.load(outfile)
            #ass['image'] = 'image/'+i +'.png'




        db.child('history').child(request.session['username']).push( { count : count })
        sd = 0
        try :
            sd = int(db.child('views').child(request.get('ids')).get().val() )
        except  :
            sd = 0
        sd += 1
        db.child('views').child(request.GET.get('ids')).set(str(sd))



        return  render(request , 'campgrounds/show.html' , { 'campground' : makeit , 'comments' :  commen , 'recom' :  recomended , 'username' :  request.session['username']  , 'icon' : storage.child("icon.jpg").get_url(None ) , 'background' : storage.child("background.jpg").get_url(None )}   )





    try :
        a =  request.session['username']
    except :
        request.session['username'] = None

    return  render(request , 'campgrounds/show.html' , {'username' :  request.session['username'] }   )




def campgroundaddcom(request) :
    if request.method == 'GET'  :

        blogname = request.GET.get('blogidnh')
        desc = request.GET.get('addcomment')
        username = request.session['username']
        if username == None :
            return  redirect('/login')



        # first get the next count for fixing the comment id
        vas = 0
        try :

             vas =   int(db.child("comment").child(blogname).child("count").get().val() )
        except  :
            vas = 0

        db.child("comment").child(blogname).child("count").set(str(vas+1))
        db.child("comment").child(blogname).child("comments").child(str(vas)).child("user").set(username)
        db.child("comment").child(blogname).child("comments").child(str(vas)).child("desc").set(desc)

    return redirect('/campgrounds-index')


def login(request):




    if request.method == 'POST':

        email = str(request.POST.get("email") )
        password = str(  request.POST.get("password") )


        before = ""

        for i in email :
            if i == '.' :
                before = before + ','
            else :
                before = before + i

        isd = db.child('users').child(before).child('password').get().val()
        print(isd)

        if isd ==  password :
            request.session['username'] = before
            return redirect( '/campgrounds-index')
        return redirect('/login')

    return render(request, 'login.html' , { 'username' :  request.session['username'] , 'icon' : storage.child("icon.jpg").get_url(None ) , 'background' : storage.child("background.jpg").get_url(None )})


def register(request):

    name = ""
    password = ""
    email = ""



    if request.method == 'POST':

        # check if email is already registered
        #
        #  seperate email in two terms


        name = request.POST.get("name")
        password = request.POST.get("password")
        email = request.POST.get("email")


        before = ""

        for i in email :
            if i == '.' :
                before = before + ','
            else :
                before = before + i


        error1 = db.child('users').child(before).get().val()
        if error1 != None :
            return redirect('/login')

        #verified



        db.child('users').child(before).set({

            "email" : email ,
            "user" : before ,
            "name" : name ,
            "password" :  password ,

        })






        return redirect('/login')

    return render(request ,  'register.html' , { 'username' :  request.session['username'] , 'icon' : storage.child("icon.jpg").get_url(None ) , 'background' : storage.child("background.jpg").get_url(None )})




def control(request) :
    # one for adding post
    #get the count




    allo = db.child('permission').child('post').get().val()
    allowance = []
    if allo == None :
        return render(request , 'control.html' , { 'allowance' : [], 'icon' : storage.child("icon.jpg").get_url(None ) , 'background' : storage.child("background.jpg").get_url(None ) }  )


    for email in allo :
        before = ""
        for i in email :
            if i == ',' :
                before = before + '.'
            else :
                before = before + i
        allowance.append(before)



    #one for deleting comment , done later on
    return render(request , 'control.html' , { 'allowance' : allowance , 'username' :  request.session['username'] , 'icon' : storage.child("icon.jpg").get_url(None ) , 'background' : storage.child("background.jpg").get_url(None )  }  )




def comallo(request) :
    email = request.POST.get('email')


    unt = 0
    if email == None  :
        return redirect('/control')

    before = ""
    for i in email :
        if i == '.' :
            before = before + ','
        else :
            before = before + i

    id = before

    db.child('permission').child('post').child(id).set(email)



    return redirect('/control')



def  comrem(request) :

    email = request.POST.get('userid')
    before = ""
    for i in email :
        if i == '.' :
            before = before + ','
        else :
            before = before + i

    id = before


    db.child('permission').child('post').child(id).remove()
    return redirect( '/control')



def userdetails(request) :

    if request.session['username'] == None :
        return  redirect('/campgrounds-index')
    recomended =  []
    x = [] 
    
    # deleated history

    #x = db.child('history').child(str(request.session['username'])).get().val()

    if x == None :
        return render(request , 'user.html' , { 'history' :  recomended , 'username' :  request.session['username']   } )
    
    for isd in  x  :
        for  i in  db.child('history').child(str(request.session['username'])).child(isd).get().val() :

            try : 
                makeit = {} 

                makeit["id"]  = i 
                makeit["title"] = db.child("detail").child(i).child("title").get().val() 
                makeit["desc"] = db.child("detail").child(i).child("desc").get().val() 
                makeit["imgurl"] = storage.child("images/"+i+".png" ).get_url(None )  
        
                recomended.append(makeit) 
            except : 
                continue 


#            print(i)
 #           if not(path.exists('static/description/' + i + '.json')) :
  #              continue

   #         with open ('static/description/' + i + '.json', 'r') as outfile:
    #            ass = json.load(outfile)


     #       ass['id'] = i
      #      del ass['desc']

       #     ass['image'] = 'image/'+i +'.png'



        #    recomended.append(ass)



    return render(request , 'user.html' , { 'history' :  recomended , 'username' :  request.session['username']  , 'icon' : storage.child("icon.jpg").get_url(None )} )


def logouts(request) :
    request.session['username'] = None
    return redirect( '/login')


def changepass(request) :
    user = request.session['username']
    pass1 = request.POST.get('password1')
    pass2 = request.POST.get('password2')
    if pass1 == pass2 :

        db.child('users').child(user).child("password").set(  pass2    )

    return redirect('/userdetails')


def deletepost(request ) :
    id = request.POST.get("ids")

    # delete the video
    #if path.exists("static/video/" + id + ".mp4") :
    #    os.remove("static/video/" + id + ".mp4")
    # delete the description
    #if path.exists("static/description/" + id + ".json") :
    #    os.remove("static/description/" + id + ".json")


    # delete the png


    #if path.exists("static/image/" + id + ".png") :
    #    os.remove("static/image/" + id + ".png")

    # remove comments

    
    db.child("comment").child(id).remove()
    tags = db.child("desctag").child(id).get().val()
    db.child("desctag").child(id).remove()

    if tags != None :
        for tag in tags :
            db.child("tags").child(tag).child(id).remove()


    i = id  

    print(i)

    try : 
        
        db.child("name").child(i).remove()
        
        db.child("detail").child(i).remove() 

    except : 
        print( " no such directory")
        
           

    return redirect('/')



def controllog(request ) :
    if request.session['username'] == "jayantanand00@gmail,com" :
        return control(request)

    return redirect('/login')
