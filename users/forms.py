# coding=utf-8
import os
from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _
from rolepermissions.shortcuts import assign_role
from django.contrib.auth.forms import UserCreationForm
from core.forms import RegisterUserForm
from .models import User


class ProfileForm(forms.ModelForm):

	def save(self, commit=True):
		super(ProfileForm, self).save(commit=False)

		self.instance.set_password(self.cleaned_data['password'])
		self.instance.save()

		return self.instance

	class Meta:
		model = User
		fields = ['username', 'name', 'email', 'password', 'birth_date', 'city', 'state', 'gender', 'cpf', 'phone', 'image']
		widgets = {
			'password':forms.PasswordInput
		}

class UserForm(RegisterUserForm):

	class Meta:
		model = User
		fields = ['username', 'name', 'email', 'birth_date', 'city', 'state', 'gender', 'type_profile', 'cpf', 'phone', 'image', 'is_staff', 'is_active']

class EditUserForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ['username', 'name', 'email', 'birth_date', 'city', 'state', 'gender', 'cpf', 'phone', 'image']

# Ailson
class UpdateUserForm(forms.ModelForm):
	company_logo = forms.ImageField(label=_('Company Logo'),required=False, error_messages = {'invalid':_("Image files only")})

	class Meta:
		model = User
		fields = ['username', 'name', 'email', 'city', 'state', 'birth_date', 'gender', 'cpf', 'phone', 'image']