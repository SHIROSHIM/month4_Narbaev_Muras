from django.shortcuts import render, redirect
from posts.models import Post, Hashtag, Comment
from posts.forms import PostCreateForm, CommentCreateForm


# Create your views here.

PAGINATION_LIMIT = 3

def main_view(request):
    return render(request, 'layouts/index.html')


def posts_view(request):
    if request.method == "GET":
        hastsag_id = int(request.GET.get('hashtag_id', 0))
        text = request.GET.get('text')
        page = int(request.GET.get('page', 1))

        if hastsag_id:
            posts = Post.objects.filter(hastsag_in=[hastsag_id])
        else:
            post = Post.objects.all()
        if text:
            posts = Post.objects.filter(title_icontains=text)


        max_page = posts.__len__() / PAGINATION_LIMIT

        if round(max_page) < max_page:
            max_page = round(max_page)+1

        max_page = int(max_page)
        posts = posts[PAGINATION_LIMIT * (page-1):PAGINATION_LIMIT * page]


        return render(request, 'posts/posts.html', context={
            'posts': posts,
            'user': None if request.user.is_anainymous else request.user,
            'pages': range(1, max_page+1)
        })




def post_detail_view(request, id):
    if request.method == 'GET':
        post = Post.objects.get(id=id)
        form = CommentCreateForm(data=request.POST)

        context = {
            'post': post,
            'comments': post.comment_set.all(),
            'hastahs': post.hashtags.all(),
            'comment form': CommentCreateForm
        }

        return render (request, 'post/detail.html', context=context)

    if request.method == 'POST':
        post = Post.objects.get(id=id)
        form = CommentCreateForm(date=request.POST)

        if form.is_valid():
            Comment.objects.create(
                post_id=id,
                text=form.cleaned_data.get('text')
            )
            return redirect(f'/posts/{id}/')
        else:
            return render(request, 'posts/detail.html', context={
                'post': post,
                'comments': post.comment_set.all(),
                'hastahs': post.hashtags.all(),
                'comment form': CommentCreateForm
            })

def post_create_view(request):
    if request.method == 'GET':
        return render(request, 'posts/create.html', context={
            'form': PostCreateForm
        })

    if request.method == 'POST':
        form = PostCreateForm(data=request.POST)

        if form.is_valid():
            Post.objects.create(
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('descripton'),
                rate=form.cleaned_data.get('rate', 0)
            )
            return redirect('/posts/')
        else:
            return render(request, 'posts/create.html', context={
                'form': form
            })