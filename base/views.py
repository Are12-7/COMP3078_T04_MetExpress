from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Village, Debate, Message, User
from .forms import VillageForm, UserForm, RegistrationForm


# REGISTER NEW USER
def registerUser(request):
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Error while creating user')

    return render(request, 'base/login.html', {'form': form})


# LOGIN
def loginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        # Check if user exist
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        # Authenticating username and password
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Does not exist
            messages.error(request, 'User email or Password Incorrect')

    context = {'page': page}
    return render(request, 'base/login.html', context)


# LOGOUT
def logoutUser(request):
    logout(request)
    return redirect('home')


# PROFILE PAGE
def profilePage(request, id):
    user = User.objects.get(id=id)
    villages = user.village_set.all()
    village_discussions = user.message_set.all()
    debates = Debate.objects.all()
    context = {'user': user, 'villages': villages,
               'village_discussions': village_discussions, 'debates': debates}
    return render(request, 'base/profile.html', context)


# GET ALL /HOME PAGE / FEEDS
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # Filtering topics / Search option
    # contains will check if the character entered by the user matches with any char in the list of debates
    villages = Village.objects.filter(
        Q(thread__topic__icontains=q) |
        Q(title__icontains=q) |
        Q(description__icontains=q)
    )

    # queryset all
    # Display 5
    debates = Debate.objects.all()[:5]
    village_count = villages.count()
    village_discussions = Message.objects.filter(
        Q(village__thread__topic__icontains=q))

    context = {'villages': villages, 'debates': debates,
               'village_count': village_count, 'village_discussions': village_discussions}

    return render(request, 'base/home.html', context)


# VILLAGE
def village(request, id):
    # queryset get by id
    village = Village.objects.get(id=id)
    # get all messages associated with a village
    village_discussions = village.message_set.all()
    sophists = village.sophists.all()

    if request.method == 'POST':
        discussions = Message.objects.create(
            user=request.user,
            village=village,
            content=request.POST.get('content')
        )
        village.sophists.add(request.user)
        return redirect('village', id=village.id)

    context = {'village': village,
               'village_discussions': village_discussions, 'sophists': sophists}
    return render(request, 'base/village.html', context)


# DEBATES/VILLAGE PAGE
@login_required(login_url='login')
def debatesPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    debates = Debate.objects.filter(topic__icontains=q)

    context = {'debates': debates}
    return render(request, 'base/debates.html', context)


# CREATE NEW VILLAGE
# only authenticated users can create new village
@login_required(login_url='login')
def createVillage(request):
    form = VillageForm()
    debates = Debate.objects.all()
    if request.method == 'POST':
        debate_topic = request.POST.get('thread')
        debate, created = Debate.objects.get_or_create(topic=debate_topic)
        Village.objects.create(
            host=request.user,
            thread=debate,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'debates': debates}
    return render(request, 'base/village_form.html', context)


# UPDATE VILLAGE
# only authenticated users can update
@login_required(login_url='login')
def updateVillage(request, id):
    village = Village.objects.get(id=id)
    form = VillageForm(instance=village)
    debates = Debate.objects.all()
    # Error message when a different user is trying to update other's user village
    if request.user != village.host:
        return HttpResponse('Sorry, you can not edit this village')

    if request.method == 'POST':
        debate_topic = request.POST.get('thread')
        debate, created = Debate.objects.get_or_create(topic=debate_topic)
        village.title = request.POST.get('title')
        village.thread = debate
        village.description = request.POST.get('description')
        village.save()
        return redirect('home')

    context = {'form': form, 'debates': debates, 'village': village}
    return render(request, 'base/village_form.html', context)


# DELETE VILLAGE
# only authenticated users can delete
@login_required(login_url='login')
def deleteVillage(request, id):
    village = Village.objects.get(id=id)

    # Error message when a different user is trying to delete other's user village
    if request.user != village.host:
        return HttpResponse('Sorry, you can not delete this village')

    if request.method == 'POST':
        village.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': village})


# DELETE DISCUSSION/COMMENT/MESSAGE
# only authenticated users can delete
@login_required(login_url='login')
def deleteDiscussion(request, id):
    village_discussions = Message.objects.get(id=id)

    # Error message when a different user is trying to delete other's user village
    if request.user != village_discussions.user:
        return HttpResponse('Sorry, you can not delete this message')

    if request.method == 'POST':
        village_discussions.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': village_discussions})


# DISCUSSIONS PAGE
def discussionsPage(request):
    village_discussions = Message.objects.all()
    context = {'village_discussions': village_discussions}
    return render(request, 'base/discussions.html', context)


# UPDATE USER/PROFILE
@login_required(login_url='login')
def updateProfile(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', id=user.id)
        else:
            return HttpResponse('Username cannot contain spaces')

    context = {'form': form}
    return render(request, 'base/edit-profile.html', context)
