from django.test import TestCase
from django.urls import reverse
from django.test.client import Client
from urlshorten.models import UrlMapper

# Create your tests here.


class CreateAPIViewShortenerTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.create_url = reverse('urlshorten:url_create')

        cls.valid_mapper_url = "https://www.django-rest-framework.org/"
        cls.i_valid_data = {
            'url': cls.valid_mapper_url,
        }

        cls.invalid_mapper_url = "some invalid string"
        cls.i_invalid_data = {
            'full_url': cls.invalid_mapper_url,
        }
        return super().setUpTestData()

    def setUp(self) -> None:
        self.client = Client()

        return super().setUp()

    def test_createapiview_get_405(self):
        """
        Test the 405 response status code, when calling a GET on the CreateAPIView.
        """
        response_of_get = self.client.get(self.create_url)
        self.assertEqual(response_of_get.status_code, 405)

    def test_createapiview_create_valid_url(self):
        """
        Test the creation of a URLMapper and the status code, using valid data.
        """
        response_of_post = self.client.post(self.create_url, data=self.i_valid_data)

        self.assertEqual(response_of_post.status_code, 200)

    def test_createapiview_create_invalid_url(self):
        """
        Test the CreateAPIView, using invalid URL string.
        """
        response_of_post = self.client.post(self.create_url, data=self.i_invalid_data)

        self.assertEqual(response_of_post.status_code, 400)


class RedirectViewUrlTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.create_url = reverse('urlshorten:url_create')
        cls.valid_mapper_url = "https://www.django-rest-framework.org/"
        cls.i_valid_data = {
            'url': cls.valid_mapper_url,
        }

        #
        return super().setUpTestData()

    def setUp(self) -> None:
        self.client = Client()
        self.obj = UrlMapper.objects.create(**self.i_valid_data)

        return super().setUp()

    def test_redirect_url(self):
        """
        Test the correct redirect process, using a valid short path.
        """

        redirect_url = reverse("urlshorten:url_redirect", args={self.obj.short_path})
        response_of_get = self.client.get(redirect_url[:-1])
        self.assertRedirects(response_of_get, response_of_get.url, 301, 301)

        response_of_get = self.client.get(response_of_get.url)
        self.assertRedirects(response_of_get, response_of_get.url, 301, 200, fetch_redirect_response=False)
        self.assertEquals(self.valid_mapper_url, response_of_get.url)

    def test_increment_counter(self):
        """
        Test increment only once
        """

        redirect_url = reverse("urlshorten:url_redirect", args={self.obj.short_path})
        response_of_get = self.client.get(redirect_url[:-1])
        self.assertRedirects(response_of_get, response_of_get.url, 301, 301)

        self.obj.refresh_from_db()
        print(f'test_increment_counter: {self.obj.hits}')

        response_of_get = self.client.get(response_of_get.url)
        self.assertRedirects(response_of_get, response_of_get.url, 301, 200, fetch_redirect_response=False)
        self.assertEquals(self.valid_mapper_url, response_of_get.url)

        self.obj.refresh_from_db()
        print(f'test_increment_counter: {self.obj.hits}')

        response_of_get = self.client.get(redirect_url[:-1], follow=True)

        self.obj.refresh_from_db()
        print(f'test_increment_counter: {self.obj.hits}')

    def test_redirect_non_existing_url(self):
        """
        Test the process of an invalid short path as input.
        """

        obj = UrlMapper.objects.create(**self.i_valid_data)

        # Hard Coded, because we know that it is Base64 and invalid.
        base_64_of_2 = "Ag=="

        redirect_url = reverse("urlshorten:url_redirect", args={base_64_of_2})
        response_of_get = self.client.get(redirect_url[:-1], follow=True)
        self.assertEquals(response_of_get.status_code, 404)
