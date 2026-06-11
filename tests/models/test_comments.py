from django.test import TestCase
from django.urls import reverse
from prototypes.models import Prototype
from users.models import CustomUser
from comments.models import Comment

class CommentCreateViewTest(TestCase): 
    def setUp(self):
         self.user = CustomUser.objects.create_user(
            email='test@test.com',
            nickname='テストユーザー',
            password='testpass123',
    )
         self.prototype = Prototype.objects.create(
            title='テストタイトル',
            catchphrase='テストテキスト',
            concept='テストコンセプト',
            user=self.user,
    )
         self.url = reverse('Comment:create', kwargs={'pk': self.prototype.pk})

# コメントがDBに保存されるか
    def test_comment_saved_to_db(self):
        self.client.force_login(self.user)
        self.client.post(self.url, {'text': 'テストコメント'})
        self.assertEqual(Comment.objects.count(), 1)

# 投稿後に詳細ページに遷移するか
    def test_redirect_after_comment(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, {'text': 'テストコメント'})
        self.assertRedirects(response, reverse('Prototypes:detail', kwargs={'pk': self.prototype.pk}))

# ログイン時だけフォームが表示されるか
    def test_form_shown_when_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('Prototypes:detail',kwargs={'pk': self.prototype.pk}))
        self.assertContains(response,'送信する')

# 未ログインはフォームが表示されないか
    def test_form_hidden_when_logged_out(self):
        response = self.client.get(reverse('Prototypes:detail', kwargs={'pk': self.prototype.pk}))
        self.assertNotContains(response, '送信する')
