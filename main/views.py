from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Post, Category
from .forms import PostForm, CategoryForm
from django import forms


@login_required
def post_list(request, username=None):
    status = request.GET.get("status")
    user = get_object_or_404(User, username=request.user.username)

    if user.is_superuser:
        posts = Post.objects.all()
        context = {'posts': posts}

        if status:
            posts = posts = Post.objects.filter(status=status).order_by("created_at")
            context = {'posts': posts, "status": status}

        if username:
            user = get_object_or_404(User, username=username)
            posts = Post.objects.filter(user=user)
            context = {'posts': posts, "status": status}

        return render(request, 'main/all_applications.html', context)

    else:
        posts = Post.objects.filter(user=user)
        context = {'posts': posts}

        if request.GET.get("sort") and request.GET.get("filter"):
            query = request.GET.get("filter")
            posts = Post.objects.filter(user=user, status="completed").order_by("created_at")[:4]
            post_count = Post.objects.filter(user=user, status="in_progress").count()
            len_post = Post.objects.filter(user=user, status="completed").count()

            context = {'posts': posts, "query": query, "post_count": post_count, "page": "home", "len_post": len_post}

        if status:
            posts = posts = Post.objects.filter(user=user, status=status).order_by("created_at")
            context = {'posts': posts, "status": status}

        return render(request, 'main/user_posts.html', context)


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'main/post_detail.html', {'post': post})


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'main/post_form.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        if not request.user.is_superuser:
            form.fields['status'].widget = forms.HiddenInput()
    return render(request, 'main/post_form.html', {'form': form})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, user=request.user)
    post.delete()
    return redirect('user_posts', username=request.user.username)


@login_required
@user_passes_test(lambda user: user.is_superuser)
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'main/cat_list.html', {'categories': categories})


@login_required
@user_passes_test(lambda user: user.is_superuser)
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect('category_detail', pk=category.pk)
    else:
        form = CategoryForm()
    return render(request, 'main/cat_form.html', {'form': form})


@login_required
@user_passes_test(lambda user: user.is_superuser)
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, 'main/cat_detail.html', {'category': category})


@login_required
@user_passes_test(lambda user: user.is_superuser)
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            return redirect('category_detail', pk=category.pk)
    else:
        form = CategoryForm(instance=category)
    return render(request, 'main/cat_form.html', {'form': form})


@login_required
@user_passes_test(lambda user: user.is_superuser)
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('category_list')