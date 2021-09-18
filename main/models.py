from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Group, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator as username_validator
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation



from .managers import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    email = models.EmailField(blank=True, unique=True)
    first_name = models.CharField(verbose_name='Имя', max_length=30, blank=True)
    last_name = models.CharField(verbose_name="Фамилия", max_length=30, blank=True)
    middle_name = models.CharField(verbose_name="Отчество", max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    birth_date = models.DateTimeField(blank=True, null=True)
    avatar = models.ImageField(upload_to='main/static/avatars', default='main/static/avatars/default_ava.png')
    is_staff = models.BooleanField(default=False,
                                   help_text=('Designates whether the user can log into this admin site.'), )
    is_active = models.BooleanField(default=True, help_text=(
        'Designates whether this user should be treated as active. '
        'Unselect this instead of deleting accounts.'
    ),
                                    )
    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('email',)

class Customer(models.Model):
    user = models.ForeignKey(User, related_name='customers', default='', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class Contact(models.Model):
    customer = models.ForeignKey(Customer, verbose_name='Пользователь',default=None, on_delete=models.CASCADE, related_name='contacts')
    adress = models.CharField(verbose_name='Адрес', blank=True, max_length=150)
    phone_number = models.CharField(verbose_name='Телефон', blank=True, max_length=12, unique=True)

    class Meta:
        verbose_name = "Контактные данные"
        verbose_name_plural = "Контактные данные"

    def __str__(self):
        return str(self.pk)


class Subscriber(models.Model):
    customer = models.OneToOneField(Customer, verbose_name="Подписчик", on_delete=models.CASCADE, related_name="subscribers")
    is_active = models.BooleanField(verbose_name='Подписка активна', default=True)
    from_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"

    def __str__(self) -> str:
        return str(self.user)



class Category(models.Model):
    name = models.CharField(max_length=15)
    slug = models.SlugField(unique=True, default='')


    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

        # задаёт ограничение уникальности для данных полей.
        # constraints = [
        #     models.UniqueConstraint(fields=['parameters.name'], name='unique_item')
        # ]

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        """Переопределение метода save() с добавлением генерации значения для поля :param slug.
        """

        if self.slug is None:
            self.slug = slugify(self.name)
        return super().save(self, *args, **kwargs)



class Brand(models.Model):
    name = models.CharField(max_length=20, blank=True, verbose_name='Бренд')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        ordering = ('name',)



class Item(models.Model):
    category = models.ManyToManyField(Category,
                                      verbose_name='Категория товаров',
                                      related_name='%(app_label)s_%(class)s_items',
                                      related_query_name='%(app_label)s_%(class)s_items',
                                      blank=True)
    brand = models.ForeignKey(Brand, max_length=80, verbose_name='Фирма', blank=True, on_delete=models.CASCADE)
    model = models.CharField(max_length=20, verbose_name='Модель')
    description = models.CharField(max_length=100, verbose_name='Описание товара', blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    in_stock_qty = models.PositiveIntegerField(verbose_name='Количество товара',default=0)
    # picture = models.ForeignKey(ItemPicture,
    #                             blank=True,
    #                             on_delete=models.CASCADE,
    #                             verbose_name='Изображение товара',
    #                             related_name='%(app_label)s_%(class)s_items',
    #                             related_query_name='%(app_label)s_%(class)s_items',
    #                             )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = "Товары"
        abstract = True

    def __str__(self):
        return f'{self.brand} {self.model}'


class ItemPicture(models.Model):
    image = models.ImageField(upload_to='main/static/item_pictures', verbose_name='Изображение')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товара'

    def __str__(self) -> str:
        return f'{self.id}'

class Parameter(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название')
    units = models.CharField(max_length=5, verbose_name='Единицы измерения', blank=True)
    category = models.ManyToManyField(Category, blank=True, default='', related_name='parameters')

    class Meta:
        verbose_name = 'Характеристика товара'
        verbose_name_plural = "Характеристики товара"
        ordering = ('name',)

    def __str__(self):
        return self.name


class ItemParameter(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    parameter = models.ForeignKey(Parameter, verbose_name='Параметр', related_name='product_parameters', blank=True,
                                  on_delete=models.CASCADE)
    value = models.CharField(verbose_name='Значение', max_length=100)

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = "Список параметров товаров"




class Tag(models.Model):
    name = models.CharField(max_length=10, verbose_name="Название тега")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self) -> str:
        return str(self.name)


class Review(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Пользователь')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    stars = models.PositiveIntegerField(verbose_name='Рейтинг')
    text = models.CharField(max_length=200, null=True, verbose_name='Текст')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата отзыва')

    class Meta:
        verbose_name='Отзыв'
        verbose_name_plural='Отзывы'


class Notebook(Item):
    parameter = GenericRelation(ItemParameter)

    class Meta(Item.Meta):
        verbose_name = 'Ноутбук'
        verbose_name_plural = 'Ноутбуки'


class Phone(Item):

    class Meta(Item.Meta):
        verbose_name = 'Смартфон'
        verbose_name_plural = 'Смартфоны'


class Fridge(Item):

    class Meta(Item.Meta):
        verbose_name = 'Холодильник'
        verbose_name_plural = 'Холодильники'