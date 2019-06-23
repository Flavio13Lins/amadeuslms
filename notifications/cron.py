""" 
Copyright 2016, 2017 UFPE - Universidade Federal de Pernambuco
 
Este arquivo é parte do programa Amadeus Sistema de Gestão de Aprendizagem, ou simplesmente Amadeus LMS
 
O Amadeus LMS é um software livre; você pode redistribui-lo e/ou modifica-lo dentro dos termos da Licença Pública Geral GNU como publicada pela Fundação do Software Livre (FSF); na versão 2 da Licença.
 
Este programa é distribuído na esperança que possa ser útil, mas SEM NENHUMA GARANTIA; sem uma garantia implícita de ADEQUAÇÃO a qualquer MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a Licença Pública Geral GNU para maiores detalhes.
 
Você deve ter recebido uma cópia da Licença Pública Geral GNU, sob o título "LICENSE", junto com este programa, se não, escreva para a Fundação do Software Livre (FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA.
"""

from django_cron import CronJobBase, Schedule

from users.models import User
from .models import CronNotification
from .utils import set_notifications


class Notify(CronJobBase):
    RUN_EVERY_MINS = 1440  # every day

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'amadeus.notification_cron'  # a unique code

    def do(self):
        set_notifications()

        admins = User.objects.filter(is_staff=True)

        if admins.count() > 0:
            admin = admins[0]
            cron_notification = CronNotification(user=admin)
            cron_notification.save()


def notification_cron():
    set_notifications()

    admins = User.objects.filter(is_staff=True)

    if admins.count() > 0:
        admin = admins[0]

        cron_notification = CronNotification(user=admin)
        cron_notification.save()
