from django.db import models


class MenuItem(models.Model):
    name = models.CharField(max_length=50)
    level = models.PositiveIntegerField(default=0)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    def __str__(self):
        if self.parent is None:
            return self.name
        return f'{self.parent} -> {self.name}'

    def save(self, *args, **kwargs):
        if self.parent is not None:
            self.level = self.parent.level + 1
        super().save(*args, **kwargs)

    def get_url_from_level(self, current_level):
        if self.level > current_level:
            return f'{self.name}'
        return f'{"../" * (current_level - self.level + 1)}{self.name}'
