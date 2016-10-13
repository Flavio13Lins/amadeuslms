from django.test import TestCase,Client
from django.core.urlresolvers import reverse
from rolepermissions.shortcuts import assign_role
from django.utils.translation import ugettext_lazy as _

from users.models import User
from .models import *
from .forms import *

# Create your tests here.
class LinkTestCase(TestCase):
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
    def test_create_link(self):
        self.client.login(username='user', password = 'testing')
        links = Link.objects.all().count()
        self.assertEqual(Link.objects.all().count(),links) #Before creating the link
        url = reverse('course:create_link')
        data = {
        'name' : 'testinglink',
        "description" : 'testdescription',
        "link" : 'teste.com'
        }
        response = self.client.post(url, data)
        #self.assertEqual(response.status_code, 200)
        self.assertFormError(response,'form',"link",_("Please enter a valid URL"))
        self.assertEqual(Link.objects.all().count(),links+1) #After creating one link, if OK, the link was created successfully.
        self.assertEqual(response.status_code, 302) #If OK, User is getting redirected correctly.
        self.assertTemplateUsed(template_name = 'links/link_modal.html')
    # def test_update_link():
    #     pass
    def test_delete_link(self):
         self.link = Link.objects.create(
         name = 'testinglink',
         description = 'testdescription',
         link = 'teste.com'
         )
         self.client.login(username='user', password = 'testing')
         links = Link.objects.all().count()
         deletedlink = Link.objects.get(name = self.link.name)
         url = reverse('course:delete_link',kwargs={'linkname': self.link.name})
         self.assertEqual(Link.objects.all().count(),links)
         response = self.client.post(url)
         self.assertEqual(Link.objects.all().count(),links - 1) #Objeto removido
         self.assertEqual(Link.objects.filter(name= deletedlink.name).exists(),False) #Objeto removido e sua não-existência verificada
         #self.assertEqual(Link.objects.filter(name= deletedlink.name).exists(),True) #Objeto removido e sua existência verificada, se ERRO, objeto foi removido com sucesso!
         self.assertEqual(response.status_code, 302) #If OK, User is getting redirected correctly.
