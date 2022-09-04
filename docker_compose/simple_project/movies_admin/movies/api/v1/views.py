from django.contrib.postgres.aggregates import ArrayAgg
from django.http import JsonResponse
from django.db.models import Q
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView

from movies.models import FilmWork, PersonsKinds


# класс-миксин для остальных классов
class MoviesMixin:
    model = FilmWork
    http_method_names = ['get']

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        # Получение и обработка данных
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )

        results = queryset.values('id', 'title', 'description',
            'creation_date', 'rating', 'type').annotate(
                genres=ArrayAgg('genres__name',
                                distinct=True)).annotate(
                actors=ArrayAgg('persons__full_name',
                                distinct=True,
                                filter=Q(personfilmwork__role=
                                         PersonsKinds.ACTOR))).annotate(
                directors=ArrayAgg('persons__full_name',
                                distinct=True,
                                filter=Q(personfilmwork__role=
                                         PersonsKinds.DIRECTOR))).annotate(
                writers=ArrayAgg('persons__full_name',
                                distinct=True,
                                filter=Q(personfilmwork__role=
                                         PersonsKinds.WRITER)))

        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
        }

        if page.has_previous():
            context['prev'] = page.previous_page_number()
        else:
            context['prev'] = None

        if page.has_next():
            context['next'] = page.next_page_number()
        else:
            context['next'] = None

        context['results'] = list(results)

        return context


class MovieDetailApi(MoviesMixin, BaseDetailView):

    def get_queryset(self):
        queryset = super(MoviesMixin, self).get_queryset().values(
            'id', 'title', 'description',
            'creation_date', 'rating', 'type').annotate(
            genres=ArrayAgg('genres__name',
                            distinct=True)).annotate(
            actors=ArrayAgg('persons__full_name',
                            distinct=True,
                            filter=Q(personfilmwork__role=
                                     PersonsKinds.ACTOR))).annotate(
            directors=ArrayAgg('persons__full_name',
                            distinct=True,
                            filter=Q(personfilmwork__role=
                                     PersonsKinds.DIRECTOR))).annotate(
            writers=ArrayAgg('persons__full_name',
                            distinct=True,
                            filter=Q(personfilmwork__role=
                                     PersonsKinds.WRITER)))

        return queryset

    def get_context_data(self, **kwargs):
        context = {}
        for item in self.object:
            context[item] = self.object[item]

        return context
