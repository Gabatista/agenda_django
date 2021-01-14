from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Contato
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages

def index(request):
    messages.add_message(request,messages.ERROR, 'Ocorreu um erro')

    contatos = Contato.objects.order_by('-nome')
    paginator = Paginator(contatos,10)
    """
    contatos = Contato.objects.order_by('-id').filter(
        show=True
    )
    """

    page = request.GET.get('p')
    contatos = paginator.get_page(page)

    return render(request,'contatos/index.html', {
        'contatos': contatos
    })

def show_contact(request, contato_id):
        contato = get_object_or_404(Contato, id=contato_id)

        if not contato.show:
            raise Http404()

        return render(request,'contatos/show_contact.html', {
            'contato': contato
        })

def busca(request):
    termo = request.GET.get('termo')

    if termo is None or not termo:
        messages.add_message(request, messages.ERROR,'Campo termo deve ser preenchido')
        return redirect('index')

    campos = Concat('nome', Value(' '), 'sobrenome')

    contatos = Contato.objects.annotate(
        nome_completo = campos
    ).filter(
        Q(nome_completo_icontains = termo) | Q(telefone_icontains = termo)
    )

    paginator = Paginator(contatos,10)

    page = request.GET.get('p')
    contatos = paginator.get_page(page)

    return render(request, 'contatos/busca.html', {
        'contatos': contatos
    })



