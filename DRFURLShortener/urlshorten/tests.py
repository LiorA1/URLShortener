from django.test import TestCase
from django.urls import reverse
from django.test.client import Client
from urlshorten.models import UrlMapper

from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient


# Create your tests here.


class CreateAPIViewShortenerTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.create_url = reverse("urlshorten:url_create")

        cls.valid_mapper_url = "https://www.django-rest-framework.org/"
        cls.i_valid_data = {
            "url": cls.valid_mapper_url,
        }

        cls.invalid_mapper_url = "some invalid string"
        cls.i_invalid_data = {
            "full_url": cls.invalid_mapper_url,
        }
        return super().setUpTestData()

    def setUp(self) -> None:
        self.client = APIClient()

        return super().setUp()

    def test_createapiview_get_200(self):
        """
        Test the 200 response status code, when calling a GET on the CreateAPIView.
        returns empty required fields.
        """
        response_of_get = self.client.get(self.create_url)

        self.assertEqual(response_of_get.status_code, 200)
        self.assertJSONEqual(
            str(response_of_get.content, encoding="utf8"), {"url": "", "short_path": ""}
        )

    def test_createapiview_create_valid_url(self):
        """
        Test the creation of a URLMapper and the status code, using valid data.
        """
        response_of_post = self.client.post(
            self.create_url, data=self.i_valid_data, format="json"
        )
        self.assertEqual(response_of_post.status_code, 201)

    def test_createapiview_create_invalid_url(self):
        """
        Test the CreateAPIView, using invalid URL string.
        """
        response_of_post = self.client.post(self.create_url, data=self.i_invalid_data)

        self.assertEqual(response_of_post.status_code, 400)


class RedirectViewUrlTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.create_url = reverse("urlshorten:url_create")

        cls.valid_mapper_url = "https://www.django-rest-framework.org/"
        cls.i_valid_data = {
            "url": cls.valid_mapper_url,
        }

        #
        return super().setUpTestData()

    def setUp(self) -> None:
        self.client = APIClient()
        response_of_post = self.client.post(
            self.create_url, self.i_valid_data, format="json"
        )
        self.obj = UrlMapper.objects.first()

        return super().setUp()

    def test_redirect_url(self):
        """
        Test the correct redirect process, using a valid short path.
        """

        redirect_url = reverse("urlshorten:url_redirect", args={self.obj.short_path})
        response_of_get = self.client.get(redirect_url)
        self.assertRedirects(
            response_of_get,
            response_of_get.url,
            301,
            301,
            fetch_redirect_response=False,
        )

    def test_increment_counter(self):
        """
        Test increment only once feature
        """
        self.assertEqual(self.obj.hits, 0)
        # hits are 0, because no one tried to access yet.

        redirect_url = reverse("urlshorten:url_redirect", args={self.obj.short_path})
        response_of_get = self.client.get(redirect_url)
        self.assertRedirects(
            response_of_get,
            response_of_get.url,
            301,
            301,
            fetch_redirect_response=False,
        )

        self.obj.refresh_from_db()
        self.assertEqual(self.obj.hits, 1)
        # hits are 1, one tried to access.

        response_of_get = self.client.get(redirect_url)
        self.assertRedirects(
            response_of_get,
            response_of_get.url,
            301,
            200,
            fetch_redirect_response=False,
        )
        self.assertEquals(self.valid_mapper_url, response_of_get.url)

        self.obj.refresh_from_db()
        self.assertEqual(self.obj.hits, 2)
        # hits are 2, one tried to access.

        response_of_get = self.client.get(redirect_url)

        self.obj.refresh_from_db()
        self.assertEqual(self.obj.hits, 3)
        # hits are 2, one tried to access.

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
