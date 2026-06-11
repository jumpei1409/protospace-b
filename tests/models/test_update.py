from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from tests.factories.users import UserFactory
from tests.factories.prototypes import PrototypeFactory


class PrototypeUpdateViewTest(TestCase):

    def setUp(self):
        self.owner = UserFactory()
        self.other_user = UserFactory()
        self.prototype = PrototypeFactory(user=self.owner)
        self.url = reverse('Prototypes:update', kwargs={'pk': self.prototype.pk})

    # -------- アクセス制御 --------

    def test_未ログインでアクセスするとログインページへリダイレクトされる(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/users/sign_in/?next={self.url}')

    def test_自分のプロトタイプの編集ページにアクセスできる(self):
        self.client.force_login(self.owner)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_他人のプロトタイプの編集ページへアクセスするとトップページへリダイレクトされる(self):
        self.client.force_login(self.other_user)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('Prototypes:index'))

    # -------- GETリクエスト --------

    def test_編集ページを開くと既存のtitleがフォームに表示される(self):
        self.client.force_login(self.owner)
        response = self.client.get(self.url)
        self.assertContains(response, self.prototype.title)

    def test_編集ページを開くと既存のcatchphraseがフォームに表示される(self):
        self.client.force_login(self.owner)
        response = self.client.get(self.url)
        self.assertContains(response, self.prototype.catchphrase)

    def test_編集ページを開くと既存のconceptがフォームに表示される(self):
        self.client.force_login(self.owner)
        response = self.client.get(self.url)
        self.assertContains(response, self.prototype.concept)

    # -------- POSTリクエスト：成功 --------

    def test_正しいデータを送信するとプロトタイプが更新される(self):
        self.client.force_login(self.owner)
        image = SimpleUploadedFile('test.jpg', b'file_content', content_type='image/jpeg')
        self.client.post(self.url, {
            'title': '更新後タイトル',
            'catchphrase': '更新後キャッチコピー',
            'concept': '更新後コンセプト',
            'image': image,
        })
        self.prototype.refresh_from_db()
        self.assertEqual(self.prototype.title, '更新後タイトル')

    def test_正しいデータを送信すると詳細ページへリダイレクトされる(self):
        self.client.force_login(self.owner)
        image = SimpleUploadedFile('test.jpg', b'file_content', content_type='image/jpeg')
        response = self.client.post(self.url, {
            'title': '更新後タイトル',
            'catchphrase': '更新後キャッチコピー',
            'concept': '更新後コンセプト',
            'image': image,
        })
        self.assertRedirects(response, reverse('Prototypes:detail', kwargs={'pk': self.prototype.pk}))

    # -------- POSTリクエスト：失敗 --------

    def test_titleが空だと同じページに留まる(self):
        self.client.force_login(self.owner)
        response = self.client.post(self.url, {
            'title': '',
            'catchphrase': 'キャッチコピー',
            'concept': 'コンセプト',
        })
        self.assertEqual(response.status_code, 200)

    def test_catchphraseが空だと同じページに留まる(self):
        self.client.force_login(self.owner)
        response = self.client.post(self.url, {
            'title': 'タイトル',
            'catchphrase': '',
            'concept': 'コンセプト',
        })
        self.assertEqual(response.status_code, 200)

    def test_conceptが空だと同じページに留まる(self):
        self.client.force_login(self.owner)
        response = self.client.post(self.url, {
            'title': 'タイトル',
            'catchphrase': 'キャッチコピー',
            'concept': '',
        })
        self.assertEqual(response.status_code, 200)

    def test_バリデーション失敗後も入力済みの値がフォームに残る(self):
        self.client.force_login(self.owner)
        response = self.client.post(self.url, {
            'title': '入力済みタイトル',
            'catchphrase': '',  # 空にしてバリデーション失敗
            'concept': '入力済みコンセプト',
        })
        self.assertContains(response, '入力済みタイトル')
        self.assertContains(response, '入力済みコンセプト')

    # -------- 画像 --------

    def test_画像を選択せずに送信しても既存の画像が保持される(self):
        self.client.force_login(self.owner)
        original_image = self.prototype.image.name
        self.client.post(self.url, {
            'title': self.prototype.title,
            'catchphrase': self.prototype.catchphrase,
            'concept': self.prototype.concept,
            # imageは送信しない
        })
        self.prototype.refresh_from_db()
        self.assertEqual(self.prototype.image.name, original_image)