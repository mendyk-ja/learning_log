"""Definiuje wzorce adresow URl dla learning_logs."""

from django.urls import path

from . import views

app_name = 'learning_logs'
urlpatterns = [
	# Strona glowna.
	path('', views.index, name='index'),
	# wyswietlenie wszystkich tematow
	path('topics/', views.topics, name='topics'),
	# strona szczegolowa dotyczaca pojedycznego tematu
	path('topics/(<int:topic_id>)/', views.topic, name='topic'),
	# strona przeznaczona do dodawania nowego tematu
	path('new_topic/', views.new_topic, name='new_topic'),
	# strona przeznaczona do dodawania nowych wpisow
	path('new_entry/(<int:topic_id>)/', views.new_entry, name='new_entry'),
	# strona przeznaczona do edycji wpisu
	path('edit_entry/(<int:entry_id>)/', views.edit_entry, name='edit_entry'),
]