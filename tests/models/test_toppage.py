from django.test import TestCase
from django.urls import reverse
from prototypes.models import Prototype
from users.models import CustomUser
from django.core.files.uploadedfile import SimpleUploadedFile

class IndexViewTest(TestCase):

    def setUp(self):
        #テストユーザーを作成
        self.user = CustomUser.objects.create_user(
            email='test@test.com',
            nickname='テストユーザー',
            password='testpass123',
        )
        #テスト用プロトタイプを作成
        self.prototype = Prototype.objects.create(
            title='テストタイトル',
            catchphrase='テストテキスト',
            concept='テストコンセプト',
            user=self.user,
            image=SimpleUploadedFile('test.png', b'file_content', content_type='image/png')
        )
        #ログイン不要でアクセスできるか
    def test_index_accessible_without_login(self):
        response = self.client.get(reverse('Prototypes:index'))
        self.assertEqual(response.status_code, 200)

        #正しいテンプレートが使われているか
    def test_uses_correct_template(self):
        response = self.client.get(reverse('Prototypes:index'))
        self.assertTemplateUsed(response, 'prototypes/index.html')

        #プロトタイプ一覧がcontextに渡されているか
    def test_prototype_info_context(self):
        response = self.client.get(reverse('Prototypes:index'))
        self.assertIn('prototypes', response.context)

         # 4つの情報が表示されているか
    def test_prototype_info_displayed(self):
        response = self.client.get(reverse('Prototypes:index'))
        self.assertContains(response, self.prototype.title)  
        self.assertContains(response, self.prototype.catchphrase)  
        self.assertContains(response, self.prototype.user.nickname)  

    # 画像URLが存在するか
    def test_image_url_is_valid(self):
        self.assertTrue(self.prototype.image)  
