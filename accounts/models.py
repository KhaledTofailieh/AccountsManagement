from django.db import models


# model manager to get the active users.
class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=User.Status.ACTIVE)


# model manager to get all customers
class CustomersManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=User.Type.CUSTOMER)


# model manager to get all stuff
class StuffManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=User.Type.STUFF)


# user model.
class User(models.Model):
    # inner class(enum) that show user status.
    class Status(models.TextChoices):
        DISABLE = 'Di', 'Disabled'
        ACTIVE = 'Ac', 'Active'

    # inner class(enum) that show user types.
    class Type(models.TextChoices):
        ADMIN = 'Ad', 'Admin'
        CUSTOMER = 'Cu', 'Customer'
        STUFF = 'St', 'Stuff'

    # user properties
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    birth_date = models.DateField(null=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    last_login = models.DateTimeField(null=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.ACTIVE)

    type = models.CharField(max_length=2,
                            choices=Type.choices,
                            default=Type.CUSTOMER)

    # define the model managers.
    objects = models.Manager()
    active = ActiveManager()
    customers = CustomersManager()
    stuff = StuffManager()

    # specify the index and extraction order.
    class Meta:
        # order the extracted records by creation date in descending way.
        ordering = ['-created_at', 'first_name', 'last_name']
        indexes = [
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f'{self.first_name}  {self.last_name}, {self.email}'
