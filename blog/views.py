# import email
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 10
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month,
                             publish__day=day)

    #list of actie comments for specific post
    comments = post.comments.filter(active=True)

    new_comment = None
    comment_form = None

    if request.method == 'POST':
        # published post
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            #creating comment objectg, currently not saved in database
            new_comment = comment_form.save(commit=False)
            # assign comment to current post
            new_comment.post = post
            #saving comment in database
            new_comment.save()
        else:
            comment_form = CommentForm()
    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form})

def post_share(request, post_id):
    #uploading post based on its identifier:
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        #form if sent
        form = EmailPostForm(request.POST)
        if form.is_valid():
            #verification form fields
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{}  ({}) zachęca do przeczytania "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Przeczytaj post "{}" na stronie {}\n\n Komentarz dodany przez {}: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'astamalinowska@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})