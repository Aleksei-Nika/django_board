from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Notice
from .forms import NoticeForm

def notice_list(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.author = request.user
            notice.save()
            return redirect('notice_list')
    else:
        form = NoticeForm()
    
    notices = Notice.objects.all().order_by('-created_at')
    
    context = {
        'notices': notices,
        'form': form
    }
    return render(request, 'notices/notice_list.html', context)

def notice_detail(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    
    context = {
        'notice' : notice
    }
    
    return render(request, 'notices/notice_detail.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('notice_list')
    else:
        form = UserCreationForm()
    context = {
        'form' : form
    }    
    return render(request, 'notices/register.html', context)

def notice_update(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    if request.user != notice.author:
        raise PermissionDenied

    if request.method == 'POST':
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            return redirect('notice_detail', pk=notice.pk)
    else:
        form = NoticeForm(instance=notice)
    
    context = {
        'form': form,
        'notice': notice
    }
    return render(request, 'notices/notice_form.html', context)


def notice_delete(request, pk):
    notice = get_object_or_404(Notice, pk=pk)

    if request.user != notice.author:
        raise PermissionDenied

    if request.method == 'POST':
        notice.delete()
        return redirect('notice_list')
    
    context = {
        'notice': notice
    }
    return render(request, 'notices/notice_confirm_delete.html', context)