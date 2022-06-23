from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models

klass_names = [
    ('0_lite', 'Лайт'),
    ('1_hobby', 'Хобби'),
    ('2_expert', 'Эксперт'),
]


class Reg(models.Model):
    competition = models.CharField("соревнование", choices=[
        ('last_attack_heat_2022', 'Last Attack Heat 2022'),
    ], default='last_attack_heat_2022', max_length=200)
    fio = models.CharField("фамилия Имя", max_length=200, validators=[
        MinLengthValidator(2)
    ])
    phone = models.CharField("контактный телефон", max_length=200, unique=True, validators=[
        MinLengthValidator(10)
    ])
    number = models.CharField("стартовый номер участника", max_length=3, unique=True, validators=[
        MinLengthValidator(1),
        RegexValidator(r'\d+', message="Только цифры")
    ])
    klass = models.CharField("класс участия", choices=klass_names, max_length=20)
    city = models.CharField("город", max_length=200, blank=True, default='')
    team = models.CharField("комманда", max_length=200, blank=True, default='')
    bike = models.CharField("модель мотоцикла", max_length=200, blank=True, default='')
    
    paid = models.BooleanField("оплачено", default=False, null=False)
    created = models.DateTimeField("дата регистрации", auto_now_add=True)
    
    def __str__(self):
        return self.fio

    class Meta:
        verbose_name = "Регистрация"
        verbose_name_plural = "Регистрации"