from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from django.contrib.auth import get_user_model
from ..factories.users import UserFactory

User = get_user_model()

class TestUser(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        service = Service(ChromeDriverManager().install())
        cls.driver = webdriver.Chrome(service=service)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        self.user = UserFactory.build()


class TestUserSignUpSuccessCase(TestUser):
    # 正しい情報を入力すればユーザー新規登録ができてトップページに移動する
    def test_user_can_signup_with_valid_information(self):
        self.driver.get(f"{self.live_server_url}/")

        # トップページに新規登録リンクがあることを確認
        signup_link = self.driver.find_element(By.LINK_TEXT, "新規登録")
        self.assertTrue(signup_link.is_displayed())

        # 新規登録ページへ移動
        self.driver.get(f"{self.live_server_url}/users/sign_up/")

        # ユーザー情報を入力
        self.driver.find_element(By.NAME, "email").send_keys(self.user.email)
        self.driver.find_element(By.NAME, "password1").send_keys(self.user.password)
        self.driver.find_element(By.NAME, "password2").send_keys(self.user.password)
        self.driver.find_element(By.NAME, "nickname").send_keys(self.user.nickname)
        self.driver.find_element(By.NAME, "profile").send_keys(self.user.profile)
        self.driver.find_element(By.NAME, "affiliation").send_keys(self.user.affiliation)
        self.driver.find_element(By.NAME, "position").send_keys(self.user.position)

        # 送信後にユーザー数が1増えることを確認
        user_count = User.objects.count()
        self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        self.assertEqual(User.objects.count(), user_count + 1)

        # トップページへ遷移することを確認
        WebDriverWait(self.driver, 10).until(
            EC.url_to_be(f"{self.live_server_url}/")
        )

        # ログアウトリンクが表示されることを確認
        logout_link = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.LINK_TEXT, "ログアウト"))
        )
        self.assertTrue(logout_link.is_displayed())

        # 新規登録・ログインリンクが表示されないことを確認
        with self.assertRaises(Exception):
            self.driver.find_element(By.LINK_TEXT, "新規登録")
        with self.assertRaises(Exception):
            self.driver.find_element(By.LINK_TEXT, "ログイン")


class TestUserSignUpFailureCase(TestUser):
    # 誤った情報ではユーザー新規登録ができずに新規登録ページへ戻る
    def test_user_cannot_signup_with_invalid_information(self):
        self.driver.get(f"{self.live_server_url}/users/sign_up/")

        # 全て空欄で送信
        self.driver.find_element(By.NAME, "email").send_keys("")
        self.driver.find_element(By.NAME, "password1").send_keys("")
        self.driver.find_element(By.NAME, "password2").send_keys("")
        self.driver.find_element(By.NAME, "nickname").send_keys("")
        self.driver.find_element(By.NAME, "profile").send_keys("")
        self.driver.find_element(By.NAME, "affiliation").send_keys("")
        self.driver.find_element(By.NAME, "position").send_keys("")

        # ユーザー数が増えないことを確認
        user_count = User.objects.count()
        self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        self.assertEqual(User.objects.count(), user_count)

        # 新規登録ページに留まることを確認
        self.assertIn("/users/sign_up/", self.driver.current_url)


class TestUserSignInSuccessCase(TestUser):
    # 正しい情報を入力すればログインができてトップページに移動する
    def test_user_can_signin_with_valid_information(self):
        # DBにユーザーを作成
        User.objects.create_user(
            email=self.user.email,
            nickname=self.user.nickname,
            password=self.user.password,
            profile=self.user.profile,
            affiliation=self.user.affiliation,
            position=self.user.position,
        )

        self.driver.get(f"{self.live_server_url}/")

        # トップページにログインリンクがあることを確認
        login_link = self.driver.find_element(By.LINK_TEXT, "ログイン")
        self.assertTrue(login_link.is_displayed())

        # ログインページへ移動
        self.driver.get(f"{self.live_server_url}/users/sign_in/")

        # ログイン情報を入力
        self.driver.find_element(By.NAME, "username").send_keys(self.user.email)
        self.driver.find_element(By.NAME, "password").send_keys(self.user.password)
        self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        # トップページへ遷移することを確認
        WebDriverWait(self.driver, 10).until(
            EC.url_to_be(f"{self.live_server_url}/")
        )

        # ログアウトリンクが表示されることを確認
        logout_link = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.LINK_TEXT, "ログアウト"))
        )
        self.assertTrue(logout_link.is_displayed())


class TestUserSignInFailureCase(TestUser):
    # 誤った情報ではログインできずにログインページへ戻る
    def test_user_cannot_signin_with_invalid_information(self):
        self.driver.get(f"{self.live_server_url}/users/sign_in/")

        # 空欄で送信
        self.driver.find_element(By.NAME, "username").send_keys("")
        self.driver.find_element(By.NAME, "password").send_keys("")
        self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        # ログインページに留まることを確認
        self.assertIn("/users/sign_in/", self.driver.current_url)