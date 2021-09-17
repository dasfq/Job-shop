from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Group, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator as username_validator
from django.template.defaultfilters import slugify

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
    avatar = models.ImageField(upload_to='avatars', default='avatars/default_ava.png')
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


class Contact(models.Model):
    user = models.ManyToManyField(User, verbose_name='Пользователь')
    adress = models.CharField(verbose_name='Адрес', blank=True, max_length=10)
    phone_number = models.CharField(verbose_name='Телефон', blank=True, max_length=12, unique=True)

    class Meta:
        verbose_name = "Контактные данные"
        verbose_name_plural = "Контактные данные"

    def __str__(self):
        return str(self.pk)


class Subscriber(models.Model):
    user = models.OneToOneField(User, verbose_name="Подписчик", on_delete=models.CASCADE, related_name="subscribers")
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

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        """Переопределение метода save() с добавлением генерации значения для поля :param slug.
        """

        if self.slug is None:
            self.slug = slugify(self.name)
        return super().save(self, *args, **kwargs)


class Article(models.Model):
    category = models.ForeignKey(Category, default="", null=False, on_delete=models.CASCADE, verbose_name='Категория')
    title = models.CharField(max_length=200, null=False, default="", verbose_name='Заголовок')
    sub_title = models.CharField(max_length=200, null=False, default="", verbose_name='Подзаголовок')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name='Описание категории'
        verbose_name_plural='Описания категории'

    def __str__(self):
        return self.title


class Shop(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    is_active = models.BooleanField(verbose_name='Статус приёма заказов', default=True)
    category = models.ManyToManyField(Category, verbose_name="Категория")

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = "Список магазинов"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Item(models.Model):
    category = models.ManyToManyField(Category, verbose_name='Категория товаров', related_name='products', blank=True)
    name = models.CharField(max_length=20, verbose_name='Название')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = "Список товаров"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class ItemInfo(models.Model):
    item = models.ForeignKey(Item, verbose_name='Товар', blank=True, on_delete=models.CASCADE)
    brand = models.CharField(max_length=80, verbose_name='Фирма', blank=True)
    description = models.CharField(max_length=100, verbose_name='Описание товара', blank=True)
    external_id = models.PositiveIntegerField(verbose_name='Внешний ИД')
    price = models.PositiveIntegerField(verbose_name='Цена')
    price_rrc = models.PositiveIntegerField(verbose_name='Рекомендуемая розничная цена')
    shop = models.ForeignKey(Shop, verbose_name='Магазин', related_name='item_infos', blank=True,
                             on_delete=models.CASCADE)
    in_stock_qty = models.PositiveIntegerField(verbose_name='Количество товара',default=0)

    class Meta:
        verbose_name = 'Информация о товаре'
        verbose_name_plural = "Информации о товаре"
        ordering = ('-item',)

        # задаёт ограничение уникальности для данных полей.
        constraints = [
            models.UniqueConstraint(fields=['item', 'shop', 'external_id'], name='unique_item_info')
        ]

    def __str__(self):
        return self.item.name


class Parameter(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название')

    class Meta:
        verbose_name = 'Имя параметра'
        verbose_name_plural = "Список всех параметров"
        ordering = ('name',)

    def __str__(self):
        return self.name


class ItemParameter(models.Model):
    item = models.ForeignKey(ItemInfo, verbose_name='Информация о продукте', related_name='item_parameters',
                             blank=True, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, verbose_name='Параметр', related_name='product_parameters', blank=True,
                                  on_delete=models.CASCADE)
    value = models.CharField(verbose_name='Значение', max_length=100)

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = "Список параметров товаров"


class Picture(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='pictures')
    image = models.ImageField(upload_to='item_pictures', verbose_name='Изображение')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self) -> str:
        return self.car.name + str(self.id)


class Tag(models.Model):
    name = models.CharField(max_length=10, verbose_name="Название тега")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self) -> str:
        return str(self.name)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, verbose_name="Отзывы")
    stars = models.PositiveIntegerField(verbose_name='Рейтинг')
    text = models.CharField(max_length=200, null=True, verbose_name='Текст')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата отзыва')

    class Meta:
        verbose_name='Отзыв'
        verbose_name_plural='Отзывы'