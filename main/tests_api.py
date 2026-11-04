from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from main.models import Experience


class ExperienceAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.editor_group = Group.objects.create(name="Editor")
        self.editor = User.objects.create_user(
            username="editor", password="editor-password"
        )
        self.editor.groups.add(self.editor_group)
        self.visitor = User.objects.create_user(
            username="visitor", password="visitor-password"
        )
        self.experience = Experience.objects.create(
            title="Asisten Dosen",
            description="Mengajar pengembangan web.",
            category="part-time",
        )
        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse(
            "api:experience-detail", args=[self.experience.id]
        )
        self.star_url = reverse(
            "api:experience-star", args=[self.experience.id]
        )

    def test_list_is_public_and_returns_serializer_fields(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["id"], str(self.experience.id))
        self.assertEqual(response.data[0]["title"], self.experience.title)
        self.assertNotIn("fields", response.data[0])
        self.assertFalse(response.data[0]["is_starred"])

    def test_list_can_filter_by_title(self):
        Experience.objects.create(
            title="Peneliti",
            description="Riset.",
            category="research",
        )

        response = self.client.get(self.list_url, {"title": "peneliti"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Peneliti")

    def test_editor_can_create_experience(self):
        self.client.force_authenticate(user=self.editor)

        response = self.client.post(
            self.list_url,
            {
                "title": "  <b>Developer</b>  ",
                "description": "Membangun aplikasi.",
                "category": "full-time",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], "Developer")
        self.assertTrue(Experience.objects.filter(title="Developer").exists())

    def test_editor_cannot_create_experience_with_empty_title(self):
        self.client.force_authenticate(user=self.editor)

        response = self.client.post(
            self.list_url,
            {
                "title": "<b> </b>",
                "description": "Deskripsi.",
                "category": "full-time",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Experience.objects.count(), 1)
        self.assertIn("title", response.data)

    def test_session_write_requires_csrf_token(self):
        client = APIClient(enforce_csrf_checks=True)
        client.force_login(self.editor)
        payload = {
            "title": "Developer",
            "description": "Membangun aplikasi.",
            "category": "full-time",
        }

        rejected_response = client.post(
            self.list_url, payload, format="json"
        )
        self.assertEqual(rejected_response.status_code, 403)

        client.get(reverse("main:show_experience"))
        csrf_token = client.cookies["csrftoken"].value
        accepted_response = client.post(
            self.list_url,
            payload,
            format="json",
            HTTP_X_CSRFTOKEN=csrf_token,
        )

        self.assertEqual(accepted_response.status_code, 201)

    def test_regular_user_cannot_create_or_update_experience(self):
        self.client.force_authenticate(user=self.visitor)

        create_response = self.client.post(
            self.list_url,
            {
                "title": "Tidak diizinkan",
                "description": "Deskripsi.",
                "category": "full-time",
            },
            format="json",
        )
        update_response = self.client.patch(
            self.detail_url, {"title": "Diubah"}, format="json"
        )

        self.assertEqual(create_response.status_code, 403)
        self.assertEqual(update_response.status_code, 403)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Asisten Dosen")

    def test_detail_and_patch(self):
        self.client.force_authenticate(user=self.editor)

        detail_response = self.client.get(self.detail_url)
        update_response = self.client.patch(
            self.detail_url, {"title": "<i>Pengajar</i>"}, format="json"
        )

        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(detail_response.data["id"], str(self.experience.id))
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.data["title"], "Pengajar")
        self.experience.refresh_from_db()
        self.assertEqual(
            self.experience.description, "Mengajar pengembangan web."
        )

    def test_editor_can_delete_experience(self):
        self.client.force_authenticate(user=self.editor)

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            Experience.objects.filter(pk=self.experience.pk).exists()
        )

    def test_missing_experience_returns_404(self):
        self.client.force_authenticate(user=self.editor)
        missing_url = reverse(
            "api:experience-detail",
            args=["00000000-0000-0000-0000-000000000000"],
        )

        response = self.client.get(missing_url)

        self.assertEqual(response.status_code, 404)

    def test_authenticated_non_editor_can_toggle_star(self):
        self.client.force_authenticate(user=self.visitor)

        first_response = self.client.post(self.star_url)
        second_response = self.client.post(self.star_url)

        self.assertEqual(first_response.status_code, 200)
        self.assertTrue(first_response.data["is_starred"])
        self.assertEqual(first_response.data["star_count"], 1)
        self.assertEqual(second_response.status_code, 200)
        self.assertFalse(second_response.data["is_starred"])
        self.assertEqual(second_response.data["star_count"], 0)

    def test_anonymous_user_cannot_star(self):
        response = self.client.post(self.star_url)

        self.assertEqual(response.status_code, 403)
        self.assertFalse(self.experience.starred_by.exists())

    def test_star_endpoint_only_accepts_post(self):
        self.client.force_authenticate(user=self.visitor)

        response = self.client.get(self.star_url)

        self.assertEqual(response.status_code, 405)
