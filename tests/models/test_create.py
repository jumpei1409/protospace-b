from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from prototypes.models import Prototype
from django.contrib.auth import get_user_model

User = get_user_model()

class PrototypeCreateTest(TestCase):

  def setUp(self):
      self.client = Client()
      self.user = User.objects.create_user(
          email='test@example.com',
          nickname='testuser',
          password='testpass123',
          profile='test profile',
          affiliation='test affiliation',
          position='test position',
      )
      self.image = SimpleUploadedFile(
          name='test_image.jpg',
          content=b'\x47\x49\x46\x38\x39\x61',
          content_type='image/jpeg',
      )
      self.url = reverse('Prototypes:create')

  # 正常にプロトタイプが保存されること
  def test_create_prototype_success(self):
      self.client.login(username='test@example.com', password='testpass123')
      response = self.client.post(self.url, {
          'title': 'テストタイトル',
          'catchphrase': 'テストキャッチコピー',
          'concept': 'テストコンセプト',
          'image': self.image,
      })
      self.assertEqual(Prototype.objects.count(), 1)
      self.assertRedirects(response, reverse('Prototypes:index'))

  # タイトルが必須であること
  def test_title_required(self):
      self.client.login(username='test@example.com', password='testpass123')
      response = self.client.post(self.url, {
          'title': '',
          'catchphrase': 'テストキャッチコピー',
          'concept': 'テストコンセプト',
          'image': self.image,
      })
      self.assertEqual(Prototype.objects.count(), 0)
      self.assertEqual(response.status_code, 200)

  # キャッチコピーが必須であること
  def test_catchphrase_required(self):
      self.client.login(username='test@example.com', password='testpass123')
      response = self.client.post(self.url, {
          'title': 'テストタイトル',
          'catchphrase': '',
          'concept': 'テストコンセプト',
          'image': self.image,
      })
      self.assertEqual(Prototype.objects.count(), 0)
      self.assertEqual(response.status_code, 200)

  # コンセプトが必須であること
  def test_concept_required(self):
      self.client.login(username='test@example.com', password='testpass123')
      response = self.client.post(self.url, {
          'title': 'テストタイトル',
          'catchphrase': 'テストキャッチコピー',
          'concept': '',
          'image': self.image,
      })
      self.assertEqual(Prototype.objects.count(), 0)
      self.assertEqual(response.status_code, 200)

  # 画像が必須であること
  def test_image_required(self):
      self.client.login(username='test@example.com', password='testpass123')
      response = self.client.post(self.url, {
          'title': 'テストタイトル',
          'catchphrase': 'テストキャッチコピー',
          'concept': 'テストコンセプト',
      })
      self.assertEqual(Prototype.objects.count(), 0)
      self.assertEqual(response.status_code, 200)

  # ログインしていないとアクセスできないこと
  def test_login_required(self):
      response = self.client.get(self.url)
      self.assertRedirects(response, '/users/sign_in/?next=/create/')

  # ログアウト状態で投稿しようとするとログインページに遷移すること
  def test_logout_redirect(self):
      response = self.client.post(self.url, {
          'title': 'テストタイトル',
          'catchphrase': 'テストキャッチコピー',
          'concept': 'テストコンセプト',
          'image': self.image,
      })
      self.assertRedirects(response, '/users/sign_in/?next=/create/')