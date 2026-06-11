from django.test import TestCase
from django.urls import reverse
from prototypes.models import Prototype
from users.models import CustomUser
from comments.models import Comment

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
            user=self.user,
            concept='テストコンセプト', 
        )
    def test_detail_accessible_without_login(self):
        response = self.client.get(reverse('Prototypes:detail', kwargs={'pk': self.prototype.pk}))
        self.assertEqual(response.status_code, 200)

    def test_prototype_info_displayed(self):
        response = self.client.get(reverse('Prototypes:detail', kwargs={'pk': self.prototype.pk}))
        self.assertContains(response, self.prototype.title)
        self.assertContains(response, self.prototype.catchphrase)
        self.assertContains(response, self.prototype.concept)
        self.assertContains(response, self.prototype.user.nickname)

    def test_edit_delete_buttons_shown_for_owner(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('Prototypes:detail', kwargs={'pk': self.prototype.pk}))
        self.assertContains(response, '編集する')
        self.assertContains(response, '削除する')

    def test_edit_delete_buttons_hidden_for_other_user(self):
        other_user = CustomUser.objects.create_user(
            email='other@test.com',
            nickname='他のユーザー',
            password='testpass123',
    )
        self.client.force_login(other_user)
        response = self.client.get(reverse('Prototypes:detail', kwargs={'pk': self.prototype.pk}))
        self.assertNotContains(response, '編集する')
        self.assertNotContains(response, '削除する')
        
    def test_edit_delete_buttons_hidden_when_logged_out(self):
        response = self.client.get(reverse('Prototypes:detail', kwargs={'pk': self.prototype.pk}))
        self.assertNotContains(response, '編集する')
        self.assertNotContains(response, '削除する')

    def test_comment_saved_to_db(self):
        self.client.force_login(self.user)
        self.client.post(reverse('Comment:create', kwargs={'pk': self.prototype.pk}),{'text': 'テストコメント'})
        self.assertEqual(Comment.objects.count(), 1)


    def test_redirect_after_comment(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('Comment:create', kwargs={'pk': self.prototype.pk}),{'text':'テストコメント'})

    def empty_comment_not_saved(self):
        self.client.force.login(self.user)
        self.client.post(reverse('Comment:create', kwags={'pk': self.prototype.pk}),{'text',''})
        self.assertEqual(Comment.objects.count(), 0)

    def test_comment_deleted_with_prototype(self):
        Comment.object.create(test='テストコメント', user=self.user, prototype=self.prototype)
        self.prototype.delete()
        self.assertEqual(Comment.objects.count(),0)