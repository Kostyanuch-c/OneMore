from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    @property
    def full_name(self) -> str:
        """Returns the user full name."""
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.username

    class Meta:
        ordering = ['id']
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
