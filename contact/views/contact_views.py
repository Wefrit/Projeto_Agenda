from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from contact.models import Contact


def get_contacts_queryset(request):
    queryset = Contact.objects.filter(show=True)

    if not request.user.is_superuser:
        queryset = queryset.filter(owner=request.user)

    return queryset


@login_required(login_url='contact:login')
def index(request):
    contacts = get_contacts_queryset(request).order_by('-id')

    paginator = Paginator(contacts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'site_title': 'Contatos - ',
    }

    return render(
        request,
        'contact/index.html',
        context,
    )


@login_required(login_url='contact:login')
def search(request):
    search_value = request.GET.get('q', '').strip()

    if search_value == '':
        return redirect('contact:index')

    contacts = get_contacts_queryset(request)

    contacts = contacts.filter(
        Q(first_name__icontains=search_value) |
        Q(last_name__icontains=search_value) |
        Q(phone__icontains=search_value)
    ).order_by('-id')

    paginator = Paginator(contacts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'site_title': 'Busca - ',
    }

    return render(
        request,
        'contact/index.html',
        context,
    )


@login_required(login_url='contact:login')
def contact(request, contact_id):
    single_contact = get_object_or_404(
        get_contacts_queryset(request),
        pk=contact_id,
    )

    site_title = f'{single_contact.first_name} {single_contact.last_name} - '

    context = {
        'contact': single_contact,
        'site_title': site_title,
    }

    return render(
        request,
        'contact/contact.html',
        context,
    )