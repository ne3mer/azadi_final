from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number, email, name, password):
        if not phone_number:
            raise ValueError('شماره موبایل وارد نشده است')
        if not email:
            raise ValueError('ایمیل وارد نشده است')
        if not name:
            raise ValueError('نام کاربر وارد نشده است')

        user = self.model(phone_number=phone_number, email=self.normalize_email(email), name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, name, password):
        user = self.create_user(phone_number, email, name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user
