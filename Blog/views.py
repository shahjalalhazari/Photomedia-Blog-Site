from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import CreateView, ListView, TemplateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from . import models, forms


# INDEX VIEW
def index(request):
    blogs = models.Blog.objects.all()[:6]
    categorys = models.Category.objects.all()[:8]
    return render(request, 'Blog/index.html', {'blogs':blogs, 'categorys':categorys})


# WRITE BLOG
class WriteBlog(LoginRequiredMixin, CreateView):
    model = models.Blog
    template_name = 'Blog/write-blog.html'
    fields = ['category', 'title', 'body', 'image']
    def form_valid(self, form):
        blog = form.save(commit=False)
        blog.author = self.request.user
        blog.save()
        return HttpResponseRedirect(reverse('blog:full_blog', kwargs={'slug':blog.slug}))


# CREATE CATEGORY
class CreateCategory(LoginRequiredMixin, CreateView):
    model = models.Category
    template_name = 'Blog/create-category.html'
    fields = ['name', 'image']
    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('blog:write'))


# ALL BLOGS
class BlogList(ListView):
    context_objects_name = 'blog_list'
    model = models.Blog
    template_name = 'Blog/blogs.html'
    def get_context_date(self, **kwargs):
        context = super(BlogList, self).get_context_data(**kwargs)
        context['cats'] = models.Category.objects.all()
        return context


# FULL/SINGLE BLOG
@login_required
def full_blog(request, slug):
    blog = models.Blog.objects.get(slug=slug)
    form = forms.CommentForm()
    if request.method == "POST":
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            comment_form = form.save(commit=False)
            comment_form.user = request.user
            comment_form.blog = blog
            comment_form.save()
            return HttpResponseRedirect(reverse('blog:full_blog', kwargs={'slug':slug}))
    # Like & Unlike
    like = models.Like.objects.filter(blog=blog, user=request.user)
    if like:
        liked = True
    else:
        liked = False
    # Edit & Delete
    editable = False
    if request.user == blog.author and blog.author.is_authenticated:
        editable = True 
    return render(request, 'Blog/full-blog.html', {'blog':blog, 'form':form, 'liked':liked,'editable':editable})


# LIKE VIEW
def like(request, pk):
    blog = models.Blog.objects.get(pk=pk)
    user = request.user
    liked = models.Like.objects.filter(blog=blog, user=user)
    if not liked:
        like = models.Like(blog=blog, user=user)
        like.save()
    return HttpResponseRedirect(reverse('blog:full_blog', kwargs={'slug':blog.slug}))


# UNLIKE VIEW
def unlike(request, pk):
    blog = models.Blog.objects.get(pk=pk)
    user = request.user
    liked = models.Like.objects.filter(blog=blog, user=user)
    liked.delete()
    return HttpResponseRedirect(reverse('blog:full_blog', kwargs={'slug':blog.slug}))


# ALL CATEGORY
def category_list(request):
    categories = models.Category.objects.all()
    return render(request, 'Blog/categories.html', {'categories':categories})


# BLOG LIST BY THEIR CATEGORY
def category(request, cat_id):
    cats_info = models.Category.objects.get(pk=cat_id)
    blog_list = models.Blog.objects.filter(category=cat_id)
    return render(request, 'Blog/blog_by_cats.html', {'blog_list':blog_list, 'cats_info':cats_info})


# EDIT BLOG
class EditBlog(LoginRequiredMixin, UpdateView):
    model = models.Blog
    template_name = 'Blog/edit-blog.html'
    fields = ['category', 'title', 'body', 'image']
    def get_success_url(self):
        return reverse('blog:full_blog', kwargs={'slug':self.object.slug})


# DELETE BLOG
class DeleteBlog(LoginRequiredMixin, DeleteView):
    context_object_name = 'blog'
    model = models.Blog
    template_name = 'Blog/delete.html'
    success_url = reverse_lazy('account:profile')