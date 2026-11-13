from django.shortcuts import render, redirect, get_object_or_404
from .models import Notice
from .forms import NoticeForm

def notice_list(requst):
    if requst.method == 'POST':
        form = NoticeForm(requst.POST)
        if form.is_valid():
            form.save()
            return redirect('noticle_list')
    else:
        form = NoticeForm()
    
    notices = Notice.objects.all().order_by('-created_at')
    
    context = {
        'notices': notices,
        'form': form
    }
    return render(requst, 'notices/notice_list.html', context)

def notice_detail(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    
    context = {
        'notice' : notice
    }
    
    return render(request, 'notices/notice_detail.html', context)