from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import *
from .forms import *
from django.template import RequestContext
from django.contrib.auth.models import User
from django.db.models import Q
import math

IMAGES_PER_PAGE = 15


def StartSession(request, user):
    request.session['logged'] = True
    request.session['nick'] = user.username
    request.session['id'] = user.id
    request.session['admin'] = user.is_staff


def CheckLogged(request, context):
    if 'logged' in request.session.keys():
        context['logged'] = True
        context['nick'] = request.session['nick']
        context['admin'] = request.session['admin']
        context['userID'] = request.session['id']


def main(request):
    query = request.GET.get('query', '')
    page = int(request.GET.get('page', 0))
    template = loader.get_template('main.html')
    users = User.objects.all().values()
    if query == '':
        images = Image.objects.all()
    else:
        images = Image.objects.filter(Q(title__icontains=query) | Q(author__username__icontains=query)).all()
    max_pages = math.ceil(len(images) / IMAGES_PER_PAGE)

    context = {
        'users': users,
        'images': images[IMAGES_PER_PAGE * page:IMAGES_PER_PAGE * (page + 1)],
        'logged': False,
        'max_pages': max_pages,
        'prev_page': page - 1,
        'next_page': page + 1,
        'query': query
    }

    CheckLogged(request, context)

    return HttpResponse(template.render(context, request))


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            user = User.objects.filter(email=form.data['mail']).first()
            if user is None:
                form = LoginForm()
                template = loader.get_template('form.html')
                error = {
                    'reason': "Nieprawidłowe dane"
                }
                return render(request, "form.html", {"form": form, "error": error,"submit_text": "zaloguj się"})
            else:
                StartSession(request, user)
                return redirect("..")
        else:
            form = LoginForm()
            template = loader.get_template('form.html')
            return render(request, "form.html", {"form": form,"submit_text": "zaloguj się"})
    else:
        form = LoginForm()
        template = loader.get_template('form.html')
        return render(request, "form.html", {"form": form,"submit_text": "zaloguj się"})


def logout(request):
    request.session.flush()
    return redirect("..")


def register(request):
    if request.method == 'POST':
        template = loader.get_template('form.html')
        form = RegisterForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass

            user_by_mail = User.objects.filter(email=form.data['mail']).first()
            user_by_nick = User.objects.filter(username=form.data['nick']).first()
            if user_by_mail is None and user_by_nick is None:
                user = User.objects.create_user(form.data['nick'], form.data['mail'], form.data['password'])
                StartSession(request, user)
                return HttpResponseRedirect("..")
            else:
                template = loader.get_template('form.html')
                form = RegisterForm()
                error = {}
                if user_by_mail is not None:
                    error['reason'] = "Mail już w użyciu"
                elif user_by_nick is not None:
                    error['reason'] = "Nick już w użyciu"
                return render(request, "form.html", {"form": form, 'error': error,"submit_text": "zarejestruj się"})
    else:
        template = loader.get_template('form.html')
        form = RegisterForm()
        return render(request, "form.html", {"form": form,"submit_text": "zarejestruj się"})


def publish(request):
    if request.method == 'POST':
        form = PublishForm(request.POST, request.FILES)  # A form bound to the POST data
        context = {"form": form}
        CheckLogged(request, context)
        if form.is_valid():  # All validation rules pass
            image = form.save(commit=False)
            image.author = User.objects.filter(id=request.session['id']).first()
            image.save()
            return HttpResponseRedirect("..")
        else:
            print(form.errors)
            form = PublishForm()
            context['error'] = "Nieprawidłowe dane"
            context['form'] = form

            return render(request, "form.html", context)
    else:
        template = loader.get_template('form.html')
        form = PublishForm()
        context = {"form": form,"submit_text": "opublikuj"}

        CheckLogged(request, context)

        return render(request, "form.html", context)


def getCommentTree(commentID) -> []:
    comments = Comment.objects.filter(respondedCommentID=commentID).all()
    for comment in comments:
        comment.subcomments = getCommentTree(comment.id)

    return comments


def show_image(request):
    if request.method == 'POST':
        image = Image.objects.filter(id=request.GET.get("imageID")).first()
        if request.POST.get("type") == "remove_image" and (request.session['admin'] or image.author.id == request.session['id']):
            Image.objects.filter(id=request.GET.get("imageID")).delete()
            return HttpResponseRedirect("..")
        if request.POST.get("type") == "delete_comment" and request.session['admin']:
            comment = Comment.objects.filter(id=request.POST.get("respondedCommentID")).update(
                text='Komentarz usunięty przez moderatorów',
                deleted=True
            )
            return HttpResponseRedirect(request.path_info + '?imageID=' + request.GET.get("imageID"))
        else:
            comment = Comment()
            comment.image = Image.objects.filter(id=request.GET.get("imageID")).first()
            comment.text = request.POST.get("text", '')
            comment.user = User.objects.filter(id=request.session['id']).first()
            if request.POST.get("type") == 'comment':
                comment.respondedCommentID = -1
            else:
                comment.respondedCommentID = int(request.POST.get("respondedCommentID", ''))

            if comment.text != '' and comment.user is not None:
                comment.save()

            response = redirect('image')
            response['Location'] += '?imageID=' + str(request.GET.get("imageID"))
            return response
    else:

        imageID = request.GET.get("imageID")

        image = Image.objects.filter(id=imageID).first()
        if image is None:
            return redirect("..")

        context = {
            "image": image
        }

        comments = Comment.objects.filter(image=image, respondedCommentID=-1).all()
        context['comments'] = comments
        for comment in comments:
            comment.subcomments = getCommentTree(comment.id)

        CheckLogged(request, context)
        return render(request, "image.html", context)


def profile(request):
    query = request.GET.get('query', '')
    userID = int(request.GET.get('userID', -1))
    if userID == -1:
        pass  # redirect

    author = User.objects.filter(id=userID).first()
    page = int(request.GET.get('page', 0))
    template = loader.get_template('profile.html')
    users = User.objects.all().values()
    if query == '':
        images = Image.objects.filter(author=author).all()
    else:
        images = Image.objects.filter(
            (Q(title__icontains=query) | Q(author__username__icontains=query))
            & Q(author=author)
        ).all()
    max_pages = math.ceil(len(images) / IMAGES_PER_PAGE)

    context = {
        'users': users,
        'images': images[IMAGES_PER_PAGE * page:IMAGES_PER_PAGE * (page + 1)],
        'logged': False,
        'max_pages': max_pages,
        'prev_page': page - 1,
        'next_page': page + 1,
        'author': author,
        'profile_search': True
    }
    if query != '':
        context['url'] = '/profile?userID=' + str(userID) + '&query=' + query + '&'
    else:
        context['url'] = '/profile?userID=' + str(userID) + '&'

    CheckLogged(request, context)

    return HttpResponse(template.render(context, request))


def edit_publish(request):
    if request.method == 'POST':
        if request.POST.get('type', '') == 'update':
            form = UpdateImageForm(request.POST)  # A form bound to the POST data
            context = {"form": form}
            CheckLogged(request, context)
            if form.is_valid():  # All validation rules pass
                image = Image.objects.filter(id=request.POST.get("imageID")).first()
                image.title = form.data['title']
                image.description = form.data['description']
                image.save()
                return HttpResponseRedirect("..")
            else:
                print(form.errors)
                form = PublishForm()
                context['error'] = "Nieprawidłowe dane"
                context['form'] = form

                return render(request, "form.html", context)
        elif request.POST.get('type', '') == 'begin':
            image = Image.objects.filter(id=request.POST.get("imageID")).first()
            template = loader.get_template('form.html')
            form = UpdateImageForm(initial={
                'title': image.title,
                'description': image.description,
                'imageID': image.id
            })
            context = {
                "form": form,
                "submit_text": "zaktualizuj"
            }

            CheckLogged(request, context)

            return render(request, "form.html", context)
