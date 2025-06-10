from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone, password, email=None, first_name=None, last_name=None, gender='male', age=None,
                    marital='unknown'):
        if not phone:
            raise ValueError('User must have Phone')

        user = self.model(phone=phone, email=self.normalize_email(email), first_name=first_name, gender=gender,
                          last_name=last_name, age=age, marital=marital)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password, email=None, first_name=None, last_name=None, gender='male', age=None,
                         marital='unknown'):
        user = self.create_user(phone, password, email, first_name, last_name, gender, age, marital)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
