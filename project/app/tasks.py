from __future__ import absolute_import
from celery import shared_task
from project.app.models import Corte_lectordecb

@shared_task
def CORTE_AUTOMATICO():
	corte_actual = Corte_lectordecb().corte_actual()
	corte_actual.hacer_corte('Corte Automatico')
	Corte_lectordecb().corte_actual()
	return 'Corte realizado con exito'