import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Experience


class ExperienceAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.regular = User.objects.create_user(
            username="regular", password="test-password", email="regular@example.com",
        )
        self.editor = User.objects.create_user(username="editor", password="test-password")
        self.editor.groups.add(Group.objects.create(name="Editor"))

        self.experience = Experience.objects.create(
            title="Teaching Assistant", description="Helped students", category="part-time",
        )
        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse("api:experience-detail", args=[self.experience.id])
        self.star_url = reverse("api:experience-star", args=[self.experience.id])
        self.payload = {
            "title": "Research Intern", "description": "Worked on NLP",
            "category": "internship", "experience_image_url": "",
        }

    def assert_unchanged(self):
        """The database still holds exactly the original experience."""
        self.assertEqual(Experience.objects.count(), 1)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Teaching Assistant")
        self.assertEqual(self.experience.description, "Helped students")
        self.assertEqual(self.experience.category, "part-time")

    # ---- reading (everyone) ----

    def test_visitor_can_read_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.experience.id))
        self.assertEqual(response.data[0]["star_count"], 0)
        self.assertFalse(response.data[0]["is_starred"])
        detail = self.client.get(self.detail_url)
        self.assertEqual(detail.status_code, status.HTTP_200_OK)
        self.assertEqual(detail.data["title"], "Teaching Assistant")

    def test_search_and_empty_results(self):
        Experience.objects.create(title="Volunteer Teacher", description="x")
        response = self.client.get(self.list_url, {"title": "TEACHING"})
        self.assertEqual([item["title"] for item in response.data], ["Teaching Assistant"])
        self.assertEqual(self.client.get(self.list_url, {"title": "nothing"}).data, [])

    def test_missing_experience_returns_404(self):
        url = reverse("api:experience-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_response_does_not_leak_account_data(self):
        self.experience.starred_by.add(self.regular)
        body = str(self.client.get(self.list_url).data)
        self.assertNotIn("regular@example.com", body)
        self.assertNotIn("password", body)
        self.assertNotIn("email", body)

    # ---- visitors and regular users cannot write ----

    def test_visitor_cannot_write(self):
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, 403)
        self.assertEqual(self.client.patch(self.detail_url, {"title": "Hacked"}, format="json").status_code, 403)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assert_unchanged()

    def test_regular_user_cannot_write(self):
        self.client.force_authenticate(user=self.regular)
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, 403)
        self.assertEqual(self.client.patch(self.detail_url, {"title": "Hacked"}, format="json").status_code, 403)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assert_unchanged()

    # ---- editor ----

    def test_editor_can_patch_and_put(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(self.detail_url, {"title": "Senior TA"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Senior TA")
        self.assertEqual(self.experience.description, "Helped students")

        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Research Intern")
        self.assertEqual(self.experience.category, "internship")

    def test_editor_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assert_unchanged()

    def test_staff_without_editor_group_cannot_patch(self):
        staff = User.objects.create_user(username="staff", password="test-password", is_staff=True)
        self.client.force_authenticate(user=staff)
        self.assertEqual(self.client.patch(self.detail_url, {"title": "Hacked"}, format="json").status_code, 403)
        self.assert_unchanged()

    # ---- owner ----

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Experience.objects.count(), 2)
        self.assertTrue(Experience.objects.filter(pk=response.data["id"], title="Research Intern").exists())

    def test_owner_can_update_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.patch(self.detail_url, {"title": "Lead TA"}, format="json").status_code, 200)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Lead TA")
        self.assertEqual(self.client.delete(self.detail_url).status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Experience.objects.filter(pk=self.experience.pk).exists())

    # ---- validation ----

    def test_html_tags_are_stripped(self):
        self.client.force_authenticate(user=self.owner)
        payload = {**self.payload, "title": "<b>Bold</b> title", "description": "<script>x</script>Text"}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created = Experience.objects.get(pk=response.data["id"])
        self.assertEqual(created.title, "Bold title")
        self.assertNotIn("<", created.description)

    def test_invalid_input_returns_400_and_saves_nothing(self):
        self.client.force_authenticate(user=self.owner)
        bad_payloads = [
            {**self.payload, "title": "<b></b>"},
            {**self.payload, "title": "   "},
            {**self.payload, "title": "x" * 300},
            {**self.payload, "description": ""},
            {**self.payload, "category": "astronaut"},
            {**self.payload, "experience_image_url": "not-a-url"},
            {**self.payload, "ended_at": "not-a-date"},
        ]
        for payload in bad_payloads:
            response = self.client.post(self.list_url, payload, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, payload)
        self.assert_unchanged()

    def test_invalid_patch_returns_400_and_keeps_data(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(self.detail_url, {"title": "<i></i>"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)
        self.assert_unchanged()

    def test_read_only_fields_cannot_be_written(self):
        self.client.force_authenticate(user=self.owner)
        forged_id = str(uuid.uuid4())
        payload = {**self.payload, "id": forged_id, "star_count": 99, "is_starred": True}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.data["id"], forged_id)
        self.assertEqual(response.data["star_count"], 0)
        self.assertEqual(Experience.objects.get(pk=response.data["id"]).starred_by.count(), 0)

    # ---- stars ----

    def test_visitor_cannot_star(self):
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.experience.starred_by.count(), 0)

    def test_star_toggles_for_logged_in_user(self):
        self.client.force_authenticate(user=self.regular)
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        self.assertTrue(self.experience.starred_by.filter(pk=self.regular.pk).exists())

        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)
        self.assertEqual(self.experience.starred_by.count(), 0)

    def test_star_always_uses_request_user(self):
        self.client.force_authenticate(user=self.regular)
        self.client.post(self.star_url, {"user": self.owner.pk, "user_id": self.owner.pk}, format="json")
        self.assertEqual(list(self.experience.starred_by.all()), [self.regular])

    def test_editor_can_star(self):
        self.client.force_authenticate(user=self.editor)
        self.assertEqual(self.client.post(self.star_url).status_code, 200)
        self.assertEqual(self.experience.starred_by.count(), 1)

    def test_star_missing_experience_returns_404(self):
        self.client.force_authenticate(user=self.regular)
        url = reverse("api:experience-star", args=[uuid.uuid4()])
        self.assertEqual(self.client.post(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_star_state_is_per_user_in_list(self):
        self.experience.starred_by.add(self.regular)
        self.client.force_authenticate(user=self.regular)
        self.assertTrue(self.client.get(self.list_url).data[0]["is_starred"])
        self.client.force_authenticate(user=self.owner)
        self.assertFalse(self.client.get(self.list_url).data[0]["is_starred"])

    def test_star_rejects_get(self):
        self.client.force_authenticate(user=self.regular)
        self.assertEqual(self.client.get(self.star_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # ---- CSRF (real session login, no force_authenticate) ----

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(client.delete(self.detail_url).status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.assert_unchanged()
        self.assertEqual(self.experience.starred_by.count(), 0)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        client.get(reverse("main:show_experiences"))  # sets the csrftoken cookie
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Experience.objects.count(), 2)
