from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from main.models import Experience


class ExperienceAPITest(APITestCase):
    def setUp(self):
        self.editor_password = "editor-test-password"
        self.owner_password = "owner-test-password"
        self.editor_group = Group.objects.create(name="Editor")
        self.editor = User.objects.create_user(
            username="editor",
            email="editor@example.com",
            password=self.editor_password,
        )
        self.editor.groups.add(self.editor_group)
        self.visitor = User.objects.create_user(
            username="visitor",
            email="visitor@example.com",
            password="visitor-test-password",
        )
        self.owner = User.objects.create_superuser(
            username="owner",
            email="owner@example.com",
            password=self.owner_password,
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

    def payload(self, **overrides):
        data = {
            "title": "Developer",
            "description": "Membangun aplikasi.",
            "category": "full-time",
        }
        data.update(overrides)
        return data

    def test_list_is_public_and_omits_account_data(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        item = response.data[0]
        self.assertEqual(item["id"], str(self.experience.id))
        self.assertEqual(item["title"], self.experience.title)
        self.assertEqual(item["star_count"], 0)
        self.assertFalse(item["is_starred"])
        self.assertNotIn("fields", item)
        self.assertNotIn("email", item)
        self.assertNotIn("password", item)
        self.assertNotIn("starred_by_names", item)

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

    def test_anonymous_visitor_cannot_write(self):
        initial_count = Experience.objects.count()

        create_response = self.client.post(
            self.list_url, self.payload(), format="json"
        )
        delete_response = self.client.delete(self.detail_url)

        self.assertEqual(create_response.status_code, 403)
        self.assertEqual(delete_response.status_code, 403)
        self.assertEqual(Experience.objects.count(), initial_count)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Asisten Dosen")

    def test_regular_user_cannot_create_update_or_delete(self):
        self.client.force_authenticate(user=self.visitor)
        initial_count = Experience.objects.count()

        create_response = self.client.post(
            self.list_url, self.payload(), format="json"
        )
        update_response = self.client.patch(
            self.detail_url, {"title": "Diubah"}, format="json"
        )
        delete_response = self.client.delete(self.detail_url)

        self.assertEqual(create_response.status_code, 403)
        self.assertEqual(update_response.status_code, 403)
        self.assertEqual(delete_response.status_code, 403)
        self.assertEqual(Experience.objects.count(), initial_count)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Asisten Dosen")

    def test_editor_can_patch_but_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        initial_count = Experience.objects.count()

        update_response = self.client.patch(
            self.detail_url, {"title": "<i>Pengajar</i>"}, format="json"
        )
        create_response = self.client.post(
            self.list_url, self.payload(), format="json"
        )
        delete_response = self.client.delete(self.detail_url)

        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.data["title"], "Pengajar")
        self.assertEqual(create_response.status_code, 403)
        self.assertEqual(delete_response.status_code, 403)
        self.assertEqual(Experience.objects.count(), initial_count)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Pengajar")
        self.assertEqual(
            self.experience.description, "Mengajar pengembangan web."
        )

    def test_owner_can_create_and_delete(self):
        self.client.force_authenticate(user=self.owner)

        create_response = self.client.post(
            self.list_url,
            self.payload(title="  <b>Developer</b>  "),
            format="json",
        )

        self.assertEqual(create_response.status_code, 201)
        self.assertEqual(create_response.data["title"], "Developer")
        created_id = create_response.data["id"]
        self.assertTrue(Experience.objects.filter(pk=created_id).exists())
        self.assertEqual(Experience.objects.count(), 2)

        delete_response = self.client.delete(
            reverse("api:experience-detail", args=[created_id])
        )

        self.assertEqual(delete_response.status_code, 204)
        self.assertFalse(Experience.objects.filter(pk=created_id).exists())
        self.assertEqual(Experience.objects.count(), 1)

    def test_invalid_text_is_rejected_without_database_changes(self):
        self.client.force_authenticate(user=self.owner)
        initial_count = Experience.objects.count()

        response = self.client.post(
            self.list_url,
            self.payload(title="<b> </b>", description="<i></i>"),
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.data)
        self.assertIn("description", response.data)
        self.assertEqual(Experience.objects.count(), initial_count)

    def test_owner_can_replace_detail_with_put(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.put(
            self.detail_url,
            self.payload(title="Dosen", description="Mengajar."),
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Dosen")
        self.assertEqual(self.experience.description, "Mengajar.")

    def test_missing_experience_returns_404(self):
        self.client.force_authenticate(user=self.owner)
        missing_url = reverse(
            "api:experience-detail",
            args=["00000000-0000-0000-0000-000000000000"],
        )

        response = self.client.get(missing_url)

        self.assertEqual(response.status_code, 404)

    def test_logged_in_user_can_toggle_own_star(self):
        self.client.force_authenticate(user=self.visitor)

        first_response = self.client.post(self.star_url)

        self.assertEqual(first_response.status_code, 200)
        self.assertTrue(first_response.data["is_starred"])
        self.assertEqual(first_response.data["star_count"], 1)
        self.assertTrue(
            self.experience.starred_by.filter(pk=self.visitor.pk).exists()
        )

        second_response = self.client.post(self.star_url)

        self.assertEqual(second_response.status_code, 200)
        self.assertFalse(second_response.data["is_starred"])
        self.assertEqual(second_response.data["star_count"], 0)
        self.assertFalse(self.experience.starred_by.exists())

    def test_anonymous_user_cannot_star(self):
        response = self.client.post(self.star_url)

        self.assertEqual(response.status_code, 403)
        self.assertFalse(self.experience.starred_by.exists())

    def test_star_endpoint_only_accepts_post(self):
        self.client.force_authenticate(user=self.visitor)

        response = self.client.get(self.star_url)

        self.assertEqual(response.status_code, 405)

    def test_session_write_requires_csrf_token(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(
            client.login(username="owner", password=self.owner_password)
        )
        initial_count = Experience.objects.count()

        rejected_response = client.post(
            self.list_url, self.payload(), format="json"
        )
        self.assertEqual(rejected_response.status_code, 403)
        self.assertEqual(Experience.objects.count(), initial_count)

        client.get(reverse("main:show_experience"))
        csrf_token = client.cookies["csrftoken"].value
        accepted_response = client.post(
            self.list_url,
            self.payload(),
            format="json",
            HTTP_X_CSRFTOKEN=csrf_token,
        )

        self.assertEqual(accepted_response.status_code, 201)
        self.assertEqual(Experience.objects.count(), initial_count + 1)
