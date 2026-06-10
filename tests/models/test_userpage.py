from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from tests.factories.users import UserFactory
from tests.factories.prototypes import PrototypeFactory

User = get_user_model()

class BaseUserPageViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.other_user = UserFactory.create()
        self.prototype = PrototypeFactory.create(user=self.user)
        self.other_prototype = PrototypeFactory.create(user=self.other_user)
        self.url = reverse('users:mypage', kwargs={'pk': self.user.pk})


class UserPageViewAccessTestCase(BaseUserPageViewTest):
    # ログインしていないユーザーでも詳細ページにアクセスできる
    def test_anonymous_user_can_access_user_detail_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    # ログインしているユーザーでも詳細ページにアクセスできる
    def test_logged_in_user_can_access_user_detail_page(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class UserPageViewUserInfoTestCase(BaseUserPageViewTest):
    def setUp(self):
        super().setUp()
        self.response = self.client.get(self.url)

    # 詳細ページに名前が表示されている
    def test_user_detail_page_shows_nickname(self):
        self.assertContains(self.response, self.user.nickname)

    # 詳細ページにプロフィールが表示されている
    def test_user_detail_page_shows_profile(self):
        self.assertContains(self.response, self.user.profile)

    # 詳細ページに所属が表示されている
    def test_user_detail_page_shows_affiliation(self):
        self.assertContains(self.response, self.user.affiliation)

    # 詳細ページに役職が表示されている
    def test_user_detail_page_shows_position(self):
        self.assertContains(self.response, self.user.position)


class UserPageViewPrototypeInfoTestCase(BaseUserPageViewTest):
    def setUp(self):
        super().setUp()
        self.response = self.client.get(self.url)

    # 詳細ページにそのユーザーのプロトタイプ名が表示されている
    def test_user_detail_page_shows_prototype_title(self):
        self.assertContains(self.response, self.prototype.title)

    # 詳細ページに投稿者名が表示されている
    def test_user_detail_page_shows_prototype_user(self):
        self.assertContains(self.response, self.prototype.user.nickname)

    # 詳細ページにキャッチコピーが表示されている
    def test_user_detail_page_shows_prototype_catchphrase(self):
        self.assertContains(self.response, self.prototype.catchphrase)

    # 詳細ページに画像のimgタグが存在する
    def test_user_detail_page_shows_prototype_image(self):
        self.assertContains(self.response, '<img')

    # 他のユーザーのプロトタイプは表示されない
    def test_user_detail_page_does_not_show_other_users_prototype(self):
        self.assertNotContains(self.response, self.other_prototype.title)