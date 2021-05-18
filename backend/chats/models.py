import json

import requests
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import get_object_or_404
from django.db.models.signals import post_save
from django.dispatch import receiver

from allauth.socialaccount.models import SocialToken


class Contact(models.Model):
    user = models.ForeignKey(
        User, related_name='friends', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Message(models.Model):
    sender = models.TextField()
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contact.user.username


class RepoChats(models.Model):
    repo_name = models.TextField(blank=True)
    collaborators = models.TextField(blank=True)
    messages = models.ManyToManyField(Message, blank=True)


def run_query(query, headers):
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()


@receiver(post_save, sender=User)
def create_contact(sender, instance, **kwargs):
    try:
        Contact.objects.get(user=instance)
    except:
        Contact.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_chats(sender, instance, **kwargs):
    user = instance
    result = SocialToken.objects.filter(account__user=user, account__provider="github")
    token = result.first()
    headers = {'Authorization': 'token ' + str(token)}
    query = '''
    {
        viewer {
        repositories(first: 100, affiliations: [OWNER, COLLABORATOR, ORGANIZATION_MEMBER],
                        ownerAffiliations:[OWNER, ORGANIZATION_MEMBER, COLLABORATOR]) {
          totalCount
          nodes{
            name
              owner {
                login
              }
               collaborators {
               nodes {
                 login
               }
              }
            }
          }
       }
    }
    '''
    req = run_query(query=query, headers=headers)
    print(req)
    for repo in req['data']['viewer']['repositories']['nodes']:
        repo_name = repo['name']
        repo_owner = repo['owner']['login']
        collaborators = repo['collaborators']['nodes']
        print(repo_name,repo_owner,collaborators)
        try:
            user = get_object_or_404(User, username=repo_owner)
            print(user)
            repo_owner = get_object_or_404(Contact, user=user)
            print(user, repo_owner)

            collaborator_list = []
            for collaborator in collaborators:
                username = collaborator['login']
                print(username)
                if str(username) == str(repo_owner):
                    collaborator_list.append({str(repo_owner): 'owner'})
                else:
                    collaborator_list.append({collaborator['login']: 'collaborator'})
            print(collaborator_list)
            try:
                RepoChats.objects.get(repo_name=repo_name, collaborators=collaborator_list)

            except:
                chat = RepoChats()
                chat.repo_name = repo_name
                chat.save()
                chat.collaborators = collaborator_list
                chat.save()
        except:
            print('Owner of the  repo is not on Merge')