from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

# create user (staff/admin)
class UserManager(BaseUserManager):
    
    #buat bikin user biasa (Staff)
    def create_user(self, username, nama, role, password=None):
        if not username:
            raise ValueError('Harus ada username!') # Validasi
        
        # bikin objek user
        user = self.model(
            username=username,
            nama=nama, 
            role=role
        )
        
        # pw hash
        user.set_password(password)
        
        # save
        user.save(using=self._db)
        return user

    # buat bikin superuser (admin)
    def create_superuser(self, username, nama, role, password=None):
        user = self.create_user(
            username=username,
            nama=nama,
            role=role,
            password=password,
        )

        user.is_staff = True
        user.is_superuser = True
        
        user.save(using=self._db)
        return user

# table staff
class UserModel(AbstractBaseUser, PermissionsMixin):

    # pilih role
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrator'
        STAFF = 'STAFF', 'Staff Front Office'

    username = models.CharField(max_length=50, unique=True, db_column='username')
    nama = models.CharField(max_length=100, verbose_name='Nama')
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STAFF, db_column='role')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # Kalo true baru bisa masuk admin
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nama', 'role']

    class Meta:
        db_table = 'staff'
        verbose_name = 'Staff'
        verbose_name_plural = 'Daftar Staff'
    
    def __str__(self):
        return f"{self.nama} ({self.role})"