
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Article, Comment, Reply, Category
from .forms import Articleform, CommentForm, ReplyForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q


def homepage(request):
    article_list = Article.objects.all()
    query = request.GET.get('axtaris')
    if query:
        article_list = article_list.filter(Q(title__icontains=query) |
                                           Q(content__icontains=query) |
                                           Q(article_author__username__icontains=query) |
                                           Q(article_author__first_name__icontains=query) |
                                           Q(article_author__last_name__icontains=query) |
                                           Q(article_category__category_name__icontains=query)
                                           ).distinct()
    paginator = Paginator(article_list, 3)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    return render(request, 'homepage.html', {'articles': articles})

@login_required(login_url='login')
def article_create(request):
    if request.user.userprofile.user_type.id == 2:
        article_form = Articleform()
        if request.method == 'POST':
            article_form = Articleform(request.POST or None, request.FILES or None)
            if article_form.is_valid():
                article = article_form.save(commit=False)
                article.article_author = request.user

                article.save()

                return redirect(article.get_absolute_url())
        return render(request, 'article_create.html', context={'form': article_form})

    else:
        return redirect('homepage')


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    #parent = get_object_or_404(Comment, )
    #Reply.objects.filter(parent=parent)
    comment_form = CommentForm(request.POST or None)
    reply_form = ReplyForm(request.POST or None)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.commenter_name = request.user
        comment.article = article
        comment.save()
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.replier_name = request.user
            #parent = Reply.objects.filter(parent=comment.id)
            reply.parent = comment.id
            reply.save()
        return redirect(article.get_absolute_url())


    return render(request, 'article_detail.html', {'article': article, 'form': comment_form, 'reply_form': reply_form})

@login_required(login_url='login')
def article_update(request, slug):

    article = get_object_or_404(Article, slug=slug)
    if article.article_author == request.user:
        article_form = Articleform(request.POST or None, request.FILES or None, instance=article)
        if article_form.is_valid():
            article_form.save()

            return redirect(article.get_absolute_url())

        return render(request, 'article_create.html', context={'form': article_form})
    else:
        return redirect('homepage')

@login_required(login_url='login')
def article_delete(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if article.article_author == request.user:
        article.delete()
        return redirect('homepage')
    else:
        return redirect('homepage')

def categories_list(request):

    category_list = Category.objects.all()
    query = request.GET.get('axtaris')
    if query:
        category_list = category_list.filter(Q(category_name__icontains=query))


    return render(request, 'categories.html', {'categories_list': category_list})

def article_from_category(request, slug):
    article_list_category = get_object_or_404(Category, slug=slug)
    article_list = Article.objects.all()

    return render(request, 'article_from_category.html', {'article_list_category': article_list_category, 'article_list': article_list})

