from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Project, Skill


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="PBP Teaching Assistant",
            description="Help students understand web development.",
            category="part-time",
        )
        self.skill = Skill.objects.create(
            name="Python",
            description="Snake",
        )
        self.project = Project.objects.create(
            title="My Project",
            description="A simple project.",
            tech_stack="Django",
        )

    def _login_star_user(self):
        User.objects.create_user(username="star-user", password="StrongPassword123!")
        self.assertTrue(
            self.client.login(username="star-user", password="StrongPassword123!")
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experiences")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/a-page-that-does-not-exist/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "PBP Teaching Assistant")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experiences"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_experience_json(self):
        response = self.client.get(reverse("main:get_experience_json"))

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["pk"], str(self.experience.id))
        self.assertEqual(data[0]["fields"]["title"], self.experience.title)
        self.assertEqual(data[0]["fields"]["description"], self.experience.description)
        self.assertEqual(data[0]["fields"]["category"], "part-time")
        self.assertIsNone(data[0]["fields"]["ended_at"])

    def test_empty_experience_json(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:get_experience_json"))

        self.assertEqual(response.json(), [])

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:get_experience_json"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertIsNotNone(response.json()[0]["fields"]["ended_at"])

    def test_project_page(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project.html")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_project_api_returns_project(self):
        response = self.client.get(reverse("api:project-list"))

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], self.project.title)
        self.assertEqual(data[0]["description"], self.project.description)

    def test_empty_project_api(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("api:project-list"))

        self.assertEqual(response.json(), [])

    def test_empty_state_message_in_pages(self):
        self.assertContains(
            self.client.get(reverse("main:show_projects")),
            "No projects have been added or found yet.",
        )
        self.assertContains(
            self.client.get(reverse("main:show_experiences")),
            "No experiences have been added or found yet.",
        )

    def test_skill_page(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertContains(response, self.skill.name)
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_experience_star(self):
        self._login_star_user()

        response = self.client.post(
            reverse("main:toggle_experience_star", args=[self.experience.id])
        )

        self.assertRedirects(response, reverse("main:show_experiences"))
        self.assertTrue(self.experience.starred_by.filter(username="star-user").exists())

    def test_project_star(self):
        self._login_star_user()

        response = self.client.post(
            reverse("api:project-star", args=[self.project.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["is_starred"])
        self.assertTrue(self.project.starred_by.filter(username="star-user").exists())
