from django.test import TestCase
from datetime import datetime
# Create your tests here.
from .models import *

#  test categories class


class TestUser (TestCase):
    def setUp(self):
        self.manka = User(username='manka', password='akisijui')
        self.manka.save()

    def tearDown(self):
        User.objects.all().delete()

    def test_instance(self):
        self.assertEqual(self.manka.username, 'manka')
        self.assertEqual(self.manka.password, 'akisijui')
        self.assertTrue(isinstance(self.manka, User))


class TestUserProfile (TestCase):
    def setUp(self):

        self.manka = User(username='manka', password='akisijui')
        self.manka.save()
        self.lord_stark = Profile(user=self.manka, Bio='i care')
        self.lord_stark.save_profile()

    def tearDown(self):
        Profile.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.lord_stark, Profile))

    def test_save_profile(self):
        self.lord_stark.save_profile()
        self.assertTrue(len(Profile.objects.all()) > 0)


class TestPost (TestCase):
    def setUp(self):
        self.manka = User(username='manka', password='akisijui')
        self.manka.save()
        self.waterfall = Post(uploaded_by=self.manka, landing_image='test.jpg',
                              country='Kenya', post_date=datetime.utcnow())
        self.waterfall.save_post(self.manka)

    def tearDown(self):
        Post.objects.all().delete()

    def test_instance(self):
        self.assertEqual(self.waterfall.uploaded_by, self.manka)
        self.assertEqual(self.waterfall.landing_image, 'test.jpg')
        self.assertEqual(self.waterfall.country, 'Kenya')
        self.assertTrue(isinstance(self.waterfall, Post))

    def test_all_posts(self):
        self.assertTrue(len(Post.objects.all()) > 0)

   

class TestComment (TestCase):
    def setUp(self):

        self.manka = User(username='manka', password='akisijui')
        self.manka.save()
        self.comment = Comment(review='great')
        self.comment.save(self.manka)

    def tearDown(self):
        Comment.objects.all().delete()

    def test_save_comment(self):
        self.assertTrue(isinstance(self.comment, Comment))

    