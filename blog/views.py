import email
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView
from .forms import EmailPostForm


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 10
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month,
                             publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})

def post_share(request, post_id):
    #uploading post based on its identifier:
    post = get_object_or_404(Post, id=post_id, status='published')

    if request.method == 'POST':
        #form if sent
        form = EmailPostForm(request.POST)
        if form.is_valid():
            #verification form fields
            cd = form.cleaned_data
            #email can be send
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form})