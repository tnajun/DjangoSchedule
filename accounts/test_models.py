from django.test import TestCase
from timeline.models import Post
from timeline.models import Posii
from accounts.models import CustomUser        
from tests.factories import PostModelFactory

class CustomUserModelTests(TestCase):

  def test_is_empty(self):
    """初期状態では何も登録されていないことをチェック"""  
    saved_CustomUser = CustomUser.objects.all()
    print('777')
    self.assertEqual(saved_CustomUser.count(), 0)


# class PostModelTests(TestCase):

#   def test_is_empty(self):
#     """初期状態では何も登録されていないことをチェック"""  
#     saved_posts = Post.objects.all()
#     print('hhh')
#     self.assertEqual(saved_posts.count(), 0)

#   def test_is_count_one(self):
#     """1つレコードを適当に作成すると、レコードが1つだけカウントされることをテスト"""
#     from factory.django import DjangoModelFactory
#     from accounts.models import CustomUser
#     from timeline.models import Post
#     from timeline.models import Posii
#     users = CustomUser.objects.all()
#     Posii_obj = Posii.objects.filter(post__author=users[0])
    
#     from faker import Faker 
#     fakegen = Faker('ja_JP') # Fakerのインスタンス作成、
#     fakegen.text()
#     fakegen.date_time().strftime("%Y/%m/%d %H:%M:%S")

#     # for n in range(10):
#     post_model = PostModelFactory(author=users[0], created_at=fakegen.date_time().strftime("%Y-%m-%d %H:%M:%S"), text=fakegen.text() )
#     saved_posts = Post.objects.all()
#     print('vvv')
#     self.assertEqual(saved_posts.count(), 1)