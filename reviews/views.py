
from django.shortcuts import render,redirect
from .models import Review,Comment
from .forms import CommentForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

@login_required
def create(request):
    if request.method == 'POST':
        data = ReviewForm(request.POST, request.FILES)
        if data.is_valid():
            db_data = data.save(commit=False)
            db_data.user = request.user
            db_data.save()
            return redirect('reviews:index')
    else:
        data = ReviewForm()
    return render(request,'reviews/create.html',{'data':data})

def index(request):
    review = Review.objects.all().order_by('-pk')
    page = request.GET.get('page') #GET 방식으로 정보를 받아오는 데이터
    paginator = Paginator(review, '5') #Paginator(분할될 객체, 페이지 당 담길 객체수)
    page_obj = paginator.get_page(page) #페이지 번호를 받아 해당 페이지를 리턴 get_page 권장
    context = {
        'review':review,
        'page': page_obj,
    }
    return render(request,'reviews/index.html',context)

def detail(request, pk):
    review = Review.objects.get(pk=pk)
    comment_form = CommentForm()
     
    context = {
        'review':review,
        'comment_form':comment_form,
        'comments': review.comment_set.all(),
    }
    return render(request, 'reviews/detail.html',context)


def comment_create(request,pk):
    review = Review.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    print(comment_form,request.POST)
    if comment_form.is_valid():
        
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
    return redirect('reviews:detail', review.pk)


def comment_delete(request,pk,comment_pk):
    comment = Comment.objects.get(pk = comment_pk)
    if request.user == comment.user: 
        comment.delete()
    return redirect('reviews:detail',pk)

def update(request,pk):
    db_data = Review.objects.get(pk=pk)

    if request.method == 'POST':
        data = ReviewForm(request.POST, instance=db_data)

        if data.is_valid():
            data.save()

            return redirect('reviews:index')

    else:
        data = ReviewForm(instance=db_data)

    return render(request, 'reviews/create.html', {'data': data})

def delete(request, pk):
    review = Review.objects.get(pk=pk)
    review.delete()

    return redirect('reviews:index')

