from django.test import TestCase
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.factories.users import UserFactory
from tests.factories.prototypes import PrototypeFactory
import time


class PrototypeUpdateIntegrationTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        self.owner = UserFactory()
        self.owner.set_password('testpassword')
        self.owner.save()
        self.other_user = UserFactory()
        self.other_user.set_password('testpassword')
        self.other_user.save()
        self.prototype = PrototypeFactory(user=self.owner)

    def ログイン(self, user):
        self.driver.get(self.live_server_url + reverse('users:sign_in'))
        self.driver.find_element(By.NAME, 'username').send_keys(user.email)
        self.driver.find_element(By.NAME, 'password').send_keys('testpassword')
        self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

    def 編集ページへ移動(self):
        url = self.live_server_url + reverse('Prototypes:update', kwargs={'pk': self.prototype.pk})
        self.driver.get(url)

    # -------- アクセス制御 --------

    def test_未ログインでアクセスするとログインページへリダイレクトされる(self):
        self.編集ページへ移動()
        self.assertIn('sign_in', self.driver.current_url)

    def test_自分のプロトタイプの編集ページにアクセスできる(self):
        self.ログイン(self.owner)
        self.編集ページへ移動()
        self.assertIn('update', self.driver.current_url)

    def test_他人のプロトタイプの編集ページへアクセスするとトップページへリダイレクトされる(self):
        self.ログイン(self.other_user)
        self.編集ページへ移動()
        self.assertEqual(self.driver.current_url, self.live_server_url + '/')

    # -------- 見た目の確認 --------

    def test_編集ページにフォームの各項目が表示される(self):
        self.ログイン(self.owner)
        self.編集ページへ移動()
        self.assertTrue(self.driver.find_element(By.NAME, 'title').is_displayed())
        self.assertTrue(self.driver.find_element(By.NAME, 'catchphrase').is_displayed())
        self.assertTrue(self.driver.find_element(By.NAME, 'concept').is_displayed())
        self.assertTrue(self.driver.find_element(By.NAME, 'image').is_displayed())
        self.assertTrue(self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').is_displayed())

    def test_編集ページを開くと既存の値がフォームに表示される(self):
        self.ログイン(self.owner)
        self.編集ページへ移動()
        title_value = self.driver.find_element(By.NAME, 'title').get_attribute('value')
        catchphrase_value = self.driver.find_element(By.NAME, 'catchphrase').text
        concept_value = self.driver.find_element(By.NAME, 'concept').text
        self.assertEqual(title_value, self.prototype.title)
        self.assertIn(self.prototype.catchphrase, catchphrase_value)
        self.assertIn(self.prototype.concept, concept_value)

    # -------- POSTリクエスト：成功 --------

    def test_正しいデータを送信すると詳細ページへ遷移する(self):
        self.ログイン(self.owner)
        self.編集ページへ移動()
        title_input = self.driver.find_element(By.NAME, 'title')
        title_input.clear()
        title_input.send_keys('更新後タイトル')
        self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
        self.assertIn('prototypes', self.driver.current_url)
        self.assertNotIn('update', self.driver.current_url)

    # -------- POSTリクエスト：失敗 --------

    def test_titleを空にして送信すると同じページに留まる(self):
        self.ログイン(self.owner)
        self.編集ページへ移動()
        title_input = self.driver.find_element(By.NAME, 'title')
        title_input.clear()
        self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
        self.assertIn('update', self.driver.current_url)

    def test_バリデーション失敗後も入力済みの値がフォームに残る(self):
        self.ログイン(self.owner)
        self.編集ページへ移動()
        title_input = self.driver.find_element(By.NAME, 'title')
        title_input.clear()
        title_input.send_keys('入力済みタイトル')
        catchphrase_input = self.driver.find_element(By.NAME, 'catchphrase')
        catchphrase_input.clear()  # 空にしてバリデーション失敗させる
        self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
        title_value = self.driver.find_element(By.NAME, 'title').get_attribute('value')
        self.assertEqual(title_value, '入力済みタイトル')