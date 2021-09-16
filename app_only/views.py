from django.shortcuts import render,redirect,HttpResponse
import bcrypt
from django.contrib import messages
from .models import User, Sneaker, Comment, Image
from .forms import ImageForm

# Create your views here.

def index(request):
    sneakers = Sneaker.objects.all().order_by('sku_number')
    context = {
        'sneakers' : sneakers,
    }
    return render(request,"home.html", context)

def login_page(request):
    return render(request,'register_login.html')

def register(request):
    errors = User.objects.register_validation(request.POST)
    if errors:
        for value in errors.values():
            messages.error(request, value, extra_tags="register")

    else:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()

        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pw_hash,
            birthdate = request.POST['birthdate']
        )
        request.session['user_id'] = user.id
        return redirect('/user_dashboard')
    return redirect('/login_register')

def login(request):
    errors = User.objects.login_validation(request.POST)
    if errors: 
        for value in errors.values():
            messages.error(request, value, extra_tags='login')

    else:
        user = User.objects.filter(email = request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect('/user_dashboard')
            else:
                messages.error(request, "Email or Password not match!", extra_tags='login')

        if not user:
            messages.error(request,"This email address not register yet!!! Please go to register!", extra_tags='login')

    return redirect('/login_register')

def logout(request):
    request.session.flush()
    return redirect('/')

def user_dashboard(request):
    # return render(request,"user_page.html")
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        user_sneakers = user.sneaker_posted.all()
        user_comments = user.user_comments.all()
        user_likes = user.liked_sneakers.all()
        context = {
            'user': user,
            'user_sneakers': user_sneakers,
            'user_comments': user_comments,
            'user_likes': user_likes
        }
        return render(request, 'user_page.html', context)


def create_sneaker_page(request):
    return render(request, "create_sneaker.html")

def create_sneaker(request):
    # return render(request, 'create_sneaker.html')
    errors = Sneaker.objects.sneaker_validation(request.POST)
    if errors:
        for value in errors.values():
            messages.error(request, value)

    else:
        user = User.objects.get(id = request.session['user_id'])
        sneaker = Sneaker.objects.create(
            sneaker_name = request.POST['sneaker_name'],
            color = request.POST['color'],
            sku_number = request.POST['sku_number'],
            release_price = request.POST['release_price'],
            release_date = request.POST['release_date'],
            sneaker_size = request.POST['sneaker_size'],
            buy_price = request.POST['buy_price'],
            posted_by = user,
        )
        request.session['sneaker_id'] = sneaker.id

        #Need to update to sneaker page
        return redirect('/user_dashboard')
            
    return redirect('/create_sneaker_page')

def upload_image(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.session["user_id"])
        sneaker = Sneaker.objects.get(id=request.POST['sneaker_id'])
        image = Image.objects.create(
            image=request.FILES['image'], 
            posted_by = user, 
            upload_on = sneaker
        )
        request.session['image_id'] = image.id

        return redirect('/user_dashboard')

def upload_comment(request, sneaker_id):
    sneaker = Sneaker.objects.get(id=sneaker_id)
    user = User.objects.get(id= request.session['user_id'])
    comment = Comment.objects.create(
        comment = request.POST['comment'],
        posted_by = user,
        upload_on = sneaker
    )

    request.session['comment_id']= comment.id

    return redirect(f'/sneakers/{sneaker_id}')


def sneaker_dashboard(request, sneaker_id):
        one_of_sneaker = Sneaker.objects.get(id= sneaker_id)
        user = User.objects.get(id=request.session['user_id'])
        this_type_sneakers = Sneaker.objects.filter(sku_number = one_of_sneaker.sku_number)
        sneaker_comments = one_of_sneaker.sneaker_comments.all()
        upload_count = this_type_sneakers.count()

        context = {
            'one_of_sneaker': one_of_sneaker,
            'this_type_sneakers': this_type_sneakers,
            'upload_count': upload_count,
            'sneaker_comments': sneaker_comments,
            'user': user
        }
        return render(request, 'sneaker_page.html', context)


def edit_sneaker_page(request, sneaker_id):
    sneaker = Sneaker.objects.get(id = sneaker_id)
    context = {
        'sneaker': sneaker
    }
    return render(request, 'edit_sneaker.html', context)

def edit_sneaker(request, sneaker_id):
    errors = Sneaker.objects.sneaker_validation(request.POST)
    if errors:
        for value in errors.values():
            messages.error(request, value)

    else:
        update_sneaker = Sneaker.objects.get(id=sneaker_id)
        update_sneaker.sneaker_name  = request.POST['sneaker_name']
        update_sneaker.color = request.POST['color']
        update_sneaker.sku_number = request.POST['sku_number']
        update_sneaker.release_price = request.POST['release_price']
        update_sneaker.release_date = request.POST['release_date']
        update_sneaker.sneaker_size = request.POST['sneaker_size']
        update_sneaker.buy_price = request.POST['buy_price']
        update_sneaker.save()

        #Need to update to sneaker page
        return redirect('/user_dashboard')
    
    return redirect(f'/sneakers/{sneaker_id}/edit_page')


def delete_sneaker(request, sneaker_id):
    delete_sneaker = Sneaker.objects.get(id = sneaker_id)
    delete_sneaker.delete()
    return redirect('/user_dashboard')

def delete_comment(request, comment_id):
    delete_sneaker_comment = Comment.objects.get(id=comment_id)
    delete_sneaker_comment.delete()
    return redirect('/user_dashboard')

def like(request, sneaker_id):
    user = User.objects.get(id= request.session['user_id'])
    sneaker = Sneaker.objects.get(id=sneaker_id)
    user.liked_sneakers.add(sneaker)
    return redirect(f'/sneakers/{sneaker_id}')


def unlike(request, sneaker_id):
    user = User.objects.get(id = request.session['user_id'])
    sneaker = Sneaker.objects.get(id=sneaker_id)
    user.liked_sneakers.remove(sneaker)
    return redirect(f'/sneakers/{sneaker_id}')


def survey(request):
    user = User.objects.get(id=request.session['user_id'])
    sneakers = Sneaker.objects.all().order_by('sku_number')

    context = {
        'user': user,
        'sneakers' : sneakers,
    }
    return render(request,"survey_page.html", context)

def unlike_in_user_dashboard(request,sneaker_id):
    user = User.objects.get(id = request.session['user_id'])
    sneaker = Sneaker.objects.get(id=sneaker_id)
    user.liked_sneakers.remove(sneaker)
    return redirect('/user_dashboard')

def like_in_survey_page(request, sneaker_id):
    user = User.objects.get(id= request.session['user_id'])
    sneaker = Sneaker.objects.get(id=sneaker_id)
    user.liked_sneakers.add(sneaker)
    return redirect('/survey')

def unlike_in_survey_page(request, sneaker_id):
    user = User.objects.get(id = request.session['user_id'])
    sneaker = Sneaker.objects.get(id=sneaker_id)
    user.liked_sneakers.remove(sneaker)
    return redirect('/survey')






    