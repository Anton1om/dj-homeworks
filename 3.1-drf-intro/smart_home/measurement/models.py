from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=50, blank=False, verbose_name='Название')
    description = models.TextField(max_length=500, blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Датчик'
        verbose_name_plural = 'Датчики'

    def __str__(self):
        return self.name


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE,
                               related_name='measurements', verbose_name='Датчик')
    temperature = models.DecimalField(max_digits=3, decimal_places=1,
                                      null = False, verbose_name='Температура')
    image = models.ImageField(
        upload_to='measurements/',
        null=True,
        blank=True,
        verbose_name='Изображение',
    )
    created_at = models.DateTimeField(auto_now_add = True, verbose_name='Дата и время создания')
    updated_at = models.DateTimeField(auto_now  = True, verbose_name='Дата и время изменения')

    class Meta:
        verbose_name = 'Измерение'
        verbose_name_plural = 'Измерения'
        ordering = ['-updated_at']
