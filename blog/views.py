from typing import Any
from django.db.models.query import QuerySet
from django.http import Http404, HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect
from .models import Post, Page
from django.views.generic import ListView, DetailView

PER_PAGE = 9


class PostListView(ListView):
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published()

    # def get_queryset(self) -> QuerySet[Any]:
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(is_published=True)

    #     return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context.update({
            'page_title': 'Home - ',
        })

        return context


class CreatedByListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context = {}

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = self._temp_context['user']

        user_full_name = user.username

        if user.first_name:
            user_full_name = f'{user.first_name} {user.last_name}'

        page_title = user_full_name + ' posts - '

        context.update({
            'page_title': page_title,
        })

        return context

    def get_queryset(self) -> QuerySet[Any]:
        querysert = super().get_queryset()
        querysert = querysert.filter(
            created_by__pk=self._temp_context['user'].pk
        )

        return querysert

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:  # noqa:E501
        author_pk = self.kwargs.get('author_pk')
        user = User.objects.filter(pk=author_pk).first()

        if user is None:
            raise Http404()

        self._temp_context.update({
            'author_pk': author_pk,
            'user': user,
        })

        return super().get(request, *args, **kwargs)


class PageDetailView(DetailView):
    model = Page
    template_name = 'blog/pages/page.html'
    slug_field = 'slug'
    context_object_name = 'page'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        page = self.get_object()
        page_title = f'{page.title} - Page - '
        context.update({
            'page_title': page_title,
        })

        return context

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(
            is_published=True
        )


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/pages/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        page_title = f'{post.title} - Post - '
        context.update({
            'page_title': page_title,
        })

        return context

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(
            is_published=True
        )


class CategoryListView(PostListView):
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(
            category__slug=self.kwargs.get('slug')
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        page_title = f'{self.object_list[0].category.name} - Category - '

        context.update({
            'page_title': page_title,
        })

        return context


class TagListView(PostListView):
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(
            tags__slug=self.kwargs.get('slug')
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        page_title = f'{self.object_list[0].tags.first().name} - Tag - '

        context.update({
            'page_title': page_title,
        })

        return context


class SearchListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._search_value = ''

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self._search_value = request.GET.get('search', '').strip()
        return super().setup(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        search_value = self._search_value

        return super().get_queryset().filter(
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value)
        )[:PER_PAGE]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        page_title = f'{self._search_value[:30]} - Search - '

        context.update({
            'search_value': self._search_value,
            'page_title': page_title,
        })

        return context

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:  # noqa:E501
        if self._search_value == '':
            return redirect('blog:index')
        return super().get(request, *args, **kwargs)
