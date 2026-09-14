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