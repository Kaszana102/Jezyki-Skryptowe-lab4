from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import *
from .forms import *
from django.template import RequestContext


def StartSession(request, user):
    request.session['logged'] = True
    request.session['nick'] = user.nick
    request.session['id'] = user.id


def main(request):
    template = loader.get_template('main.html')
    users = User.objects.all().values()
    images = Image.objects.all().values()
    context = {
        'users': users,
        'images': images,
        'logged': False
    }

    if 'logged' in request.session.keys():
        context['logged'] = True
        context['nick'] = request.session['nick']

    return HttpResponse(template.render(context, request))


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            user = User.objects.filter(mail=form.data['mail']).first()
            if user is None:
                form = LoginForm()
                template = loader.get_template('form.html')
                error = {
                    'reason': "Nieprawidłowe dane"
                }
                return render(request, "form.html", {"form": form, "error": error})
            else:
                StartSession(request, user)
                return redirect("..")
        else:
            form = LoginForm()
            template = loader.get_template('form.html')
            return render(request, "form.html", {"form": form})
    else:
        form = LoginForm()
        template = loader.get_template('form.html')
        return render(request, "form.html", {"form": form})


def logout(request):
    request.session.flush()
    return redirect("..")


def register(request):
    if request.method == 'POST':
        template = loader.get_template('form.html')
        form = RegisterForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass

            user = User.objects.filter(mail=form.data['mail']).first()
            if user is None:
                user = User(nick=form.data['nick'], mail=form.data['mail'], password=form.data['password'])
                user.save()
                StartSession(request, user)
                return HttpResponseRedirect("..")
            else:
                template = loader.get_template('form.html')
                form = RegisterForm()
                error = {
                    'reason': "Mail już w użyciu"
                }
                return render(request, "form.html", {"form": form, 'error': error})
    else:
        template = loader.get_template('form.html')
        form = RegisterForm()
        return render(request, "form.html", {"form": form})


def publish(request):
    if request.method == 'POST':
        form = PublishForm(request.POST, request.FILES)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            image = form.save(commit=False)
            image.authorID = request.session['id']
            image.save()
            return HttpResponseRedirect("..")
        else:
            print(form.errors)
            form = PublishForm()
            error = {
                'reason': "Nieprawidłowe dane"
            }
            return render(request, "form.html", {"form": form, 'error': error})
    else:
        template = loader.get_template('form.html')
        form = PublishForm()
        return render(request, "form.html", {"form": form})
