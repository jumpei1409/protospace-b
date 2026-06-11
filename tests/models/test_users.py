from django.test import TestCase
from tests.factories.users import UserFactory   # 絶対インポート
from users.forms import CustomUserCreationForm  # 絶対インポート

class BaseFormTest(TestCase):
    def setUp(self):
        self.user = UserFactory.build()
        self.valid_data = {
            'email': self.user.email,
            'password1': self.user.password,
            'password2': self.user.password,
            'nickname': self.user.nickname,
            'profile': self.user.profile,
            'affiliation': self.user.affiliation,
            'position': self.user.position,
        }


class UserFormSuccessTestCase(BaseFormTest):
    # 正しい情報を入力するとフォームが有効になる
    def test_form_is_valid_with_valid_data(self):
        form = CustomUserCreationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())


class UserFormFailureTestCase(BaseFormTest):
    # メールアドレスが空だとフォームが無効になる
    def test_form_is_invalid_when_email_is_blank(self):
        self.valid_data['email'] = ''
        form = CustomUserCreationForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'], ['このフィールドは必須です。'])

    # メールアドレスに@がないとフォームが無効になる
    def test_form_is_invalid_when_email_has_no_at_symbol(self):
        self.valid_data['email'] = 'notanemail'
        form = CustomUserCreationForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'], ['有効なメールアドレスを入力してください。'])

    # メールアドレスが重複しているとフォームが無効になる
    def test_form_is_invalid_when_email_is_duplicate(self):
        UserFactory.create(
            email=self.user.email,
            profile=self.user.profile,
            affiliation=self.user.affiliation,
            position=self.user.position,
        )
        form = CustomUserCreationForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'], ['この Email を持った Custom user が既に存在します。'])

    # パスワードが空だとフォームが無効になる
    def test_form_is_invalid_when_password_is_blank(self):
        self.valid_data['password1'] = ''
        self.valid_data['password2'] = ''
        form = CustomUserCreationForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password1', form.errors)
        self.assertEqual(form.errors['password1'], ['このフィールドは必須です。'])

    # パスワードが6文字未満だとフォームが無効になる
    def test_form_is_invalid_when_password_is_too_short(self):
        self.valid_data['password1'] = 'qpw0z'
        self.valid_data['password2'] = 'qpw0z'
        form = CustomUserCreationForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertEqual(form.errors['password2'], ['このパスワードは短すぎます。最低 6 文字以上必要です。'])

    # パスワードと確認用パスワードが一致しないとフォームが無効になる
    def test_form_is_invalid_when_passwords_do_not_match(self):
        self.valid_data['password2'] = 'differentpassword'
        form = CustomUserCreationForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertEqual(form.errors['password2'], ['パスワードが一致しません'])

    # ユーザー名が空だとフォームが無効になる
    def test_form_is_invalid_when_nickname_is_blank(self):
        self.valid_data['nickname'] = ''
        form = CustomUserCreationForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nickname', form.errors)
        self.assertEqual(form.errors['nickname'], ['このフィールドは必須です。'])

    # プロフィールが空だとフォームが無効になる
    def test_form_is_invalid_when_profile_is_blank(self):
        self.valid_data['profile'] = ''
        form = CustomUserCreationForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('profile', form.errors)
        self.assertEqual(form.errors['profile'], ['このフィールドは必須です。'])

    # 所属が空だとフォームが無効になる
    def test_form_is_invalid_when_affiliation_is_blank(self):
        self.valid_data['affiliation'] = ''
        form = CustomUserCreationForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('affiliation', form.errors)
        self.assertEqual(form.errors['affiliation'], ['このフィールドは必須です。'])

    # 役職が空だとフォームが無効になる
    def test_form_is_invalid_when_position_is_blank(self):
        self.valid_data['position'] = ''
        form = CustomUserCreationForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('position', form.errors)
        self.assertEqual(form.errors['position'], ['このフィールドは必須です。'])