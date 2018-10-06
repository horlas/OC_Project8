from django.conf import settings
from django.db import models
# Create your models here.

class TimestamptedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        abstract = True



class SelectedProduct(models.Model):
    name =  models.CharField(max_length=100)
    url = models.URLField()
    img = models.URLField()
    n_grade = models.CharField(max_length=1)
    category = models.CharField(max_length=150)

    class Meta:
        verbose_name = "selected_product"

    def __str__(self):
        return self.name


class Backup(TimestamptedModel):
    selected_product_id = models.ForeignKey(SelectedProduct, on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "backup"

    def __str__(self):
        return str(self.id)



class SubstitutProduct(models.Model):
    name =  models.CharField(max_length=100)
    url = models.URLField()
    img = models.URLField()
    n_grade = models.CharField(max_length=1)
    category = models.CharField(max_length=150)
    backup_id = models.ForeignKey(Backup , on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
    )
    selected_product_id = models.ForeignKey(SelectedProduct, on_delete=models.CASCADE)


    class Meta:
        verbose_name = "substitut_product"

    def __str__(self):
        return self.name



