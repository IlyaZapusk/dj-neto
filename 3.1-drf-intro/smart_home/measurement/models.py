from django.db import models

class Sensor(models.Model):
    objects = None
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Measurement(models.Model):
    objects = None
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements')
    temperature = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='measurements/', null=True, blank=True)

    def __str__(self):
        return f"{self.sensor} - {self.temperature}"