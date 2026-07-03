from django.shortcuts import render, redirect, get_object_or_404
from .forms import TicketForm, CommentForm
from .models import Ticket


def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            return redirect('ticket_list')
    else:
        form = TicketForm()

    return render(request, 'tickets/create_ticket.html', {'form': form})

from .models import Ticket


def ticket_list(request):
    tickets = Ticket.objects.all().order_by('-created_at')
    return render(request, 'tickets/ticket_list.html', {'tickets': tickets})

from django.shortcuts import get_object_or_404

def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket
            comment.user = request.user
            comment.save()
    else:
        form = CommentForm()

    return render(request, 'tickets/ticket_detail.html', {
        'ticket': ticket,
        'form': form
    })