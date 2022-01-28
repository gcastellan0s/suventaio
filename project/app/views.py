# -*- encoding: utf-8 -*-
from models import *
from forms import *
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from taggit.models import Tag
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from allauth.socialaccount.models import SocialToken, SocialAccount
from django.db.models import Q
from django.contrib.sites.models import Site
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.http import JsonResponse
from django.core import serializers
from validate_email import validate_email
from datetime import datetime, timedelta
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context, Template
from django.core.mail import EmailMultiAlternatives, get_connection
from config.settings import DEFAULT_FROM_EMAIL, SITE_ID, PRODUCTION, EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_PORT, EMAIL_USE_TLS
from django.contrib.auth.decorators import login_required
from django.http import Http404 
from serializer import ExtJsonSerializer
from django.utils.crypto import get_random_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connections
from django.db.utils import OperationalError
from money import Money
from pprint import pprint
import humanize
import sys
import time
import urllib
import re
import json
from django.core.serializers.json import DjangoJSONEncoder
import requests

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def get_domain(request):
    return request.META['HTTP_HOST'].split('.')

def user_login(request):
    domain = get_domain(request)
    message_username = ''
    if not request.user.is_anonymous():
        return HttpResponseRedirect(reverse('index',))
    if request.method == "POST":
        if 'login' in request.POST:
            username = request.POST.get('username')	
            password = request.POST.get('password')
            if validate_email(username):
                user = User.objects.filter(email=username)
                if user:
                    username = user[0].username
                else:
                    message_username = 'Usuario o Contraseña incorrectos'
            else:
                username =  domain[0] + '_' + request.POST.get('username')
            if not message_username:
                access = authenticate(username=username, password=password)
                if access:
                    login(request, access)
                    return HttpResponseRedirect(reverse('user_login'))
                else:
                    username = request.POST.get('username')
                    message_username = 'Usuario o Contraseña incorrectos'
        if 'new' in request.POST:
            message_username = 'Solicitud aceptada'
        if 'recover' in request.POST:
            message_username = 'Solicitud aceptada'
    try: 
        if domain[0] == 'ttaio':
            return render(request, 'zaresapp/lectordecb/login.html',locals())
        if domain[1] == 'ttaio':
            return render(request, 'zaresapp/lectordecb/login.html',locals())
    except:
        pass
    return render(request, 'app/login_user.html',locals())

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_login'))

def privacity(request):
    return render(request, 'app/privacity.html',locals())

def landing(request):
    return render(request, 'app/landing.html',locals())

def index(request):
    domain = get_domain(request)
    if request.user.is_anonymous():
        try:
            vamico = False
            if domain[0] == 'vamico' or domain[0] == 'vamicomx':
                vamico = True
            if domain[1] == 'vamico' or domain[1] == 'vamicomx':
                vamico = True
            if vamico:
                if request.method == "POST":
                    if not request.POST.get('oculto') and request.POST.get('mensaje'):
                        nombre = request.POST.get('nombre')
                        email = request.POST.get('email')	
                        empresa = request.POST.get('empresa')
                        mensaje = request.POST.get('mensaje')
                        subject, from_email, to = 'Contacto VAMICO', 'vamico@zaresapp.com', 'info@vamicomx.com'
                        text_content = 'TIENES UNA NUEVA FORMA DE CONTACTO'
                        html_content = '<h2>TIENES UNA NUEVA FORMA DE CONTACTO</h2>'+'<p><strong>Nombre:</strong> ' + unicode(nombre) + '</p>'+'<p><strong>Email:</strong> ' + unicode(email) + '</p>'+'<p><strong>Empresa:</strong> ' + unicode(empresa) + '</p>'+'<p><strong>Mensaje:</strong> ' + unicode(mensaje) + '</p>'
                        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                        msg.attach_alternative(html_content, "text/html")
                        msg.send()
                        mensaje = "Nos pondremos pronto en contacto contigo."
                return render(request, 'zaresapp/vamico/index.html',locals())
        except:
            pass
        try: 
            if domain[0] == 'finezipo':
                return render(request, 'zaresapp/finezipo/index.html',locals())
            if domain[1] == 'finezipo':
                return render(request, 'zaresapp/finezipo/index.html',locals())
        except:
            pass
        try: 
            if domain[0] == 'bitspixels':
                return render(request, 'zaresapp/bitspixels/index.html',locals())
            if domain[1] == 'bitspixels':
                return render(request, 'zaresapp/bitspixels/index.html',locals())
        except:
            pass
        try: 
            if domain[0] == 'automocion':
                return render(request, 'zaresapp/automocion/index.html',locals())
            if domain[1] == 'automocion':
                return render(request, 'zaresapp/automocion/index.html',locals())
        except:
            pass

        #try: 
        if domain[0] == 'sergiogarte' or domain[1] == 'sergiogarte':
            if not request.GET.get('p'):
                return render(request, 'zaresapp/sergiogarte/index.html',locals())
            page = request.GET.get('p')
            if page == 'hechura-a-medida':
                return render(request, 'zaresapp/sergiogarte/hechura-a-medida.html',locals())	
            if page == 'biografia':
                return render(request, 'zaresapp/sergiogarte/biografia.html',locals())
            if page == 'privacidad':
                return render(request, 'zaresapp/sergiogarte/privacy.html',locals())
            if page == 'contacto':
                return render(request, 'zaresapp/sergiogarte/contacto.html',locals())
            mode = [
                {
                    'index' : '1',
                    'name' : 'VESTIDO 1',
                    'price' : 0,
                    'description' : 'Vestido en chiffon Italiano color crudo.<br /> Talle en tul y decorado con flores de encaje y pedrería.',
                    'sizes' : '44, 46, 48',
                    'colors' : 'rosa',
                    'picture' : 'c1/c1-1.jpg',
                    'pictures' : ['c1/c1-2.jpg','c1/c1-3.jpg','c1/c1-4.jpg'],
                    'section' : 'alta-moda',
                },
                {
                    'index' : '2',
                    'name' : 'VESTIDO 2',
                    'price' : 0,
                    'description' : 'Falda corte sirena crepe tacto seda.<br /> Saco de paño de lana en color blanco con acabados de galón en las extremidades colocado a mano, es una reinterpretación de los sacos Dior de 1957.',
                    'sizes' : '44, 46, 48',
                    'colors' : 'blanco, negro',
                    'picture' : 'c2/c2-1.jpg',
                    'pictures' : ['c2/c2-2.jpg','c2/c2-3.jpg','c2/c2-4.jpg','c2/c2-5.jpg','c2/c2-6.jpg',],
                    'section' : 'alta-moda',
                },
                {
                    'index' : '3',
                    'name' : 'VESTIDO 3',
                    'price' : 0,
                    'description' : 'Vestido en satén: Escote corazón y abertura en la pierna decorado con aplicaciones de pedrería.<br /> Y un moño de tafeta color crema en la parte trasera ..',
                    'sizes' : '44, 46, 48',
                    'colors' : 'rojo',
                    'picture' : 'c3/c3-1.jpg',
                    'pictures' : ['c3/c3-2.jpg','c3/c3-3.jpg','c3/c3-4.jpg','c3/c3-5.jpg'],
                    'section' : 'alta-moda',
                },
                {
                    'index' : '4',
                    'name' : 'VESTIDO 4',
                    'price' : 0,
                    'description' : 'Vestido largo 3 capas de falda en gasa hoja de cebolla.<br /> Drapeado en el talle por ambos lados. Escote en V.',
                    'sizes' : '44, 46, 48',
                    'colors' : 'rojo',
                    'picture' : 'c4/c4-1.jpg',
                    'pictures' : ['c4/c4-2.jpg','c4/c4-3.jpg','c4/c4-4.jpg','c4/c4-5.jpg','c4/c4-6.jpg','c4/c4-7.jpg','c4/c4-8.jpg','c4/c4-9.jpg','c4/c4-10.jpg',],
                    'section' : 'alta-moda',
                },
                {
                    'index' : '5',
                    'name' : 'VESTIDO 5',
                    'price' : 0,
                    'description' : 'Vestido corte sirena escote alto. Sin mangas corte de 1950.<br /> Con una pequeña cauda. Elaborado en shimer italiano 100% algodón',
                    'sizes' : '44, 46, 48',
                    'colors' : 'verde',
                    'picture' : 'c5/c5-1.jpg',
                    'pictures' : ['c5/c5-2.jpg','c5/c5-3.jpg','c5/c5-4.jpg','c5/c5-5.jpg','c5/c5-6.jpg','c5/c5-7.jpg',],
                    'section' : 'alta-moda',
                },
                {
                    'index' : '6',
                    'name' : 'VESTIDO 6',
                    'price' : 0,
                    'description' : 'Falda amplia crepe tacto seda.<br /> Y corset con peplum estampado en flores azules con dorado, escote en forma de  corazón.',
                    'sizes' : '44, 46, 48',
                    'colors' : 'negro, blanco, azul, dorado',
                    'picture' : 'c6/c6-1.jpg',
                    'pictures' : ['c6/c6-2.jpg','c6/c6-3.jpg','c6/c6-4.jpg','c6/c6-5.jpg','c6/c6-6.jpg','c6/c6-7.jpg',],
                    'section' : 'alta-moda',
                },
                {
                    'index' : '7',
                    'name' : 'VESTIDO 7',
                    'price' : 0,
                    'description' : 'Vestido en color turquesa y oro, corte sirena en tafetá con corset interno, escote en forma decorazón.<br /> Y escote de moño que se une a la espalda para crear mangas.',
                    'sizes' : '44, 46, 48',
                    'colors' : 'turquesa, oro',
                    'picture' : 'c7/c7-1.jpg',
                    'pictures' : ['c7/c7-2.jpg','c7/c7-3.jpg',],
                    'section' : 'alta-moda',
                },
                {
                    'index' : '8',
                    'name' : 'VESTIDO 8',
                    'price' : 0,
                    'description' : 'Vestido en crepe tacto seda forro en contraste, estampado de cachemira morado y gris tornaron .. falda 3 capas de gasa de hoja de cebolla.<br /> Escote prolongado y escote en la cadera alta.',
                    'sizes' : '44, 46, 48',
                    'colors' : 'rosa',
                    'picture' : 'c8/c8-1.jpg',
                    'pictures' : ['c8/c8-2.jpg','c8/c8-3.jpg',],
                    'section' : 'alta-moda',
                },
                {
                    'index' : '9',
                    'name' : 'ESTAMPADO FLORAL ESTILO ACUERALA',
                    'price' : '$ 800.00 M.N.',
                    'description' : 'Vestido. en algodon. estampado floral estilo acuerala, escote v en espalda, forro en algodón',
                    'sizes' : 'CH, M, G',
                    'colors' : 'Estampado Flores',
                    'picture' : 'listo-para-llevar/1.jpg',
                    'pictures' : ['listo-para-llevar/1.jpg','listo-para-llevar/1-1.jpg','listo-para-llevar/1-2.jpg',],
                    'section' : 'listo-para-usar',
                },
                {
                    'index' : '10',
                    'name' : 'VESTIDO 2',
                    'price' : 0,
                    'description' : '',
                    'sizes' : '44, 46, 48',
                    'colors' : '',
                    'picture' : 'listo-para-llevar/2.jpg',
                    'pictures' : ['listo-para-llevar/2.jpg','listo-para-llevar/2-1.jpg',],
                    'section' : 'listo-para-usar',
                },
                {
                    'index' : '11',
                    'name' : 'VESTIDO 3',
                    'price' : 0,
                    'description' : '',
                    'sizes' : '44, 46, 48',
                    'colors' : 'negro',
                    'picture' : 'listo-para-llevar/3.jpg',
                    'pictures' : ['',],
                    'section' : 'listo-para-usar',
                },
                {
                    'index' : '12',
                    'name' : 'BLUSA ESCOTE OJAL',
                    'price' : '$ 550.M.N',
                    'description' : 'Blusa escote ojal, chifon italiano (sintetico), mangas amplias con precilla en el  hombro para ajustar el largo de la manga, boton interno. en escote acabados en color contrastante de algodon,',
                    'sizes' : '44, 46, 48',
                    'colors' : '',
                    'picture' : 'listo-para-llevar/4.jpg',
                    'pictures' : ['listo-para-llevar/4.jpg','listo-para-llevar/4-1.jpg','listo-para-llevar/4-2.jpg',],
                    'section' : 'listo-para-usar',
                },
                {
                    'index' : '13',
                    'name' : 'VESTIDO COLOR VERDE, ESCOTE EN ESPLADA, CON PEQUEÑA CAUDA',
                    'price' : '$ 5500 M.N.',
                    'description' : 'Vestido color verde, escote en esplada , con pequeña cauda, bordado en canutillo de cristal (a mano), crepe tipo seda.',
                    'sizes' : 'Se elabora a la medida',
                    'colors' : 'beige, negro y verde',
                    'picture' : 'listo-para-llevar/5.jpg',
                    'pictures' : ['listo-para-llevar/5.jpg','listo-para-llevar/5-1.jpg','listo-para-llevar/5-2.jpg',],
                    'section' : 'alta-moda',
                },
                {
                    'index' : '14',
                    'name' : 'VESTIDO CREPE TIPO SEDA',
                    'price' : '$ 5500 M.N.',
                    'description' : 'Vestido crepe tipo seda, largo recto que moldea el cuerpo, escote en espalda, abertura tracera para un caminar mas comodo',
                    'sizes' : 'M, Se elabora a la medida',
                    'colors' : 'negro y beige , forro en biscosa',
                    'picture' : 'listo-para-llevar/9.jpg',
                    'pictures' : ['listo-para-llevar/9.jpg','listo-para-llevar/9-1.jpg','listo-para-llevar/9-2.jpg',],
                    'section' : 'alta-moda',
                },
                {
                    'index' : '15',
                    'name' : 'BLUSA CAMSIERA  EN ALGODON',
                    'price' : '$500 M.N.',
                    'description' : 'blusa camsiera  en algodon, escote amplio  cuello de lazo. cuello y puños amplios. botones tipo cristal,  en puños boton doble tipo mancuernilla',
                    'sizes' : 'M, G',
                    'colors' : 'negro y beige , forro en biscosa',
                    'picture' : 'listo-para-llevar/11.jpg',
                    'pictures' : ['listo-para-llevar/11.jpg',],
                    'section' : 'listo-para-usar',
                },
                {
                    'index' : '16',
                    'name' : 'FALDA VINIPIEL CORTE BASICO',
                    'price' : '$ 450 M.N',
                    'description' : 'Falda vinipiel corte basico. forro en algodón con spandex. ',
                    'sizes' : 'CH, M, G',
                    'colors' : '',
                    'picture' : 'listo-para-llevar/13.png',
                    'pictures' : ['listo-para-llevar/13.png',],
                    'section' : 'listo-para-usar',
                },
                {
                    'index' : '17',
                    'name' : 'BLUSA DE ALGODÓN',
                    'price' : '$ 500 M.N',
                    'description' : 'Blusa de algodón .  color verde olivo,    con cinta en cintura y botones en el centro',
                    'sizes' : 'CH, M, G',
                    'colors' : '',
                    'picture' : 'listo-para-llevar/12.jpg',
                    'pictures' : ['listo-para-llevar/12.jpg',],
                    'section' : 'listo-para-usar',
                },
                {
                    'index' : '18',
                    'name' : 'BLUSA AMPLIA  ESCOTE EN V',
                    'price' : '$550 M.N',
                    'description' : 'Blusa amplia  escote en v  con mangas de campana,   en gasa de flores',
                    'sizes' : 'CH, M, G',
                    'colors' : '',
                    'picture' : 'listo-para-llevar/10.jpg',
                    'pictures' : ['listo-para-llevar/10.jpg','listo-para-llevar/10-1.jpg'],
                    'section' : 'listo-para-usar',
                },
                {
                    'index' : '19',
                    'name' : 'COLLAR PARA PERRITO',
                    'price' : 'CH $550 M $650 G $750',
                    'description' : 'Collar para perrito  elaborado en cristales tejido y cosido a mano - para no irritar ni lastimar la piel o el pelo.',
                    'sizes' : 'CH 27cm, M 47cm, G 60cm',
                    'colors' : '',
                    'picture' : 'mascotas/1.jpg',
                    'pictures' : ['mascotas/1.jpg','mascotas/1-1.jpg'],
                    'section' : 'mascotas',
                },
            ]
            if page == 'alta-moda':
                title = 'Alta Moda'
                section = 'alta-moda'
                return render(request, 'zaresapp/sergiogarte/altamoda.html',locals())
            if page == 'pret-a-porter':
                title = 'Listo para usar'
                section = request.GET.get('c')
                return render(request, 'zaresapp/sergiogarte/altamoda.html',locals())
            if page == 'producto':
                c = request.GET.get('c')
                section = request.GET.get('section')
                return render(request, 'zaresapp/sergiogarte/product.html',locals())
        #except:
            #exc_type, exc_value, exc_traceback = sys.exc_info()
            #return JsonResponse({
                #'exc_type':str(exc_type),
                #'exc_value':str(exc_value),
                #'exc_traceback':str(exc_traceback),
            #})

        try: 
            if domain[0] == 'ttaio':
                if request.GET.get('privacidad'):
                    return render(request, 'zaresapp/lectordecb/privacidad.html',locals())
                return HttpResponseRedirect(reverse('lectordecb',))
            if domain[1] == 'ttaio':
                if request.GET.get('privacidad'):
                    return render(request, 'zaresapp/lectordecb/privacidad.html',locals())
                return HttpResponseRedirect(reverse('lectordecb',))
        except:
            pass
            
        
        if domain[0] == 'armor-gym':
            page = request.GET.get('page')
            if page:
                if page=='nosotros':
                    return render(request, 'zaresapp/armorgym/nosotros.html',locals())
                if page=='entrenadores':
                    return render(request, 'zaresapp/armorgym/entrenadores.html',locals())
                if page=='nutriologos':
                    return render(request, 'zaresapp/armorgym/nutriologos.html',locals())
                if page=='armorbox':
                    return render(request, 'zaresapp/armorgym/armorbox.html',locals())
            return render(request, 'zaresapp/armorgym/index.html',locals())
        if domain[1] == 'armor-gym':
            page = request.GET.get('page')
            if page:
                if page=='nosotros':
                    return render(request, 'zaresapp/armorgym/nosotros.html',locals())
                if page=='entrenadores':
                    return render(request, 'zaresapp/armorgym/entrenadores.html',locals())
                if page=='nutriologos':
                    return render(request, 'zaresapp/armorgym/nutriologos.html',locals())
                if page=='armorbox':
                    return render(request, 'zaresapp/armorgym/armorbox.html',locals())
            return render(request, 'zaresapp/armorgym/index.html',locals())
        
        return render(request, 'app/landing.html',locals())
    else:
        if domain[0] == 'ttaio':
            if request.GET.get('hacer_corte'):
                corte_lectordecb = Corte_lectordecb.objects.filter(id = request.GET.get('hacer_corte'))
                if corte_lectordecb:
                    message = corte_lectordecb[0].hacer_corte(request.user)
            if request.GET.get('empleado'):
                corte = Corte_lectordecb.objects.filter(id = request.GET.get('corte'))
                empleado = request.GET.get('empleado')
                if corte:
                    corte = corte[0]
                    inicio, fin = corte.inicio_fin()
                    cursordb = connections['lectordecb'].cursor()
                    cursordb.execute(" SELECT * FROM fprv WHERE PRVSEQ="+empleado)
                    empleadoq = dictfetchall(cursordb)
                    total = 0
                    if not empleadoq:
                        message = "No se encontró este empleado en la base de datos."
                    else:
                        cursordb.execute("SELECT * FROM ftikets WHERE TKTDATEEND2 BETWEEN '"+inicio+"' AND '"+fin+"' AND TKTEMPL = '"+empleado+"'")
                        tickets = dictfetchall(cursordb)
                        for ticket in tickets:
                            total = total + float(ticket['TKTSURT'])
                        total = Money(amount=str(total), currency='MXN')
                    cursordb.close()
                else:
                    raise Http404
            elif request.GET.get('corte'):
                corte = Corte_lectordecb.objects.filter(id = request.GET.get('corte'))
                if corte:
                    corte = corte[0]
                    inicio, fin = corte.inicio_fin()
                    cursordb = connections['lectordecb'].cursor()
                    cursordb.execute("SELECT * FROM ftikets WHERE TKTDATEEND2 BETWEEN '"+inicio+"' AND '"+fin+"'")
                    tickets = dictfetchall(cursordb)
                    cursordb.close()
                else:
                    raise Http404
            else:
                cortes = Corte_lectordecb.objects.all().order_by('-id')
            corte_actual = Corte_lectordecb().corte_actual()
            return render(request, 'zaresapp/lectordecb/reportes.html',locals())

        if request.user.profile == 'Administrador' or request.user.is_superuser:
            return render(request, 'app/index.html',locals())
        elif request.user.profile == 'Cajero' or request.user.profile == 'Vendedor' or request.user.profile == 'Vendedor autorizado para cobrar':
            if len(request.user.sell_point.all()) > 1:
                return HttpResponseRedirect(reverse('select_sellpoint'))
            else:
                if request.user.profile == 'Vendedor' or request.user.profile == 'Vendedor autorizado para cobrar':
                    return HttpResponseRedirect(reverse('vendor', args=[request.user.sell_point.all()[0].slug])+'?id='+str(request.user.sell_point.all()[0].id))

def invoice(request):
    form = InvoiceClientForm()
    if request.method == "POST":
        form = InvoiceClientForm(request.POST)
    return render(request, 'app/invoice.html',locals())

@login_required( login_url = '/login/' )
def select_sellpoint(request):
    return render(request, 'app/select_sellpoint.html',locals())

def rest_inventory(product_attr, quantity):
    product_attr.inventory = product_attr.inventory - quantity
    product_attr.save()
    return True

@csrf_exempt
@login_required( login_url = '/login/' )
def vendor(request, slug):
    sell_point = Sell_point.objects.get(id=request.GET.get('id'), slug=slug)
    show_sellpoint_name = True
    if request.method == 'POST':
        if 'get_products' in request.POST:
            return JsonResponse({
                'products': ExtJsonSerializer().serialize( Product_attrs.objects.filter(product__menu=Menu.objects.get(id=request.POST.get('menu')), sell_point=sell_point, active=True), fields=('alias','inventory','price','dynamic_price','bar_code','taxes'), props=('image','name','units','quantity','format_price','color_menu')),
            })
        if 'last_tickets' in request.POST:
            return JsonResponse({
                'tickets': ExtJsonSerializer().serialize( Ticket.objects.filter(user=request.user).order_by('-id')[0:5], fields=('code_sellpoint', 'total'), props=() ),
            })
        if 'make_ticket' in request.POST:
            products_ticket = json.loads(request.POST.get('ticket'))
            anticipe = request.POST.get('anticipe')
            is_order = request.POST.get('is_order')
            ticket = Ticket()
            code_sellpoint, code_company = ticket.assign_codes(sell_point)
            ticket.code_sellpoint = code_sellpoint
            ticket.code_company = code_company
            ticket.sell_point = sell_point
            ticket.user = request.user
            if is_order == 'true':
                ticket.is_order = True
                ticket.anticipe = anticipe
            else:
                ticket.is_order = False
                ticket.anticipe = 0
            if request.user.profile == 'Vendedor':
                ticket.status = 'Pendiente'
            else:
                ticket.status = 'Cobrado'
            ticket.total = 0
            ticket.taxes = 0
            ticket.secret_code = get_random_string(length=8)
            ticket.cut = ticket.assign_cut(sell_point)
            ticket.save()
            total = 0
            taxes = 0
            for product_ticket in products_ticket:
                product_attr = Product_attrs.objects.get(id=product_ticket['product_id'])
                if not ticket.status == 'Pendiente':
                    rest_inventory(product_attr, product_ticket['quantity'])
                    
                    #for products in product_attr.products.recipe.all()
                        #try:
                            #product_attr.objects.get(products=)
                ticket_products = Ticket_products()
                ticket_products.ticket = ticket
                ticket_products.product = product_attr.product.name
                ticket_products.alias = product_ticket['alias']
                ticket_products.quantity = product_ticket['quantity']
                ticket_products.price = product_ticket['price']
                ticket_products.total = round((float(product_ticket['price']) * float(product_ticket['quantity'])),2)
                if product_attr.taxes:
                    ticket_products.taxes = ( ticket_products.total / 1.16) * .16
                else:
                    ticket_products.taxes = 0
                ticket_products.save()
                total += ticket_products.total
                taxes += ticket_products.taxes
            ticket.total = total
            ticket.taxes = taxes
            ticket.save()
            return JsonResponse({
                'code': ticket.code_sellpoint,
                'total': total,
                'taxes': taxes,
                'subtotal': total - taxes,
                'key': ticket.secret_code,
            })
    my_products = sell_point.my_products()
    my_menus = sell_point.my_menus(my_products)
    return render(request, 'app/vendor.html',locals()) 

@login_required( login_url = '/login/' )
def users(request):
    if request.user.profile == 'Administrador' or request.user.is_superuser:
        users = User.objects.filter(company=request.user.company)
    else:
        raise Http404
    return render(request, 'app/users.html',locals())

@login_required( login_url = '/login/' )
def user_form(request, action):
    if request.user.profile == 'Administrador' or request.user.is_superuser:
        if action == 'add':
            form = UserForm()
            if request.method == "POST":
                form = UserForm(request.POST)
                if form.is_valid():
                    user = form.save(commit=False)
                    user.set_password('l6jig7_*po@v152$-k2m@3')
                    user.company = request.user.company
                    user.username = request.user.company.name.lower() + '_' + user.visible_username
                    user.save()
                    form.save_m2m()
                    return HttpResponseRedirect(reverse('change_password', args=[user.id]))
        elif action == 'edit':
            user = User.objects.get(id=request.GET.get('id'))
            form = UserForm(instance=user)
            if request.method == "POST":
                form = UserForm(request.POST, instance=user)
                if form.is_valid():
                    user = form.save(commit=False)
                    user.username = request.user.company.name.lower() + '_' + user.visible_username
                    user.save()
                    form.save_m2m()
                    return HttpResponseRedirect(reverse('users'))
        elif action == 'delete':
            User.objects.get(id=request.GET.get('id')).delete()
            return HttpResponseRedirect(reverse('users'))
    else:
        raise Http404
    return render(request, 'app/user_form.html',locals())

@login_required( login_url = '/login/' )
def change_password(request, id):
    user = User.objects.get(id=id)
    if request.user.profile == 'Administrador' or request.user.is_superuser or request.user == user:
        form = Change_PasswordForm(instance=user)	
        if request.method == "POST":
            form = Change_PasswordForm(request.POST, instance=user)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(request.POST.get('password2'))
                user.password2 = None
                user.password3 = None
                user.save()
        return render(request, 'app/change_password_form.html',locals())
    else:
        raise Http404

def sellpoints(request):
    if request.user.profile == 'Administrador' or request.user.is_superuser:
        pvs = Sell_point.objects.filter(company = request.user.company)
    else:
        raise Http404
    return render(request, 'app/sellpoints.html',locals())

def sellpoint_form(request, acction):
    if request.user.profile == 'Administrador' or request.user.is_superuser:
        if acction == 'add':
            form = Sell_pointForm()
            if request.method == "POST":
                form = Sell_pointForm(request.POST, request.FILES)
                if form.is_valid():
                    points = len(Sell_point.objects.filter(company=request.user.company))
                    if points >= request.user.company.sell_point_limits:
                        messages.error(request, 'Llegaste al limite de tus puntos de venta')
                        return HttpResponseRedirect(reverse('sellpoints'))
                    else:
                        obj = form.save(commit=False)
                        obj.name = obj.name.upper()
                        obj.company = request.user.company
                        obj.create_by = request.user
                        if points == 0:
                            obj.cost = 1200
                        elif points == 1:
                            obj.cost = 800
                        elif points > 1:
                            obj.cost = 400
                        obj.save()
                        return HttpResponseRedirect(reverse('sellpoints'))
        elif acction == 'edit':
            sellpoint = Sell_point.objects.get(id=request.GET.get('id'))
            form = Sell_pointForm(instance=sellpoint)
            if request.method == "POST":
                form = Sell_pointForm(request.POST, request.FILES, instance=sellpoint)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.name = obj.name.upper()
                    obj.save()
                    return HttpResponseRedirect(reverse('sellpoints'))
        elif acction == 'delete':
            Sell_point.objects.get(id=request.GET.get('id')).delete()
            return HttpResponseRedirect(reverse('sellpoints'))	
        return render(request, 'app/sellpoint_form.html',locals())
    else:
        raise Http404

@csrf_exempt
def menus(request):
    if request.user.profile == 'Administrador' or request.user.is_superuser:
        menus = Menu.objects.filter(company = request.user.company)
    else:
        raise Http404
    return render(request, 'app/menus.html',locals())

@csrf_exempt
def menu_form(request, acction):
    if request.user.profile == 'Administrador' or request.user.is_superuser:
        if acction == 'add':
            form = MenusForm(request.user,)
            if request.method == "POST":
                form = MenusForm(request.user, request.POST)
                if form.is_valid():
                    obj = form.save(commit = False)
                    obj.company = request.user.company
                    obj.save()
                    return HttpResponseRedirect(reverse('menus'))
        elif acction == 'edit':
            menu = Menu.objects.get(id=request.GET.get('id'))
            form = MenusForm(request.user, instance=menu)
            if request.method == "POST":
                form = MenusForm(request.user, request.POST, instance=menu)
                if form.is_valid():
                    obj = form.save(commit = False)
                    obj.company = request.user.company
                    obj.save()
                    return HttpResponseRedirect(reverse('menus'))
        elif acction == 'delete':
            Menu.objects.get(id=request.GET.get('id')).delete()
            return HttpResponseRedirect(reverse('menus'))	
        return render(request, 'app/menu_form.html',locals())
    else:
        raise Http404

@csrf_exempt
def menus_ajax(request):
    if request.user.profile == 'Administrador' or request.user.is_superuser:
        if 'treeData' in request.POST:
            def recursor (data, parent):
                level = 0
                for d in data:
                    menu = Menu.objects.get(id = d['id'])
                    menu.nivel = level
                    menu.parent = parent
                    menu.save()
                    if d['children']:
                        recursor(d['children'], menu)
                    level += 1
            data = json.loads(request.POST.get('treeData'))
            recursor (data, None)
            return JsonResponse({
                'json': True,
            })
        if 'edit' in request.POST:
            menu = Menu.objects.get(id = request.POST.get('id'))
            menu.name = request.POST.get('name')
            menu.color = request.POST.get('color')
            try :
                menu.parent = Menu.objects.get(id = request.POST.get('parent'))
            except:
                menu.parent = None
            menu.save()
            return JsonResponse({
                'json': True,
            })
        if 'getid' in request.POST:
            menu = Menu.objects.get(id = request.POST.get('getid'))
            try:
                parent = menu.parent.id
            except:
                parent = None
            return JsonResponse({
                'id': menu.id,
                'name': menu.name,
                'color': menu.color,
                'parent': parent,
            })
        if 'delete' in request.POST:
            Menu.objects.get(id = request.POST.get('id')).delete()
            return JsonResponse({
                'json': True,
            })
    else:
        raise Http404

def products(request):
    if request.user.profile == 'Administrador' or request.user.is_superuser:
        products = Product.objects.filter(company = request.user.company)
        return render(request, 'app/products.html',locals())
    else:
        raise Http404

@csrf_exempt
def product_form(request, acction):
    if request.user.profile == 'Administrador' or request.user.is_superuser:
        if acction == 'add':
            form = ProductForm(request.user,)
            if request.method == "POST":
                form = ProductForm(request.user, request.POST)
                if form.is_valid():
                    obj = form.save(commit = False)
                    obj.company = request.user.company
                    obj.save()
                    form.save_m2m()
                    for sell_point in obj.sell_points.all():
                        product_attrs = Product_attrs()
                        product_attrs.product = obj
                        product_attrs.sell_point = sell_point
                        product_attrs.alias = obj.name
                        product_attrs.save()
                    return HttpResponseRedirect(reverse('products'))
        elif acction == 'edit':
            product = Product.objects.get(id=request.GET.get('id'))
            list_sell_points = []
            for sell_point in product.sell_points.all():
                list_sell_points.append(sell_point)
            form = ProductForm(request.user, instance=product)
            if request.method == "POST":
                form = ProductForm(request.user, request.POST, instance=product)
                if form.is_valid():
                    obj = form.save(commit = False)
                    obj.company = request.user.company
                    obj.save()
                    form.save_m2m()
                    for sell_point in obj.sell_points.all():
                        if not Product_attrs.objects.filter(product=product, sell_point=sell_point):
                            product_attrs = Product_attrs()
                            product_attrs.product = obj
                            product_attrs.sell_point = sell_point
                            product_attrs.alias = obj.name
                            product_attrs.save()
                    for sell_point in list_sell_points:
                        if not sell_point in obj.sell_points.all():
                            Product_attrs.objects.filter(product=product, sell_point=sell_point).delete()
                    return HttpResponseRedirect(reverse('products'))
        elif acction == 'delete':
            Product.objects.get(id=request.GET.get('id')).delete()
            return HttpResponseRedirect(reverse('products'))	
        return render(request, 'app/product_form.html',locals())
    else:
        raise Http404

def recipes(request, slug):
    if request.user.profile == 'Administrador' or request.user.is_superuser:
        product = Product.objects.get(id=request.GET.get('id'), slug=slug)
        if request.user.company == product.company or request.user.is_superuser:
            recipes = Recipe.objects.filter(parent=product)
            return render(request, 'app/recipes.html',locals())
        else:
            raise Http404
    else:
        raise Http404

def recipe_form(request, acction):
    if request.user.profile == 'Administrador' or request.user.is_superuser:
        product = Product.objects.get(id=request.GET.get('id'))
        if request.user.company == product.company or request.user.is_superuser:
            if acction == 'add':
                form = RecipeForm(request.user, product,)
                if request.method == "POST":
                    form = RecipeForm(request.user, product, request.POST)
                    if form.is_valid():
                        obj = form.save(commit = False)
                        try:
                            recipe = Recipe.objects.get(product=obj.product, parent=product)
                            recipe.quantity = recipe.quantity + obj.quantity
                            recipe.save()
                        except:
                            obj.parent = product
                            obj.save()
                        return HttpResponseRedirect(reverse('recipes', args=[product.slug])+'?id='+str(product.id))
            elif acction == 'delete':
                Recipe.objects.get(id=request.GET.get('recipe')).delete()
                return HttpResponseRedirect(reverse('recipes', args=[product.slug])+'?id='+str(product.id))	
            return render(request, 'app/recipe_form.html',locals())
        else:
            raise Http404
    else:
        raise Http404

def product_attributes(request, slug):
    if request.user.profile == 'Administrador' or request.user.is_superuser:
        product = Product.objects.get(id=request.GET.get('id'), slug=slug)
        product_attrs = Product_attrs.objects.filter(product=product)
        
        return render(request, 'app/product_attributes.html',locals())
        
    else:
        raise Http404

def product_attribute_form(request):
    if request.user.profile == 'Administrador' or request.user.is_superuser:
        product_attrs = Product_attrs.objects.get(id=request.GET.get('id'))
        if request.user.company == product_attrs.sell_point.company or request.user.is_superuser:
            form = Product_attrsForm(instance = product_attrs)
            if request.method == "POST":
                form = Product_attrsForm(request.POST, instance = product_attrs)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(reverse('product_attributes', args=[product_attrs.product.slug]) + '?id=' + str(product_attrs.product.id))
            return render(request, 'app/product_attribute_form.html',locals())
        else:
            raise Http404
    else:
        raise Http404

def sellpoints_cut(request):
    if request.user.profile == 'Administrador' or request.user.is_superuser:
        pvs = Sell_point.objects.filter(company = request.user.company)
    else:
        raise Http404
    return render(request, 'app/sellpoints_cut.html',locals())

def cut_times(request, slug):
    if request.user.profile == 'Administrador' or request.user.is_superuser:
        sellpoint = Sell_point.objects.get(id=request.GET.get('id'), slug=slug)
        cuttime = Cuttime.objects.filter(sell_point=sellpoint)
        if request.user.company == sellpoint.company or request.user.is_superuser:
            return render(request, 'app/cut_times.html',locals())
        else:
            raise Http404
    else:
        raise Http404
    
@csrf_exempt
def cut_time_form(request, slug):
    sellpoint = Sell_point.objects.get(id=request.GET.get('id'), slug=slug)
    try:
        Cuttime.objects.get(id=request.GET.get('delete')).delete()
        return HttpResponseRedirect(reverse('cut_times', args=[sellpoint.slug])+'?id='+str(sellpoint.id))
    except:
        pass
    if request.user.profile == 'Administrador' or request.user.is_superuser:
        if request.user.company == sellpoint.company or request.user.is_superuser:
            form = CuttimeForm()
            if request.method == "POST":
                cuttime = Cuttime()
                cuttime.time = datetime.strptime(request.POST.get('time'), '%I:%M %p')
                cuttime.sell_point = sellpoint
                cuttime.save()
                return HttpResponseRedirect(reverse('cut_times', args=[sellpoint.slug])+'?id='+str(sellpoint.id))
            return render(request, 'app/cut_time_form.html',locals())
        else:
            raise Http404
    else:
        raise Http404

def cuts(request, slug):
    sellpoint = Sell_point.objects.get(id=request.GET.get('id'), slug=slug)
    if request.user.profile == 'Administrador' or request.user.is_superuser:
        if request.user.company == sellpoint.company or request.user.is_superuser:
            paginator = Paginator(Cut.objects.filter(sell_point = sellpoint).order_by('-id'), 35)
            try:
                cuts = paginator.page(request.GET.get('page'))
            except PageNotAnInteger:
                cuts = paginator.page(1)
            except EmptyPage:
                cuts = paginator.page(paginator.num_pages)
            pagemin = cuts.number - 2
            pagemax = cuts.number + 5
            return render(request, 'app/cuts.html',locals())
        else:
            raise Http404
    else:
        raise Http404

def make_cut(cut):
    cut.terminate = True
    cut.save()
    return True

@csrf_exempt
def cut_details(request):
    cut = Cut.objects.get(id=request.GET.get('id')) 
    if request.method == 'POST':
        if 'make_cut' in request.POST:
            action = make_cut(cut)
            return JsonResponse({
                'cut': action,
            })
    if request.user.profile == 'Administrador' or request.user.is_superuser:
        if request.user.company == cut.sell_point.company or request.user.is_superuser:
            products_array = []
            total = 0
            taxes = 0
            tickets = Ticket.objects.filter(cut = cut).order_by('-id')
            ticket_products = Ticket_products.objects.filter(ticket__cut=cut).order_by('alias')
            for ticket_product in ticket_products:
                flag = True
                for row in products_array:
                    if row['alias'] == ticket_product.alias and row['price'] == ticket_product.price:
                        row['quantity'] += ticket_product.quantity
                        row['total'] += ticket_product.total
                        row['taxes'] += ticket_product.taxes
                        flag = False
                        break
                if flag:
                    products_array.append( 
                        {
                            'alias':ticket_product.alias,
                            'quantity':ticket_product.quantity,
                            'price':ticket_product.price,
                            'total':ticket_product.total,
                            'taxes':ticket_product.taxes,
                        }
                    )
                total +=  ticket_product.total
                taxes += ticket_product.taxes
            subtotal = total - taxes
            return render(request, 'app/cut_details.html',locals())
        else:
            raise Http404
    else:
        raise Http404

def ticket_detail(request, id):
    if request.user.profile == 'Administrador' or request.user.is_superuser:
        ticket = Ticket.objects.get(id=id)
        if request.user.company == ticket.sell_point.company or request.user.is_superuser:
            return render(request, 'app/ticket_detail.html',locals())
        else:
            raise Http404
    else:
        raise Http404

def invoice_sellpoint(request):
    if request.user.profile == 'Administrador' or request.user.is_superuser:
        pvs = Sell_point.objects.filter(company = request.user.company)
    else:
        raise Http404
    return render(request, 'app/invoice_sellpoint.html',locals())

def invoice_sellpoint_form(request, acction):
    if request.user.profile == 'Administrador' or request.user.is_superuser:
        if acction == 'edit':
            sellpoint = Sell_point.objects.get(id=request.GET.get('id'))
            form = InvoiceSell_pointForm(instance=sellpoint)
            if request.method == "POST":
                form = InvoiceSell_pointForm(request.POST, request.FILES, instance=sellpoint)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.rfc = obj.rfc.upper()
                    obj.save()
                    return HttpResponseRedirect(reverse('invoice_sellpoint'))
        return render(request, 'app/invoice_sellpoint_form.html',locals())
    else:
        raise Http404

####FINEZIPO

def finezipo_nosotros(request):
    return render(request, 'zaresapp/finezipo/nosotros.html',locals())

def finezipo_artistas(request, artista):
    if artista == 'manelyk':
        artista = 'Manelyk'
        return render(request, 'zaresapp/finezipo/manelik.html',locals())
    if artista == 'tracy':
        artista = 'Tracy Sáenz'
        return render(request, 'zaresapp/finezipo/tracy.html',locals())
    if artista == 'jenny':
        artista = 'Jenny Garcia'
        return render(request, 'zaresapp/finezipo/jenny.html',locals())
    if artista == 'gemelos':
        artista = 'GEMELOS'
        return render(request, 'zaresapp/finezipo/gemelos.html',locals())
    if artista == 'sabrinasabrok':
        artista = 'Sabrina Sabrok'
        return render(request,'zaresapp/finezipo/sabrinasabrok.html',locals())
    if artista == 'lorena':
        artista = 'Lorena Herrera'
        return render(request,'zaresapp/finezipo/lorena.html',locals())
    if artista == 'esteban':
        artista = 'Esteban Martinez'
        return render(request,'zaresapp/finezipo/esteban.html',locals())
    if artista == 'elettra':
        artista = 'Elettra Lamborghini'
        return render(request,'zaresapp/finezipo/elettra.html',locals())
    if artista == 'igor':
        artista = 'Igor'
        return render(request,'zaresapp/finezipo/igor.html',locals())
    if artista == 'fernando':
        artista = 'Fernando'
        return render(request,'zaresapp/finezipo/fernando.html',locals())
    if artista == 'jawi':
        artista = 'Jawi'
        return render(request,'zaresapp/finezipo/jawi.html',locals())
    if artista == 'vanessa':
        artista = 'Vanessa Claudio'
        return render(request,'zaresapp/finezipo/vanessa.html',locals())
    if artista == 'lisvega':
        artista = 'Lis Vega'
        return render(request,'zaresapp/finezipo/lisvega.html',locals())
    if artista == 'marlene':
        artista = 'MAarlene Favela'
        return render(request,'zaresapp/finezipo/marlenefavela.html',locals())
    if artista == 'vanessahuppenkothen':
        artista = 'Vanessa Huppenkothen'
        return render(request,'zaresapp/finezipo/vanessahuppenkothen.html',locals())
    if artista == 'talia':
        artista = 'Talia Acashore'
        return render(request,'zaresapp/finezipo/talia.html',locals())
    if artista == 'karime':
        artista = 'Talia Acashore'
        return render(request,'zaresapp/finezipo/karime.html',locals())
    if artista == 'wanderslover':
        artista = 'Wanders Lover'
        return render(request,'zaresapp/finezipo/wanderslover.html',locals())
    if artista == 'victorortiz':
        artista = 'Victor Ortiz'
        return render(request,'zaresapp/finezipo/victorortiz.html',locals())
    if artista == 'eleazargomez':
        artista = 'Eleazar Gómez'
        return render(request,'zaresapp/finezipo/eleazargomez.html',locals())
    if artista == 'gabyramirez':
        artista = 'Gaby Ramírez'
        return render(request,'zaresapp/finezipo/gabyramirez.html',locals())
    if artista == 'yessicamonsalve':
        artista = 'DJ La Fresa'
        return render(request,'zaresapp/finezipo/yessicamonsalve.html',locals())
    if artista == 'wapayasos':
        artista = 'WAPAYASOS'
        return render(request,'zaresapp/finezipo/wapayasos.html',locals())
    if artista == 'letwins':
        artista = 'LETWINS'
        return render(request,'zaresapp/finezipo/letwins.html',locals())
    if artista == 'karenka':
        artista = 'KARENKA'
        return render(request,'zaresapp/finezipo/karenka.html',locals())
    if artista == 'labebeshita':
        artista = 'La Bebeshita'
        return render(request,'zaresapp/finezipo/labebeshita.html',locals())
    if artista == 'shuloscalderon':
        artista = 'Los Chulos Calderón'
        return render(request,'zaresapp/finezipo/shuloscalderon.html',locals())
    if artista == 'caelike':
        artista = 'Caelike'
        return render(request,'zaresapp/finezipo/caelike.html',locals())
    if artista == 'chamosalas':
        artista = 'Chamo Salas'
        return render(request,'zaresapp/finezipo/chamosalas.html',locals())
    if artista == 'jeremy':
        artista = 'Jheremy'
        return render(request,'zaresapp/finezipo/jeremy.html',locals())
    if artista == 'damaris':
        artista = 'Damaris Rojas'
        return render(request,'zaresapp/finezipo/damaris.html',locals())
    if artista == 'mhoni':
        artista = 'Mhoni Vidente'
        return render(request,'zaresapp/finezipo/mhoni.html',locals())
    if artista == 'marisolgrajales':
        artista = 'Marisol Grajales'
        return render(request,'zaresapp/finezipo/marisolgrajales.html',locals())
    if artista == 'nataliaontiveros':
        artista = 'Natalia Ontiveros'
        return render(request,'zaresapp/finezipo/nataliaontiveros.html',locals())
    if artista == 'ernestocazares':
        artista = 'Ernesto Cazares'
        return render(request,'zaresapp/finezipo/ernestocazares.html',locals())
    if artista == 'aristeocazares':
        artista = 'Aristeo Cazares'
        return render(request,'zaresapp/finezipo/aristeocazares.html',locals())
    if artista == 'malakings':
        artista = 'Malakings'
        return render(request,'zaresapp/finezipo/malakings.html',locals())
    if artista == 'jihu':
        artista = 'Jihu'
        return render(request,'zaresapp/finezipo/jihu.html',locals())
    if artista == 'petrova':
        artista = 'Petrova'
        return render(request,'zaresapp/finezipo/petrova.html',locals())
    if artista == 'vikingo':
        artista = 'Vikingo'
        return render(request,'zaresapp/finezipo/vikingo.html',locals())
    if artista == 'fernandocorona':
        artista = 'Fernando Corona'
        return render(request,'zaresapp/finezipo/fernandocorona.html',locals())
    if artista == 'aleidanunez':
        artista = 'Aleida Nuñez'
        return render(request,'zaresapp/finezipo/aleidanunez.html',locals())
    if artista == 'ianyeley':
        artista = 'Ian y Eley'
        return render(request,'zaresapp/finezipo/ianyeley.html',locals())
    if artista == 'anaespinola':
        artista = 'Ana Espinola'
        return render(request,'zaresapp/finezipo/anaespinola.html',locals())
    if artista == 'veronicamontes':
        artista = 'Veronica Montes'
        return render(request,'zaresapp/finezipo/veronicamontes.html',locals())

def finezipo_contacto(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')	
        empresa = request.POST.get('empresa')
        mensaje = request.POST.get('mensaje')
        subject, from_email, to = 'Contacto Finezipo', 'finezipo@zaresapp.com', 'fine.zipo@gmail.com'
        text_content = 'TIENES UNA NUEVA FORMA DE CONTACTO'
        html_content = '<h2>TIENES UNA NUEVA FORMA DE CONTACTO</h2>'+'<p><strong>Nombre:</strong> ' + unicode(nombre) + '</p>'+'<p><strong>Email:</strong> ' + unicode(email) + '</p>'+'<p><strong>Empresa:</strong> ' + unicode(empresa) + '</p>'+'<p><strong>Mensaje:</strong> ' + unicode(mensaje) + '</p>'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        mensaje = "Nos pondremos pronto en contacto contigo. :)"
    return render(request, 'zaresapp/finezipo/contacto.html',locals())

def finezipo_que_hacemos(request):
    return render(request, 'zaresapp/finezipo/que_hacemos.html',locals())

def finezipo_shows(request):
    return render(request, 'zaresapp/finezipo/shows.html',locals())

def finezipo_shows_info(request, info):
    info = info
    return render(request, 'zaresapp/finezipo/shows_info.html',locals())

@csrf_exempt
def lectordecb(request):
    if request.method == "POST":
        api = request.POST.get('api')
        if api == 'login':
            try:
                cursordb = connections['lectordecb'].cursor()
                cursordb.execute(" SELECT * FROM fprv WHERE PRVCOD='"+request.POST.get('usuario')+"' AND PRVPASWORD='"+request.POST.get('password')+"' ")
                querydb = dictfetchall(cursordb)
                cursordb.close()
                flagapi = False
                usuario = ''
                usuario_id = ''
                usuario_name = ''
                message = 'Usuario ó contraseña incorrectos'
                tickets = []
                if len(querydb) > 0:
                    flagapi = True
                    try:
                        usuario_par1 = int(querydb[0]['PRVPAR1'])
                    except:
                        usuario_par1 = '00'
                    try:
                        usuario_par2 = int(querydb[0]['PRVPAR2'])
                    except:
                        usuario_par2 = '00'
                    usuario = querydb[0]['PRVCOD']
                    usuario_id = querydb[0]['PRVSEQ']
                    usuario_name = querydb[0]['PRVNOM']
                    message = 'Éxito'
                    corte_actual = Corte_lectordecb().corte_actual()
                    inicio, fin = corte_actual.inicio_fin()
                    cursordb = connections['lectordecb'].cursor()
                    cursordb.execute("SELECT * FROM ftikets WHERE TKTDATEEND2 BETWEEN '"+inicio+"' AND '"+fin+"' AND TKTEMPL = '"+str(usuario)+"'")
                    querydb = dictfetchall(cursordb)
                    json_tickets = json.dumps(querydb, cls=DjangoJSONEncoder)
                    cursordb.close()
                    return JsonResponse({
                        'location': request.POST.get('location'),
                        'action': flagapi,
                        'message': message,
                        'usuario': usuario,
                        'usuario_id': usuario_id,
                        'usuario_par1': usuario_par1,
                        'usuario_par2': usuario_par2,
                        'usuario_name': usuario_name,
                        'corte': str(corte_actual.id),
                        'tickets': json_tickets,
                    })
                else:
                    return JsonResponse({
                        'location': False,
                        'action': False,
                        'message': 'Usuario ó contraseña incorrectos',
                        'usuario': False,
                        'usuario_id': False,
                        'usuario_name': False,
                    })
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                return JsonResponse({
                    'location': False,
                    'action': False,
                    'message': 'Por favor contacte al administrador del sistema con este error: ' + str(exc_value.message) + ' in: ' + str(exc_traceback.tb_lineno) + ' type: ' + str(exc_type.__name__),
                    'usuario': False,
                    'usuario_id': False,
                    'usuario_name': False,
                })
        elif api == 'capture':
            try:
                codebar = str(request.POST.get('codebar'))
                if codebar == '8778895' or codebar == '8778894' or codebar == '8778893':
                    return JsonResponse({
                            'flagapi': 1,
                            'codebar': 'Producto prueba - ' + codebar,
                            'usuario': request.POST.get('usuario'),
                            'tktprod': codebar,
                            'tktvalor': 100.00,
                            'tktvalor_': str(Money(amount=str(100.00), currency='MXN')),
                            'tktcant': 150,
                            'tkttotal': 100.00 * 150,
                            'tkttotal_': str(100.00 * 150),
                            'message': str(150) + ' u. a  ' + str(Money(amount=str(100.00), currency='MXN')) + ' = ' + str(str(100.00 * 150)),
                        })
                cursordb = connections['lectordecb'].cursor()
                cursordb.execute(" SELECT * FROM ftikets WHERE TKTSEQ='"+codebar+"' ")
                querydb = dictfetchall(cursordb)
                cursordb.close()
                if len(querydb) > 0:
                    if querydb[0]['TKTSTATUS'] == 0:
                        flagapi = 1
                        codebar = str(querydb[0]['TKTPROD']) + ' - ' + str(querydb[0]['TKTSEQ'])
                        usuario = request.POST.get('usuario')
                        tktprod = querydb[0]['TKTPROD']
                        tktvalor = float(querydb[0]['TKTMIN'])
                        tktvalor_ = Money(amount=str(tktvalor), currency='MXN')
                        tktcant = int(querydb[0]['TKTCANT'])
                        tkttotal = tktvalor * tktcant
                        tkttotal_ = Money(amount=str(tkttotal), currency='MXN')
                        message = str(tktcant) + ' u. a  ' + str(tktvalor_) + ' = ' + str(tkttotal_)
                        date1 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        date2 = datetime.now().strftime('%Y-%m-%d')
                        cursordb = connections['lectordecb'].cursor()
                        cursordb.execute(""+
                            "UPDATE ftikets "+
                            "SET "+
                                    "TKTSTATUS=1, "+
                                    "TKTSURT='"+str(tktcant)+"', "+
                                    "TKTEMPL='"+usuario+"', "+
                                    "TKTCOM='"+message+"', "+
                                    "TKTPEDPLSEQ='"+str(Corte_lectordecb().corte_actual().id)+"', "+
                                    "TKTPAR0='"+request.POST.get('usuario_par1')+"', "+
                                    "TKTPAR1='"+request.POST.get('usuario_par2')+"', "+
                                    "TKTDATEEND='"+str(date2)+"', "+
                                    "TKTDATEEND2='"+str(date1)+"' "+
                            "WHERE"+
                                " TKTSEQ = "+ str(querydb[0]['TKTSEQ'])+
                        "")
                        cursordb.close()
                        return JsonResponse({
                            'flagapi': flagapi,
                            'codebar': codebar,
                            'usuario': usuario,
                            'tktprod': tktprod,
                            'tktvalor': tktvalor,
                            'tktvalor_': str(tktvalor_),
                            'tktcant': tktcant,
                            'tkttotal': tkttotal,
                            'tkttotal_': str(	),
                            'message': message,
                        })
                    else:
                        flagapi = 0
                        codebar = 'Error: ' + str(querydb[0]['TKTSEQ'])
                        usuario = request.POST.get('usuario')
                        tktprod = None
                        tktvalor = None
                        tktcant = None
                        tkttotal = None
                        message = 'Este código ya fué registrado anteriormente'
                else:
                    flagapi = 0
                    codebar = 'Error - ' + request.POST.get('codebar')
                    usuario = request.POST.get('usuario')
                    tktprod = None
                    tktvalor = None
                    tktcant = None
                    tkttotal = None
                    message = 'No se encontraron coincidencias en la base de datos'
                cursordb.close()
                return JsonResponse({
                    'flagapi': flagapi,
                    'codebar': codebar,
                    'usuario': usuario,
                    'tktprod': tktprod,
                    'tktvalor': tktvalor,
                    'tktcant': tktcant,
                    'tkttotal': tkttotal,
                    'message': message,
                })
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                return JsonResponse({
                    'flagapi': 0,
                    'codebar': 'Error',
                    'usuario': None,
                    'tktprod': None,
                    'tktvalor': None,
                    'tktcant': None,
                    'tkttotal': None,
                    'message': 'Por favor contacte al administrador del sistema con este error: ' + str(exc_value.message) + ' in: ' + str(exc_traceback.tb_lineno) + ' type: ' + str(exc_type.__name__)
                })
        if api == 'report':
            try:
                corte = request.POST.get('corte')
                corte = Corte_lectordecb.objects.filter(id = corte)
                if corte:
                    inicio, fin = corte[0].inicio_fin()
                    cursordb = connections['lectordecb'].cursor()
                    cursordb.execute("SELECT * FROM ftikets WHERE TKTDATEEND2 BETWEEN '"+inicio+"' AND '"+fin+"' AND TKTEMPL = '"+request.POST.get('usuario')+"'")
                    querydb = dictfetchall(cursordb)
                    json_tickets = json.dumps(querydb, cls=DjangoJSONEncoder)
                    cursordb.close()
                    return JsonResponse({
                        'flagapi': 1,
                        'tickets': json_tickets,
                    })
                return JsonResponse({
                    'flagapi': 0,
                    'message': 'No se encontró ningún corte relacionado',
                })
            except Exception as e:
                return JsonResponse({
                    'flagapi': 0,
                    'message': 'Error: ' + str(e),
                })
    return HttpResponseRedirect(reverse('user_login'))

    
