# coding=utf-8

from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from rolepermissions.shortcuts import assign_role

from courses.models import Course, Category
from courses.forms import CourseForm
from users.models import User

class CourseViewTestCase(TestCase):

	def setUp(self):
		self.client = Client()

		self.user = User.objects.create_user(
			username = 'test',
			email = 'testing@amadeus.com',
			is_staff = True,
			is_active = True,
			password = 'testing'
		)
		assign_role(self.user, 'system_admin')

		self.category = Category(
			name = 'Categoria Teste',
			slug = 'categoria_teste'
		)
		self.category.save()

		self.course = Course(
			name = 'Curso Teste',
			slug = 'curso_teste',
			max_students = 50,
			init_register_date = '2016-08-26',
			end_register_date = '2016-10-01',
			init_date = '2016-10-05',
			end_date = '2017-10-05',
			category = self.category
		)
		self.course.save()

	def test_index(self):
		self.client.login(username='test', password='testing')

		url = reverse('course:manage')

		response = self.client.get(url)

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'course/index.html')

	def test_index_not_logged(self):
		url = reverse('course:manage')

		response = self.client.get(url, follow = True)

		self.assertRedirects(response, '%s?next=%s' % (reverse('core:home'), url), 302, 200)

	def test_create(self):
		self.client.login(username='test', password='testing')

		url = reverse('course:create')
		data = {
			"name": 'Curso Teste',
			"slug":'curso_teste',
			"max_students": 50,
			"init_register_date": '2016-08-26',
			"end_register_date": '2016-10-01',
			"init_date":'2016-10-05',
			"end_date":'2017-10-05',
			"category": self.category
		}

		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'course/create.html')

	def test_create_not_logged(self):
		url = reverse('course:create')

		response = self.client.get(url, follow = True)

		self.assertRedirects(response, '%s?next=%s' % (reverse('core:home'), url), 302, 200)

	def test_create_no_permission(self):
		self.user = User.objects.create_user(username = 'student', email = 'student@amadeus.com', type_profile = 2, is_staff = False, is_active = True, password = 'testing')

		assign_role(self.user, 'student')

		self.client.login(username='student', password='testing')

		url = reverse('course:create')

		response = self.client.get(url)

		self.assertEquals(response.status_code, 403)


	def test_update(self):

		self.client.login(username = 'test', password = 'testing')

		url = reverse('course:update', kwargs = {'slug': self.course.slug})
		data = Course.objects.get(name="Curso Teste")
		data.name = "Curse Test"

		# response = self.client.put(url, data)
		# self.assertEqual(response.status_code, 200)
		# self.assertEqual(response.data, data.name)

	def test_update_not_logged(self):
		url = reverse('course:update', kwargs = {'slug': self.course.slug})

		response = self.client.get(url, follow = True)

		self.assertRedirects(response, '%s?next=%s' % (reverse('core:home'), url), 302, 200)

	def test_update_no_permission(self):
		self.user = User.objects.create_user(username = 'student', email = 'student@amadeus.com', type_profile = 2, is_staff = False, is_active = True, password = 'testing')

		assign_role(self.user, 'student')

		self.client.login(username='student', password='testing')

		url = reverse('course:update', kwargs = {'slug': self.course.slug})

		response = self.client.get(url)

		self.assertEquals(response.status_code, 403)

	def test_view(self):
		self.client.login(username = 'test', password = 'testing')

		url = reverse('course:view', kwargs = {'slug': self.course.slug})

		# response = self.client.get(url)

		# self.assertEquals(response.status_code, 200)
		# self.assertTemplateUsed(response, 'course/view.html')

	def test_update_not_logged(self):
		url = reverse('course:view', kwargs = {'slug': self.course.slug})

		response = self.client.get(url, follow = True)

		self.assertRedirects(response, '%s?next=%s' % (reverse('core:home'), url), 302, 200)
