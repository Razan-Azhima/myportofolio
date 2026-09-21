import json

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Achievement, Education, Experience, Skill


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )
        self.achievement = Achievement.objects.create(
            title="Juara 1 Hackathon",
            category="Kompetisi",
            year="2025",
            description="Membuat aplikasi berbasis Django.",
            issuer="Universitas Indonesia",
        )
        self.education = Education.objects.create(
            institution="Universitas Indonesia",
            degree_or_major="S1 Sistem Informasi",
            faculty="Fakultas Ilmu Komputer",
            period="2024 – Sekarang",
            status="Mahasiswa Aktif",
        )
        self.skill = Skill.objects.create(
            name="Python / Django",
            category="backend",
            description="Pengembangan REST API dan web monolitik.",
        )

    # --- Main Page Tests ---
    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")
        self.assertEqual(response.status_code, 404)

    # --- Experience Model & View Tests ---
    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))
        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))
        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")

    # --- Achievement Model & View Tests ---
    def test_achievement_model(self):
        self.assertEqual(str(self.achievement), "Juara 1 Hackathon")

    def test_achievement_page(self):
        response = self.client.get(reverse("main:show_achievements"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "achievements.html")
        self.assertContains(response, self.achievement.title)
        self.assertContains(response, self.achievement.category)
        self.assertContains(response, self.achievement.year)
        self.assertContains(response, self.achievement.description)
        self.assertContains(response, self.achievement.issuer)

    def test_empty_achievement_page(self):
        Achievement.objects.all().delete()
        response = self.client.get(reverse("main:show_achievements"))
        self.assertContains(response, "Belum ada pencapaian yang ditambahkan.")

    # --- Education Model & View Tests ---
    def test_education_model(self):
        self.assertEqual(str(self.education), "Universitas Indonesia")

    def test_education_page(self):
        response = self.client.get(reverse("main:show_education"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education.html")
        self.assertContains(response, self.education.institution)
        self.assertContains(response, self.education.degree_or_major)
        self.assertContains(response, self.education.faculty)
        self.assertContains(response, self.education.period)
        self.assertContains(response, self.education.status)

    def test_empty_education_page(self):
        Education.objects.all().delete()
        response = self.client.get(reverse("main:show_education"))
        self.assertContains(response, "Belum ada riwayat pendidikan yang ditambahkan.")

    def test_education_search_filter(self):
        Education.objects.create(
            institution="Institut Teknologi Bandung",
            degree_or_major="Teknik Informatika",
            faculty="STEI",
            period="2020 – 2024",
            status="Lulus",
        )
        response = self.client.get(reverse("main:show_education"), {"title": "Indonesia"})
        self.assertContains(response, self.education.institution)
        self.assertNotContains(response, "Institut Teknologi Bandung")

    def test_create_education_page_get(self):
        response = self.client.get(reverse("main:create_education"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education_form.html")
        self.assertContains(response, "Add New Education")

    def test_create_education_post_valid(self):
        response = self.client.post(reverse("main:create_education"), {
            "institution": "Universitas Gadjah Mada",
            "degree_or_major": "Teknik Elektro",
            "faculty": "Fakultas Teknik",
            "period": "2021 – 2025",
            "status": "Lulus",
        })
        self.assertRedirects(response, reverse("main:show_education"))
        self.assertTrue(
            Education.objects.filter(institution="Universitas Gadjah Mada").exists()
        )

    def test_create_education_post_invalid(self):
        initial_count = Education.objects.count()
        response = self.client.post(reverse("main:create_education"), {
            "institution": "",
            "degree_or_major": "",
            "faculty": "",
            "period": "",
            "status": "",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Education.objects.count(), initial_count)

    def test_update_education_page_get(self):
        response = self.client.get(
            reverse("main:update_education", args=[self.education.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education_form.html")
        self.assertContains(response, "Edit Education")
        self.assertContains(response, self.education.institution)

    def test_update_education_post_valid(self):
        response = self.client.post(
            reverse("main:update_education", args=[self.education.id]),
            {
                "institution": "Universitas Indonesia",
                "degree_or_major": "S1 Sistem Informasi",
                "faculty": "Fakultas Ilmu Komputer",
                "period": "2024 – Sekarang",
                "status": "Mahasiswa Aktif (Update)",
            },
        )
        self.assertRedirects(response, reverse("main:show_education"))
        self.education.refresh_from_db()
        self.assertEqual(self.education.status, "Mahasiswa Aktif (Update)")

    def test_update_nonexistent_education_returns_404(self):
        response = self.client.get(
            reverse("main:update_education", args=["00000000-0000-0000-0000-000000000000"])
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_education_post(self):
        response = self.client.post(
            reverse("main:delete_education", args=[self.education.id])
        )
        self.assertRedirects(response, reverse("main:show_education"))
        self.assertFalse(Education.objects.filter(id=self.education.id).exists())

    def test_delete_education_get_does_not_delete(self):
        response = self.client.get(
            reverse("main:delete_education", args=[self.education.id])
        )
        self.assertRedirects(response, reverse("main:show_education"))
        self.assertTrue(Education.objects.filter(id=self.education.id).exists())

    def test_get_educations_json(self):
        response = self.client.get(reverse("main:get_educations_json"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["fields"]["institution"], self.education.institution)

    def test_get_educations_json_with_filter(self):
        Education.objects.create(
            institution="Institut Teknologi Bandung",
            degree_or_major="Teknik Informatika",
            faculty="STEI",
            period="2020 – 2024",
            status="Lulus",
        )
        response = self.client.get(
            reverse("main:get_educations_json"), {"title": "Bandung"}
        )
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["fields"]["institution"], "Institut Teknologi Bandung")

    # --- Skill Model & View Tests ---
    def test_skill_model(self):
        self.assertEqual(str(self.skill), "Python / Django")

    def test_skill_page(self):
        response = self.client.get(reverse("main:show_skills"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "skills.html")
        self.assertContains(response, self.skill.name)
        self.assertContains(response, self.skill.description)
        self.assertContains(response, "Backend")

    def test_empty_skill_page(self):
        Skill.objects.all().delete()
        response = self.client.get(reverse("main:show_skills"))
        self.assertContains(response, "Belum ada keahlian yang ditambahkan.")

    def test_create_skill_page_get(self):
        response = self.client.get(reverse("main:create_skill"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "skill_form.html")
        self.assertContains(response, "Add New Skill")

    def test_create_skill_post_valid(self):
        response = self.client.post(reverse("main:create_skill"), {
            "name": "React",
            "category": "frontend",
            "description": "Membangun antarmuka pengguna berbasis komponen.",
        })
        self.assertRedirects(response, reverse("main:show_skills"))
        self.assertTrue(Skill.objects.filter(name="React").exists())

    def test_create_skill_post_invalid(self):
        initial_count = Skill.objects.count()
        response = self.client.post(reverse("main:create_skill"), {
            "name": "",
            "category": "backend",
            "description": "",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Skill.objects.count(), initial_count)

    def test_update_skill_page_get(self):
        response = self.client.get(reverse("main:update_skill", args=[self.skill.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "skill_form.html")
        self.assertContains(response, "Edit Skill")
        self.assertContains(response, self.skill.name)

    def test_update_skill_post_valid(self):
        response = self.client.post(
            reverse("main:update_skill", args=[self.skill.id]),
            {
                "name": "Python / Django",
                "category": "backend",
                "description": "Pengembangan REST API tingkat lanjut.",
            },
        )
        self.assertRedirects(response, reverse("main:show_skills"))
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.description, "Pengembangan REST API tingkat lanjut.")

    def test_update_nonexistent_skill_returns_404(self):
        response = self.client.get(
            reverse("main:update_skill", args=["00000000-0000-0000-0000-000000000000"])
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_skill_post(self):
        response = self.client.post(reverse("main:delete_skill", args=[self.skill.id]))
        self.assertRedirects(response, reverse("main:show_skills"))
        self.assertFalse(Skill.objects.filter(id=self.skill.id).exists())

    def test_delete_skill_get_does_not_delete(self):
        response = self.client.get(reverse("main:delete_skill", args=[self.skill.id]))
        self.assertRedirects(response, reverse("main:show_skills"))
        self.assertTrue(Skill.objects.filter(id=self.skill.id).exists())