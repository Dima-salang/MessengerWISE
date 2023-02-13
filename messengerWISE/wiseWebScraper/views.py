from django.shortcuts import render
from django.utils.decorators import method_decorator
import requests
import json
from django.http import HttpResponse
from bs4 import BeautifulSoup
from .models import Message
from django.views.generic import View, TemplateView
from django.views.decorators.csrf import csrf_exempt
import wikipediaapi

VERIFY_TOKEN = "EAAIOelghIbABAIcWoYerYE9yzmnHc3og2qFp2ZCG5YP3W5jgy4Xa7YksGBlHs3EraKlztDzSkHcy4HZCmC9EWv5O1glWWOCzn6AD0ZARdn825kAgjofkSiT1LtebxmRYuAOtCDYYIa5PrnziVyOR1VQ8UpiZBGkWBKcKTr3l0T7m1LIlNHj4cFoTUe4Cdm8ZD"


# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class WebHook(View):

    def get(self, request, *args, **kwargs):

        if request.method == "GET":
            if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
                return HttpResponse(self.request.GET['hub.challenge'])
            else:
                return HttpResponse('Error, invalid token')

    def post(self, request, *args, **kwargs):
    
        if request.method == "POST":

            incoming_message = json.loads(request.body.decode('utf-8'))
            print("Got message:", incoming_message)
            wiki_wiki = wikipediaapi.Wikipedia('en')
            print("Scraping...")
            
            
            
            for entry in incoming_message["entry"]:
                for message in entry["messaging"]:
                    if "message" in message:
                        sender_id = message["sender"]["id"]
                        article_title = message["message"].get("text")
                        wiki_page = wiki_wiki.page(f'{article_title}')
                        if wiki_page.exists():
                            response = wiki_page.summary
                            print("Scrape complete for ", article_title)
                            self.send_message(sender_id, response)
                        else:
                            return HttpResponse("Does not exist")
            return HttpResponse()


    def send_message(self, recipient_id, message_text):
        params = {
            "access_token": VERIFY_TOKEN
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": message_text
            }
        })

        r = requests.post("https://graph.facebook.com/v9.0/me/messages", params=params, headers=headers, data=data)
        

        

class PrivacyPolicyView(TemplateView):
    template_name = 'privacy-policy.html'

class TermsAndService(TemplateView):
    template_name = 'terms-service.html'
