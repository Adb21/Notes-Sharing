from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class TestAuth(APITestCase):
    def setUp(self) -> None:
        user_data = [
            {
                "username": "test_user_01",
                "first_name": "John",
                "last_name": "Wick",
                "email": "johnwick@test.com",
                "password": "cB23ep$",
            },
            {
                "username": "test_user_02",
                "first_name": "Tony",
                "last_name": "Stark",
                "email": "tonystark@test.com",
                "password": "b4bha$&$",
            },
        ]
        self.user_01 = User.objects.create_user(**user_data[0])
        self.user_02 = User.objects.create_user(**user_data[1])

        self.notes_list_url = reverse("note-list")

        return super().setUp()

    def login_as_user(self, user):
        if user == 0:
            self.token = RefreshToken.for_user(self.user_01)
        else:
            self.token = RefreshToken.for_user(self.user_02)

        self.access_token = str(self.token.access_token)

        # Using the access token in the HTTP Authorization header
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)

    def test_01_notes_crud(self):
        self.login_as_user(0)

        note_create_data = [
            {
                "title": "Office ToDo",
                "content": "check emails, code review, bug fixing",
            },
            {
                "title": "Home ToDo",
                "content": "gym, cook, sleep",
            },
        ]

        # Create Note Test
        for note in note_create_data:
            resp = self.client.post(self.notes_list_url, note)
            response = resp.json()
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response["title"], note["title"])

        # Get list Test
        resp = self.client.get(self.notes_list_url)
        list_response = resp.json()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(list_response["count"], 2)

        # Retirve Note Test
        note_detail_url = reverse(
            "note-detail", kwargs={"pk": list_response["results"][0]["id"]}
        )
        resp = self.client.get(note_detail_url)
        note_response = resp.json()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(note_response["id"], list_response["results"][0]["id"])

        # Update Note Test
        update_data = {
            "title": "Home ToDo List",
            "content": "gaming, cooking ,sleeping",
        }
        resp = self.client.put(note_detail_url, update_data)
        note_response = resp.json()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(note_response["id"], list_response["results"][0]["id"])
        self.assertEqual(note_response["title"], update_data["title"])
        self.assertEqual(note_response["content"], update_data["content"])

        # Delete Note Test
        resp = self.client.delete(note_detail_url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_02_notes_sharing(self):
        self.login_as_user(0)

        note_create_data = [
            {
                "title": "Office ToDo",
                "content": "check emails, code review, bug fixing",
            },
            {
                "title": "Home ToDo",
                "content": "gym, cook, sleep",
            },
        ]

        # Create Note Test
        for note in note_create_data:
            resp = self.client.post(self.notes_list_url, note)
            response = resp.json()
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response["title"], note["title"])

        # Get list Test
        resp = self.client.get(self.notes_list_url)
        list_response = resp.json()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(list_response["count"], 2)

        # Note Sharing
        note_sharing_url = reverse(
            "note-share", kwargs={"id": list_response["results"][0]["id"]}
        )
        resp = self.client.get(note_sharing_url)
        share_response = resp.json()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("sharable_id", share_response)
        sharable_id = share_response["sharable_id"]

        # View Sharable Note from User 2
        self.login_as_user(1)

        # Retirve Note Test
        note_detail_url = self.notes_list_url + f"?uid={sharable_id}"
        resp = self.client.get(note_detail_url)
        note_response = resp.json()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(note_response["title"], list_response["results"][0]["title"])
