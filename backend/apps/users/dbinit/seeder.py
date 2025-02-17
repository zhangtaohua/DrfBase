import hashlib
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()
from faker import Faker
from ..models import Users


def generate_data(num_users):
  fake = Faker('zh_CN')
  for _ in range(num_users):
    user_name = fake.user_name()
    name = fake.name()
    email = fake.email()
    mobile = fake.phone_number()
    password = 'test123456'
    print(f'生成中:用户名:{user_name},姓名:{name},电话:{mobile}')
    user = Users.objects.create(username=user_name, name=name, email=email, mobile=mobile)
    user.set_password(hashlib.md5(password.encode()).hexdigest())
    user.save()


if __name__ == '__main__':
  generate_data(100)