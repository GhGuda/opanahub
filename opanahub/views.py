from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import *
from django.contrib.auth.decorators import login_required
import random
from django.db.models import Q

# for password reset form customization

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from bs4 import BeautifulSoup


# time re tiue irutu poeirt iwr tiopwitw
from datetime import timezone, timedelta
from django.utils.timesince import timesince

# Create your views here.


def index(request):
    if User.is_authenticated:
        return redirect(frontpage)
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            auth_user = auth.authenticate(username=username, password=password)

            if auth_user is not None:
                auth.login(request, auth_user)
                return redirect('frontpage')
            
            else:
                messages.error(request, "No identity matched, retry")
                return redirect('index')
        else:
            return render(request, "index.html")



def logout(request):
    auth.logout(request)
    return redirect('index')


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if len(username) <= 0:
                messages.error(request, "Enter username!")
                return redirect('register')
            if password == username:
                messages.error(request, "Password similar to username!")
                return redirect('register')
            elif len(email) <= 0:
                messages.error(request, "Enter email!")
                return redirect('register')
            elif len(password) < 8:
                messages.error(request, "Password is weak, enter strong password!")
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.error(request, "Username taken!")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email taken!")
                return redirect('register')
            else:
                new_user = User.objects.create_user(username=username, email=email, password=password)
                new_user.save()

                auth_new_user = auth.authenticate(username=username, password=password)
                auth.login(request,auth_new_user)

                user_obi = User.objects.get(username=username)

                new_profile = Profile.objects.create(user=user_obi)
                new_profile.save()
                return redirect('setting')
            


        else:
            messages.error(request, "Passwords do not match!")
            return redirect('register')
    else:
        return render(request, "register.html")



def password_reset_request(request):
    if request.method == "POST":
        password_form = PasswordResetForm(request.POST)
        if password_form.is_valid():
            data = password_form.cleaned_data['email']
            user_email = User.objects.filter(Q(email=data))
            if user_email.exists():
                for user in user_email:
                    subject = 'Password Reset'
                    email_template_name = "passwordtext.html"
                    parameters={
                        'email': user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'OpanaHub',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol':'http://'
                    }
                    email = render_to_string(email_template_name, parameters)
                    soup = BeautifulSoup(email, 'html.parser')
                    plain_text_message = soup.get_text()
                    try:
                        send_mail(subject, plain_text_message, '', [user.email], fail_silently=True)
                    except:
                        return HttpResponse('Invalid Header')
                    return redirect('password_reset_done')
    else:
        password_form = PasswordResetForm()
    
    
    context={
        'password_form' : password_form
    }
    
    
    return render(request, "reset.html", context)
    



@login_required(login_url=index)
def frontpage(request):
    user_obj = User.objects.get(username=request.user)
    get_profile = Profile.objects.get(user=user_obj)
    logged_in_user = request.user

    # if request.method == "POST":
    #     query = request.get("query")
    #     if query:
    #         pass

    posts = Posts.objects.all()
    
    for post in posts:
        comments = Comment.objects.filter(post=post).order_by('created_on')[:2]
        post.comments = comments


    context = {
        "profile": get_profile,
        "post": posts,
    }

    return render(request, "frontpage.html", context)



@login_required(login_url=index)
def edit(request, pana):
    post = Posts.objects.get(post_id=pana)
    get_profile = Profile.objects.get(user__username=request.user)
    
    if request.method == "POST":
        
        if request.FILES.get("upload") == None:
            user = get_profile
            caption = request.POST['caption']
            tag = request.POST['tag']
            new_trends = Trend.objects.create(tag=tag)
            upload = post.image
            
            post.caption=caption
            post.trends=new_trends
            post.image=upload
            post.profile=user
            post.edited = True
            post.save()
            return redirect('frontpage')
        
        
        if request.FILES.get("upload") != None:
            user = get_profile
            caption = request.POST['caption']
            tag = request.POST['tag']
            new_trends = Trend.objects.create(tag=tag)
            upload = request.FILES.get("upload")
            
            post.caption=caption
            post.trends=new_trends
            post.image=upload
            post.profile=user
            post.edited = True
            post.save()
            return redirect('frontpage')
        
    context ={
        "profile": get_profile,
        'post':post
        # "suggested_profile": suggested_profile,
    }
    return render(request, "edit.html", context)




@login_required(login_url=index)
def delpost(request, pana):
    post = Posts.objects.get(post_id=pana)
    post.delete()
    return redirect(frontpage)



def search(request):
    pass


def delthiss(request, pana, user):
    post = Posts.objects.get(post_id=pana)
    post.delete()
    return redirect(profile, user)



def onlyFollowing(request):
    user_obj = User.objects.get(username=request.user)
    get_profile = Profile.objects.get(user=user_obj)


    profile_followers = Follow.objects.filter(user=get_profile)
    posts = Posts.objects.filter()







@login_required(login_url=index)
def profile(request, user):
    user_obj = User.objects.get(username=user)
    profile =  Profile.objects.get(user=user_obj)
    postt = Posts.objects.filter(profile=profile)
    user_obj = Profile.objects.get(user=request.user)
    logged_in_user = request.user

    follower = user_obj
    following = profile

    if Follow.objects.filter(user=follower, following=following):
        switch = "Following"
    else:
        switch = "Follow"

    profile_visited_followers = len(Follow.objects.filter(user=profile))
    profile_visited_following = len(Follow.objects.filter(following=profile))

    total_likes = 0  

    for post in postt:
        total_likes += post.likes

    context ={
        "profile": profile,
        "user_obj": user_obj,
        "post": postt,
        "switch": switch,
        "profile_visited_followers": profile_visited_followers,
        "profile_visited_following": profile_visited_following,
        # "suggested_profile": suggested_profile,
        # "post_comments": post_comments,
        "likes": total_likes,
    }

    return render(request, "profile.html", context)


@login_required(login_url=index)
def follow(request):

    if request.method == "POST":
        current_user = request.POST['follower']
        followed_user = request.POST['following']
        follower = User.objects.get(username=current_user)
        following = User.objects.get(username=followed_user)

        user_obj = Profile.objects.get(user=follower)

        u = Profile.objects.get(user=following)


        if Follow.objects.filter(user=user_obj, following=u).first():
            del_follower = Follow.objects.get(user=user_obj, following=u)
            del_follower.delete()
            return redirect(profile, followed_user)
        else:
            new_follower = Follow.objects.create(user=user_obj, following=u)
            new_follower.save()
            return redirect(profile, followed_user)



@login_required(login_url=index)
def addup(request):
    if request.method == "POST":
        userprofile = request.POST['userprofile']
        current_user = request.POST['follower']
        followed_user = request.POST['following']
        follower = User.objects.get(username=current_user)
        following = User.objects.get(username=followed_user)

        user_obj = Profile.objects.get(user=follower)

        u = Profile.objects.get(user=following)


        if Follow.objects.filter(user=user_obj, following=u).first():
            del_follower = Follow.objects.get(user=user_obj, following=u)
            del_follower.delete()
            return redirect("follower", userprofile)
        else:
            new_follower = Follow.objects.create(user=user_obj, following=u)
            new_follower.save()
            return redirect("follower", userprofile)

        
        

@login_required(login_url=index)
def follower(request, user):
    user_obj = User.objects.get(username=user)
    profile =  Profile.objects.get(user=user_obj)
    post = Posts.objects.filter(profile=profile)
    user_ob = Profile.objects.get(user=request.user)
    logged_in_user = request.user

    follower = user_ob
    following = profile

    if Follow.objects.filter(user=follower, following=following):
        switches = "Following"
    else:
        switches = "Follow"

    # profile_visited_followers = len(Follow.objects.filter(user=profile))
    profile_following = Follow.objects.filter(following=profile)
    profile_visited_following = len(Follow.objects.filter(following=profile))


    # if logged_in_user.is_authenticated and logged_in_user.profile == profile:
    #     prof_sug = list(Profile.objects.exclude(user=user_pro))
    # else:
    #     prof_sug = list(Profile.objects.exclude(user=user_obj.user))

    # random.shuffle(prof_sug)

    # suggested_profile = prof_sug[:4]




    context ={
        "profile": profile,
        "post": post,
        "switches": switches,
        "profile_following": profile_following,
        # "profile_visited_followers": profile_visited_followers,
        "profile_visited_following": profile_visited_following,
        # "suggested_profile": suggested_profile,
        
    }

    return render(request, 'followers.html', context)



@login_required(login_url=index)
def following(request, user):
    user_obj = User.objects.get(username=user)
    profile =  Profile.objects.get(user=user_obj)
    post = Posts.objects.filter(profile=profile)
    user_obj = Profile.objects.get(user=request.user)

    follower = user_obj
    following = profile

    if Follow.objects.filter(user=follower, following=following):
        switch = "Following"
    else:
        switch = "Follow"

    # profile_visited_followers = len(Follow.objects.filter(user=profile))
    profile_followers = Follow.objects.filter(user=profile)
    # profile_visited_following = len(Follow.objects.filter(following=profile))


    context ={
        "profile": profile,
        "post": post,
        "switch": switch,
        "profile_following": profile_followers,
        # "profile_visited_followers": profile_visited_followers,
        # "profile_visited_following": profile_visited_followers,
        
    }

    return render(request, 'following.html', context)













@login_required(login_url=index)
def savethis(request):
    user_obj = User.objects.get(username=request.user)
    get_profile = Profile.objects.get(user=user_obj)
    post_id = request.GET.get("like_id")

    posts = Posts.objects.get(post_id=post_id)

    post_save = Save.objects.filter(post=posts, user=get_profile).first()
    

    if post_save == None:
        new_save = Save.objects.create(post=posts, user=get_profile)
        new_save.save()
        posts.saved +=1
        posts.sav = True
        posts.save()
        return redirect('frontpage')
    
    else:
        post_save.delete()
        posts.saved -=1
        posts.sav = False
        posts.save()
        return redirect('frontpage')


@login_required(login_url=index)
def savethiss(request):
    user_obj = User.objects.get(username=request.user)
    get_profile = Profile.objects.get(user=user_obj)
    post_id = request.GET.get("post_id")

    posts = Posts.objects.get(post_id=post_id)

    post_save = Save.objects.filter(post=posts, user=get_profile).first()
    

    if post_save == None:
        new_save = Save.objects.create(post=posts, user=get_profile)
        new_save.save()
        posts.saved +=1
        posts.sav = True
        posts.save()
        return redirect(pana_details, post_id)
    
    else:
        post_save.delete()
        posts.saved -=1
        posts.sav = False
        posts.save()
        return redirect(pana_details, post_id)



@login_required(login_url=index)
def savethissinprofile(request, user):
    user_obj = User.objects.get(username=request.user)
    get_profile = Profile.objects.get(user=user_obj)
    post_id = request.GET.get("post_id")

    u = User.objects.get(username=user)
    visit_profile = Profile.objects.get(user=u)

    posts = Posts.objects.get(post_id=post_id)

    post_save = Save.objects.filter(post=posts, user=get_profile).first()

    if post_save == None:
        new_save = Save.objects.create(post=posts, user=get_profile)
        new_save.save()
        posts.saved +=1
        posts.sav = True
        posts.save()
        return redirect(profile, visit_profile)
    
    else:
        post_save.delete()
        posts.saved -=1
        posts.sav = False
        posts.save()
        return redirect(profile, visit_profile)
    

@login_required(login_url=index)
def savedthissinyo(request, user):
    user_obj = User.objects.get(username=request.user)
    get_profile = Profile.objects.get(user=user_obj)
    post_id = request.GET.get("post_id")

    u = User.objects.get(username=user)
    visit_profile = Profile.objects.get(user=u)

    posts = Posts.objects.get(post_id=post_id)

    post_save = Save.objects.filter(post=posts, user=get_profile).first()

    if post_save == None:
        new_save = Save.objects.create(post=posts, user=get_profile)
        new_save.save()
        posts.saved +=1
        posts.sav = True
        posts.save()
        return redirect(userliked, visit_profile)
    
    else:
        post_save.delete()
        posts.saved -=1
        posts.sav = False
        posts.save()
        return redirect(userliked, visit_profile)
    
    
@login_required(login_url=index)
def savedthissinyou(request, user):
    user_obj = User.objects.get(username=request.user)
    get_profile = Profile.objects.get(user=user_obj)
    post_id = request.GET.get("post_id")

    u = User.objects.get(username=user)
    visit_profile = Profile.objects.get(user=u)

    posts = Posts.objects.get(post_id=post_id)

    post_save = Save.objects.filter(post=posts, user=get_profile).first()

    if post_save == None:
        new_save = Save.objects.create(post=posts, user=get_profile)
        new_save.save()
        posts.saved +=1
        posts.sav = True
        posts.save()
        return redirect(savedpost, visit_profile)
    
    else:
        post_save.delete()
        posts.saved -=1
        posts.sav = False
        posts.save()
        return redirect(savedpost, visit_profile)


@login_required(login_url=index)
def savedpost(request, user):
    user_obj = User.objects.get(username=user)
    profile =  Profile.objects.get(user=user_obj)
    post = Posts.objects.filter(profile=profile)
    user_obj = Profile.objects.get(user=request.user)
    saved = Save.objects.filter(user=profile).order_by("-post__likes")
    logged_in_user = request.user

    follower = user_obj
    following = profile

    if Follow.objects.filter(user=follower, following=following):
        switch = "Following"
    else:
        switch = "Follow"

    profile_visited_followers = len(Follow.objects.filter(user=profile))
    profile_visited_following = len(Follow.objects.filter(following=profile))


    # if logged_in_user.is_authenticated and logged_in_user.profile == profile:
    #     prof_sug = list(Profile.objects.exclude(user=user_pro))
    # else:
    #     prof_sug = list(Profile.objects.exclude(user=user_obj.user))

    # random.shuffle(prof_sug)

    # suggested_profile = prof_sug[:4]


    context ={
        "profile": profile,
        "post": post,
        "switch": switch,
        "profile_visited_followers": profile_visited_followers,
        "profile_visited_following": profile_visited_following,
        # "post_comments": post_comments,
        "saved": saved,
        # "logged_in_user": logged_in_user,
    }

    return render(request, "saved.html", context)





@login_required(login_url=index)
def likethis(request):
    user_obj = User.objects.get(username=request.user)
    get_profile = Profile.objects.get(user=user_obj)
    post_id = request.GET.get("like_id")

    posts = Posts.objects.get(post_id=post_id)

    post_like = Like_post.objects.filter(post=posts, user=get_profile).first()
    

    if post_like == None:
        new_like = Like_post.objects.create(post=posts, user=get_profile)
        new_like.save()
        posts.likes +=1
        posts.liked = True
        posts.save()
        return redirect('frontpage')
    
    else:
        post_like.delete()
        posts.liked = False
        posts.likes -=1
        posts.save()
        return redirect('frontpage')


@login_required(login_url=index)
def likethiss(request):
    user_obj = User.objects.get(username=request.user)
    get_profile = Profile.objects.get(user=user_obj)
    post_id = request.GET.get("post_id")

    posts = Posts.objects.get(post_id=post_id)

    post_like = Like_post.objects.filter(post=posts, user=get_profile).first()

    if post_like == None:
        new_like = Like_post.objects.create(post=posts, user=get_profile)
        new_like.save()
        posts.likes +=1
        posts.liked = True
        posts.save()
        return redirect(pana_details, post_id)
    
    else:
        post_like.delete()
        posts.likes -=1
        posts.liked = False
        posts.save()
        return redirect(pana_details, post_id)
    
@login_required(login_url=index)
def likethissinprofile(request, user):
    user_obj = User.objects.get(username=request.user)
    get_profile = Profile.objects.get(user=user_obj)
    post_id = request.GET.get("post_id")

    u = User.objects.get(username=user)
    visit_profile = Profile.objects.get(user=u)

    posts = Posts.objects.get(post_id=post_id)

    post_like = Like_post.objects.filter(post=posts, user=get_profile).first()

    if post_like == None:
        new_like = Like_post.objects.create(post=posts, user=get_profile)
        new_like.save()
        posts.likes +=1
        posts.liked = True
        posts.save()
        return redirect(profile, visit_profile)
    
    else:
        post_like.delete()
        posts.likes -=1
        posts.liked = False
        posts.save()
        return redirect(profile, visit_profile)
    
@login_required(login_url=index)
def likethissinyo(request, user):
    user_obj = User.objects.get(username=request.user)
    get_profile = Profile.objects.get(user=user_obj)
    post_id = request.GET.get("post_id")

    u = User.objects.get(username=user)
    visit_profile = Profile.objects.get(user=u)

    posts = Posts.objects.get(post_id=post_id)

    post_like = Like_post.objects.filter(post=posts, user=get_profile).first()

    if post_like == None:
        new_like = Like_post.objects.create(post=posts, user=get_profile)
        new_like.save()
        posts.likes +=1
        posts.liked = True
        posts.save()
        return redirect(userliked, visit_profile)
    
    else:
        post_like.delete()
        posts.likes -=1
        posts.liked = False
        posts.save()
        return redirect(userliked, visit_profile)
    
    
@login_required(login_url=index)
def likethissinyou(request, user):
    user_obj = User.objects.get(username=request.user)
    get_profile = Profile.objects.get(user=user_obj)
    post_id = request.GET.get("post_id")

    u = User.objects.get(username=user)
    visit_profile = Profile.objects.get(user=u)

    posts = Posts.objects.get(post_id=post_id)

    post_like = Like_post.objects.filter(post=posts, user=get_profile).first()

    if post_like == None:
        new_like = Like_post.objects.create(post=posts, user=get_profile)
        new_like.save()
        posts.likes +=1
        posts.liked = True
        posts.save()
        return redirect(savedpost, visit_profile)
    
    else:
        post_like.delete()
        posts.likes -=1
        posts.liked = False
        posts.save()
        return redirect(savedpost, visit_profile)

@login_required(login_url=index)
def userliked(request, user):
    user_pro = User.objects.get(username=user)
    profile =  Profile.objects.get(user=user_pro)
    post = Posts.objects.filter(profile=profile)
    user_obj = Profile.objects.get(user=request.user)
    likes = Like_post.objects.filter(user=profile).order_by("-post__likes")
    logged_in_user = request.user

    follower = user_obj
    following = profile

    if Follow.objects.filter(user=follower, following=following):
        switch = "Following"
    else:
        switch = "Follow"

    profile_visited_followers = len(Follow.objects.filter(user=profile))
    profile_visited_following = len(Follow.objects.filter(following=profile))


    if logged_in_user.is_authenticated and logged_in_user.profile == profile:
        prof_sug = list(Profile.objects.exclude(user=user_pro))
    else:
        prof_sug = list(Profile.objects.exclude(user=user_obj.user))

    random.shuffle(prof_sug)

    suggested_profile = prof_sug[:4]

    context ={
        "profile": profile,
        "post": post,
        "switch": switch,
        "profile_visited_followers": profile_visited_followers,
        "profile_visited_following": profile_visited_following,
        # "post_comments": post_comments,
        "likes": likes,
        "suggested_profile": suggested_profile,
    }

    return render(request, "liked.html", context)









@login_required(login_url=index)
def pana(request):
    user_obj = User.objects.get(username=request.user)
    get_profile = Profile.objects.get(user=user_obj)
    logged_in_user = request.user

    if request.method == "POST":
        user = get_profile
        caption = request.POST['caption']
        tag = request.POST['tag']
        upload = request.FILES.get("upload")
        
        new_trends = Trend.objects.create(tag=tag)

        if tag == None:
            new_post = Posts.objects.create(profile=user, image=upload, caption=caption)
            new_post.save()
        else:
            new_post = Posts.objects.create(profile=user, trends=new_trends, image=upload, caption=caption)
            new_post.save()
        
        new_trends = Trend.objects.create(tag=tag)
        new_trends.save()
        return redirect('frontpage')
        
    context ={
        "profile": get_profile,
    }

    return render(request, "pana.html", context)



@login_required(login_url=index)
def pana_details(request, post_id):
    user_obj = User.objects.get(username=request.user)
    get_profile = Profile.objects.get(user=user_obj)
    post = Posts.objects.get(post_id=post_id)
    logged_in_user = request.user


    if request.method == "POST":
        body = request.POST['body']
        

        new_comment = Comment.objects.create(user=get_profile, post=post, body=body)
        post.comments +=1
        post.save()
        new_comment.save()
        

    comments = Comment.objects.filter(post=post)

    # if logged_in_user.is_authenticated and logged_in_user.profile == profile:
    #     prof_sug = list(Profile.objects.exclude(user=user_pro))
    # else:
    #     prof_sug = list(Profile.objects.exclude(user=user_obj.user))

    # random.shuffle(prof_sug)

    # suggested_profile = prof_sug[:4]


    context={
        'posts':post, 
        "profile":get_profile,
        'comment': comments,
        # 'suggested_profile': suggested_profiles,
    }

    return render(request, "details.html", context)

@login_required(login_url=index)
def comment_del(request, post_id, comment_id):
    comment = Comment.objects.get(comment_id=comment_id)
    posts = Posts.objects.get(post_id=post_id)
    comment.delete()
    posts.comments -=1
    posts.save()
    return redirect("pana_details", post_id)

@login_required(login_url=index)
def likecomment(request, post_id):
    user_obj = User.objects.get(username=request.user)
    get_profile = Profile.objects.get(user=user_obj)
    # posts = Posts.objects.get(post_id=post_id)

    comment_id = request.GET.get("comment_id")

    comment = Comment.objects.get(comment_id=comment_id)

    check_like = Like_comment.objects.filter(user=get_profile, comment_id=comment_id).first()

    if check_like == None:
        new_like = Like_comment.objects.create(user=get_profile, comment_id=comment_id)
        comment.likes += 1
        comment.liked = True
        comment.save()
        
        new_like.save()
    else:
        check_like.delete()
        comment.likes -= 1
        comment.liked = False
        comment.save()

    
    
    return redirect("pana_details", post_id)


@login_required(login_url=index)
def setting(request):
    user_obj = User.objects.get(username=request.user)
    profile =  Profile.objects.get(user=user_obj)

    if request.method == 'POST':
        if request.FILES.get('backimg') == None:
            back_img = profile.back_img
            name = request.POST['display_name']
            bio = request.POST['bio']
            web = request.POST['web']
            
            profile.back_img=back_img
            profile.display_name=name
            profile.bio=bio
            profile.web=web
            

        if request.FILES.get('backimg') != None:
            back_img = request.FILES.get('backimg')
            name = request.POST['display_name']
            bio = request.POST['bio']
            web = request.POST['web']

            profile.back_img=back_img
            profile.display_name=name
            profile.bio=bio
            profile.web=web


        if request.FILES.get('profileim') == None:
            profile_img = profile.profile_img
            name = request.POST['display_name']
            web = request.POST['web']
            bio = request.POST['bio']

            profile.profile_img = profile_img
            profile.display_name = name
            profile.web = web
            profile.bio = bio
            profile.save()
            return redirect('setting')
        

        if request.FILES.get('profileim') != None:
            profile_img = request.FILES.get('profileim')
            name = request.POST['display_name']
            web = request.POST['web']
            bio = request.POST['bio']

            profile.profile_img = profile_img
            profile.display_name = name
            profile.web = web
            profile.bio = bio
            profile.save()
            return redirect('setting')

            # logged_in_user = request.user

            # if logged_in_user.is_authenticated and logged_in_user.profile == profile:
            #     prof_sug = list(Profile.objects.exclude(user=user_pro))
            # else:
            #     prof_sug = list(Profile.objects.exclude(user=user_obj.user))

            # random.shuffle(prof_sug)

            # suggested_profile = prof_sug[:4]

    else:
        return render(request, "settings.html", {'profile': profile,})




def search(request):
    profile =  Profile.objects.get(user=request.user)
    if request.method == "POST":
        param = request.POST['param']
        context={}
        if param:
            users = Profile.objects.filter(Q(user__username__icontains=param) | Q(display_name__icontains=param))
            posts = Posts.objects.filter(Q(caption__icontains=param))
    context = {
        'users': users,
        'post': posts,
        'profile': profile,
        'param': param,
    }

    return render(request, "search.html", context)