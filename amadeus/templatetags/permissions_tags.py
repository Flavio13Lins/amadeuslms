""" 
Copyright 2016, 2017 UFPE - Universidade Federal de Pernambuco
 
Este arquivo é parte do programa Amadeus Sistema de Gestão de Aprendizagem, ou simplesmente Amadeus LMS
 
O Amadeus LMS é um software livre; você pode redistribui-lo e/ou modifica-lo dentro dos termos da Licença Pública Geral GNU como publicada pela Fundação do Software Livre (FSF); na versão 2 da Licença.
 
Este programa é distribuído na esperança que possa ser útil, mas SEM NENHUMA GARANTIA; sem uma garantia implícita de ADEQUAÇÃO a qualquer MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a Licença Pública Geral GNU para maiores detalhes.
 
Você deve ter recebido uma cópia da Licença Pública Geral GNU, sob o título "LICENSE", junto com este programa, se não, escreva para a Fundação do Software Livre (FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA.
"""

from django import template

from amadeus import permissions
from users.models import User

register = template.Library()


@register.assignment_tag
def has_support():
    return "true" if User.objects.filter(is_support=True).exists() else "false"


@register.assignment_tag
def show_support_button(user):
    return not user.is_support


@register.assignment_tag
def analytics_permissions(user):
    return permissions.has_analytics_permissions(user)


@register.assignment_tag
def category_permissions(user, category):
    return permissions.has_category_permissions(user, category)


@register.assignment_tag
def category_manage_permissions(user, category):
    return permissions.has_category_manage_permissiosn(user, category)


@register.assignment_tag
def subject_permissions(user, subject):
    return permissions.has_subject_permissions(user, subject)


@register.assignment_tag
def subject_manage_permissions(user, subject):
    return permissions.has_subject_manage_permissions(user, subject)


@register.assignment_tag
def subject_view_permissions(user, subject):
    return permissions.has_subject_view_permissions(user, subject)


@register.assignment_tag
def resource_permissions(user, resource):
    return permissions.has_resource_permissions(user, resource)

