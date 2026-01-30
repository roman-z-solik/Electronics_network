from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название продукта')
    model = models.CharField(max_length=255, verbose_name='Модель')
    release_date = models.DateField(verbose_name='Дата выхода на рынок')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f"{self.name} ({self.model})"


class NetworkNode(models.Model):
    FACTORY = 0
    RETAIL_NETWORK = 1
    INDIVIDUAL_ENTREPRENEUR = 2

    NODE_TYPE_CHOICES = [
        (FACTORY, 'Завод'),
        (RETAIL_NETWORK, 'Розничная сеть'),
        (INDIVIDUAL_ENTREPRENEUR, 'Индивидуальный предприниматель'),
    ]

    name = models.CharField(max_length=255, verbose_name='Название звена')
    node_type = models.IntegerField(choices=NODE_TYPE_CHOICES, verbose_name='Тип звена')

    email = models.EmailField(verbose_name='Email')
    country = models.CharField(max_length=100, verbose_name='Страна')
    city = models.CharField(max_length=100, verbose_name='Город')
    street = models.CharField(max_length=255, verbose_name='Улица')
    house_number = models.CharField(max_length=20, verbose_name='Номер дома')

    products = models.ManyToManyField(Product, related_name='network_nodes', verbose_name='Продукты')

    supplier = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='supplied_to',
        verbose_name='Поставщик'
    )

    debt = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name='Задолженность перед поставщиком'
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    class Meta:
        verbose_name = 'Звено сети'
        verbose_name_plural = 'Звенья сети'

    def __str__(self):
        return self.name

    @property
    def level(self):
        if self.supplier is None:
            return 0
        return self.supplier.level + 1
