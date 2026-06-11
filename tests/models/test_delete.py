from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from prototypes.models import Prototype
from django.contrib.auth import get_user_model

User = get_user_model()

class PrototypeDeleteTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            nickname='testuser',
            password='testpass123',
            profile='test',
            affiliation='test',
            position='test',
        )
        self.other_user = User.objects.create_user(
            email='other@example.com',
            nickname='otheruser',
            password='testpass123',
            profile='test',
            affiliation='test',
            position='test',
        )
        self.image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61',
            content_type='image/jpeg',
        )
        self.prototype = Prototype.objects.create(
            title='テスト',
            catchphrase='テストキャッチ',
            concept='テストコンセプト',
            image=self.image,
            user=self.user,
        )
        self.url = reverse('Prototypes:delete', kwargs={'pk': self.prototype.pk})

    # 正常に削除できること
    def test_delete_success(self):
        self.client.login(username='test@example.com', password='testpass123')
        response = self.client.post(self.url)
        self.assertEqual(Prototype.objects.count(), 0)
        self.assertRedirects(response, reverse('Prototypes:index'))

    # ログインしていないと削除できないこと
    def test_delete_login_required(self):
        response = self.client.post(self.url)
        self.assertEqual(Prototype.objects.count(), 1)
        self.assertRedirects(response, '/users/sign_in/?next=' + self.url)

    # 他人のプロトタイプは削除できないこと（404になること）
    def test_delete_other_user(self):
        self.client.login(username='other@example.com', password='testpass123')
        response = self.client.post(self.url)
        self.assertEqual(Prototype.objects.count(), 1)
        self.assertEqual(response.status_code, 404)