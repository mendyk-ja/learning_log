from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm


def index(request):
	""" Strona glowna dla aplikacji Learning Log."""
	return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
	"""wyswietlenie wszystkich tematow"""
	topics = Topic.objects.filter(owner=request.user).order_by('date_added')
	context = {'topics': topics}
	return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
	"""wyswietla pojedynczy temat i wszystkie powiazane z nim wpisy."""
	topic = Topic.objects.get(id=topic_id)
	if topic.owner != request.user:
		raise Http404

	entries = topic.entry_set.order_by('-date_added')
	context = {'topic': topic, 'entries': entries}
	return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
	"""dodaj nowy temat"""
	if request.method != 'POST':
		# nie przekazano zadnych danych, nalezy utworzyc nowy formularz
		form = TopicForm()
	else:
		# przekazano dane za pomoca metody POST, nalezy je przetworzyc
		form = TopicForm(data=request.POST)
		if form.is_valid():
			new_topic = form.save(commit=False)
			new_topic.owner = request.user
			form.save()
			return redirect('learning_logs:topics')

	# wyswietlenie pustego formularza
	context = {'form': form}
	return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
	"""Dodanie nowego wpisu dla okreslonego tmeaty."""
	topic = Topic.objects.get(id=topic_id)

	if request.method != 'POST':
		# Nie przekazano zadnych danych, nalezy utowrzyc pusty formularz.
		form= EntryForm()
	else:
		# przekazano dane za pooca zadania POST, nalezy je przetworzyc
		form = EntryForm(data=request.POST)
		if form.is_valid():
			new_entry = form.save(commit=False)
			new_entry.topic = topic
			new_entry.save()
			return redirect('learning_logs:topic', topic_id=topic_id)

	# wyswietlenie pustego komentarza
	context = {'topic': topic, 'form': form}
	return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
	"""Edycja istniejacego wpisu."""
	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic
	if topic.owner != request.user:
		raise Http404

	if request.method != 'POST':
		# zadanie poczatkowe, wypelnienie formularza aktualna trescia wpisu."""
		form = EntryForm(instance=entry)
	else:
		# przekazano dane za pomoca zadania POST, nalezy je przetworzyc
		form = EntryForm(instance=entry, data=request.POST)
		if form.is_valid():
			form.save()
			return redirect('learning_logs:topic', topic_id=topic.id)

	context = {'entry': entry, 'topic': topic, 'form': form}
	return render(request, 'learning_logs/edit_entry.html', context)