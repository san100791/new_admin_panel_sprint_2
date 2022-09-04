import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator


class Types(models.TextChoices):
    MOVIE = 'movie', _('movie')
    TV = 'tv_show', _('tv_show')


class PersonsKinds(models.TextChoices):
    DIRECTOR = 'director', _('director')
    WRITER = 'writer', _('writer')
    ACTOR = 'actor', _('actor')


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('full_name'), max_length=255)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')


class FilmWork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    creation_date = models.DateField(_('creation_date'), null=True)
    file_path = models.FilePathField(_('file_path_field'), path='/', null=True)
    rating = models.FloatField(_('rating'), null=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])
    type = models.CharField(_('type'), max_length=7, choices=Types.choices)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')

    def __str__(self):
        return self.title

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('FilmWork')
        verbose_name_plural = _('FilmWorks')


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey(FilmWork, verbose_name=_('filmwork'),
                                  on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, verbose_name=_('genre'),
                              on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _('Genre of filmWork')
        verbose_name_plural = _('Genres of filmWork')
        indexes = [
            models.Index(fields=['film_work', 'genre', ],
                         name='film_work_genre_idx')
        ]
        constraints = [
            models.UniqueConstraint(fields=['film_work', 'genre', ],
                                    name='film_work_genre_idx_')
        ]


class PersonFilmwork(UUIDMixin):
    person = models.ForeignKey(Person, verbose_name=_('person'),
                               on_delete=models.CASCADE)
    film_work = models.ForeignKey(FilmWork, verbose_name=_('filmwork'),
                                  on_delete=models.CASCADE)
    role = models.CharField(_('role'), max_length=8,
                            choices=PersonsKinds.choices, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _('Person of of filmWork')
        verbose_name_plural = _('Persons of of filmWork')
        indexes = [
            models.Index(fields=['film_work', 'person', ],
                         name='film_work_person_idx')
        ]
        constraints = [
            models.UniqueConstraint(fields=['film_work', 'person', ],
                                    name='film_work_person_idx_')
        ]
