from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from django.urls import reverse_lazy
from Blogapp.models import Post,Comment
from Blogapp.form import PostForm,CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView,ListView,DetailView,
                                    CreateView,UpdateView,DeleteView)

# Create your views here.
class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    template_name='post_list.html'

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'


class CreatePostView(LoginRequiredMixin,CreateView):
    login_url='/login/'
    redirect_field_name = 'Blogapp:post_details'
    form_class = PostForm
    model = Post
    template_name = "post_form.html"

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url='/login/'
    redirect_field_name = 'Blogapp:post_details'
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('Blogapp:post_list')

class DraftListView(LoginRequiredMixin,ListView):
    login_url='/login/'
    redirect_field_name = 'Blogapp:post_details'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')
    template_name = "post_draft_list.html"


#######################################Comment#####

@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish
    return redirect('Blogapp:post_details',pk=pk)


@login_required
def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method =='POST':
        form = CommentForm()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return render('post_detail.html',pk=post.pk)
    else:
        form = CommentForm()
    return render(request,'comment_form.html',{'form':form})



@login_required
def comment_approved(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('Blogapp:post_details',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk= comment.post.pk
    comment.delete()
    return render('post_detail.html',pk= post_pk)
