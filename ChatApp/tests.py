from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Group, Message, Reaction
from .forms import MessageForm, ReactionForm

class ChatAppTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.group = Group.objects.create(name='Test Group')
        self.message = Message.objects.create(sender=self.user, group=self.group, text='Test message')

    def test_send_message(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('send_message', kwargs={'group_id': self.group.id}), {'text': 'New message'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Message.objects.count(), 2)
        new_message = Message.objects.last()
        self.assertEqual(new_message.sender, self.user)
        self.assertEqual(new_message.group, self.group)
        self.assertEqual(new_message.text, 'New message')

    def test_add_reaction(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('add_reaction', kwargs={'message_id': self.message.id}), {'emoji': '👍'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Reaction.objects.count(), 1)
        new_reaction = Reaction.objects.last()
        self.assertEqual(new_reaction.message, self.message)
        self.assertEqual(new_reaction.user, self.user)
        self.assertEqual(new_reaction.emoji, '👍')
