""" 
Copyright 2016, 2017 UFPE - Universidade Federal de Pernambuco
 
Este arquivo é parte do programa Amadeus Sistema de Gestão de Aprendizagem, ou simplesmente Amadeus LMS
 
O Amadeus LMS é um software livre; você pode redistribui-lo e/ou modifica-lo dentro dos termos da Licença Pública Geral GNU como publicada pela Fundação do Software Livre (FSF); na versão 2 da Licença.
 
Este programa é distribuído na esperança que possa ser útil, mas SEM NENHUMA GARANTIA; sem uma garantia implícita de ADEQUAÇÃO a qualquer MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a Licença Pública Geral GNU para maiores detalhes.
 
Você deve ter recebido uma cópia da Licença Pública Geral GNU, sob o título "LICENSE", junto com este programa, se não, escreva para a Fundação do Software Livre (FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA.
"""

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from categories.models import Category
from log.models import Log
from subjects.models import Subject, Tag

valid_formats = ['image/jpeg', 'image/x-citrix-jpeg', 'image/png', 'image/x-citrix-png',
                 'image/x-png', 'image/gif']


def validate_img_extension(value):
    if hasattr(value.file, 'content_type'):
        if not value.file.content_type in valid_formats:
            raise ValidationError(_('File not supported.'))


class Question(models.Model):
    enunciado = models.TextField(_("Statement"), blank=True)
    question_img = models.ImageField(verbose_name=_("Image"), blank=True, null=True,
                                     upload_to='questions/', validators=[validate_img_extension])
    categories = models.ManyToManyField(Tag, verbose_name='categories',
                                        related_name='question_categories', blank=False)
    subject = models.ForeignKey(Subject, verbose_name=_('Subject'), related_name='question_subject',
                                null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return self.enunciado


class Alternative(models.Model):
    content = models.TextField(_("Content"))
    question = models.ForeignKey(Question, verbose_name=_('Question'), related_name='alt_question',
                                 null=True, on_delete=models.SET_NULL)
    alt_img = models.ImageField(verbose_name=_("Image"), blank=True, null=True,
                                upload_to='questions/alternatives',
                                validators=[validate_img_extension])
    is_correct = models.BooleanField(_('Is correct?'), default=False)

    class Meta:
        verbose_name = "Alternative"
        verbose_name_plural = "Alternatives"

    def __str__(self):
        return self.content


class CreateQuestionInDBLog(Log):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL)


class ReplicateQuestionInDBLog(Log):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL)


class UpdateQuestionInDBLog(Log):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL)


class DeleteQuestionInDBLog(Log):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL)
