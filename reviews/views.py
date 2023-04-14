from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Review, Comment
from .forms import ReviewForm, CommentForm
from PIL import Image
from io import BytesIO
# Create your views here.
def index(request):
    reviews = Review.objects.all()
    context = {
        'reviews': reviews,
    }
    return render(request, 'reviews/index.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            # 변수에 사용자가 업로드한 이미지 파일 데이터를 할당
            image = form.cleaned_data['image']
            # 이미지 파일을 바이트 스트림으로 읽은 후, Pillow 패키지의 Image.open() 메소드로 open
            img = Image.open(BytesIO(image.read()))
            # 이미지 크기를 60x100으로 변경
            img_resized = img.resize((60, 100))
            # 변수에 BytesIO 객체를 생성
            output = BytesIO()
            # 리사이즈된 이미지를 JPEG 포맷으로 저장
            img_resized.save(output, format='JPEG')
            # output 객체의 파일 포인터를 맨 앞으로 이동
            output.seek(0)
            review = form.save(commit=False)
            review.user = request.user
            review = form.save()
            return redirect('reviews:detail', review.pk)
    else:
        form = ReviewForm()
    context = {
        'form': form,
    }
    return render(request, 'reviews/create.html', context)



def detail(request, pk):
    review = Review.objects.get(pk=pk)
    review_count = Review.objects.filter(pk__lte=review.pk).count()
    comment_form = CommentForm()
    comments = review.comment_set.all()
    context = {
        'review': review,
        'comment_form': comment_form,
        'comments': comments,
        'review_count': review_count,
    }
    return render(request, 'reviews/detail.html', context)


@login_required
def delete(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user == review.user:
        review.delete()
    return redirect('reviews:index')


@login_required
def update(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user == review.user:
        if request.method == 'POST':
            form = ReviewForm(request.POST, request.FILES, instance=review)
            if form.is_valid():
                image = form.cleaned_data['image']
                img = Image.open(BytesIO(image.read()))
                img_resized = img.resize((60, 100))
                output = BytesIO()
                img_resized.save(output, format='JPEG')
                output.seek(0)
                form.save()
                return redirect('reviews:detail', review.pk)
        else:
            form = ReviewForm(instance=review)
    else:
        return redirect('reviews:index')
    context = {
        'review': review,
        'form': form,
    }
    return render(request, 'reviews/update.html', context)


@login_required
def comment_create(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment_form.save()
        return redirect('reviews:detail', review.pk)
    context = {
        'review': review,
        'comment_form': comment_form,
    }
    return render(request, 'reviews/detail.html', context)


@login_required
def comment_delete(request, review_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('reviews:detail', review_pk)