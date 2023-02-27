from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import login, logout, authenticate
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from .forms import ChatGroupForm, MessageForm, ReactionForm, UpdateForm
from .models import ChatGroup, Message, Reaction

@login_required(login_url="/login")
def home(request):
    return render(request, "main/home.html")

@login_required(login_url="/login")
def create_message(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/home")
    else:
        form = MessageForm()

    return render(request, 'main/create_post.html', {"form": form})

@login_required(login_url="/login")        
def update_details(request):
    if request.method == "POST":
        form = UpdateForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = UpdateForm()

    return render(request, 'registration/update_detail.html', {"form": form})

def password_reset(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "registration/password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="registration/password/password_reset.html", context={"password_reset_form":password_reset_form})

@login_required(login_url="/login")
def create_group(request):
    if request.method == 'POST':
        form = ChatGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            group.members.add(request.user)
            return redirect('group/group_detail', pk=group.pk)
    else:
        form = ChatGroupForm()
    return render(request, 'group/create_group.html', {'form': form})

@login_required(login_url="/login")
def group_detail(request, group_id):
    group = get_object_or_404(ChatGroup, id=group_id)
    members = group.members.all()
    return render(request, 'group/group_detail.html', {'group': group, 'members': members})

@login_required(login_url="/login")
def delete_group(request, group_id):
    group = get_object_or_404(ChatGroup, id=group_id)
    if request.method == 'POST':
        group.delete()
        return redirect('home')
    return render(request, 'group/delete_group.html', {'group': group})

@login_required(login_url="/login")
def search_members(request):
    if request.method == 'POST':
        query = request.POST['query']
        members = User.objects.filter(username__icontains=query)
        return render(request, 'group/search_members.html', {'members': members})
    return render(request, 'group/search_members.html')

@login_required(login_url="/login")
def add_member(request, group_id, member_id):
    group = get_object_or_404(ChatGroup, id=group_id)
    member = get_object_or_404(User, id=member_id)
    group.members.add(member)
    return redirect('group/group_detail', group.id)

@login_required(login_url="/login")
def chat_group(request, group_id):
    group = get_object_or_404(ChatGroup, id=group_id)
    messages = Message.objects.filter(group=group)
    reactions = Reaction.objects.filter(message__group=group)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.group = group
            message.save()
            return redirect('group_detail', group_id=group_id)
    else:
        form = MessageForm()
    reaction_form = ReactionForm()
    return render(request, 'group_detail.html', {'group': group, 'messages': messages, 'reactions': reactions, 'form': form, 'reaction_form': reaction_form})

@login_required(login_url="/login")
def send_message(request, group_id):
    group = get_object_or_404(ChatGroup, id=group_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.group = group
            message.save()
            return redirect('chat/chat_group', group_id=group_id)
    else:
        form = MessageForm()
    return render(request, 'chat/send_message.html', {'group': group, 'form': form})
    
@login_required(login_url="/login")
def add_reaction(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.method == 'POST':
        form = ReactionForm(request.POST)
        if form.is_valid():
            reaction = form.save(commit=False)
            reaction.message = message
            reaction.user = request.user
            reaction.save()
    return redirect('chat/chat_group', group_id=message.group.id)
