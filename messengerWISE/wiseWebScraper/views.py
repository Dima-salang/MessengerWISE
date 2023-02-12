from django.shortcuts import render
import requests
from django.http import HttpResponse
from bs4 import BeautifulSoup
from .models import Message

# Create your views here.

def webhook(request):
    # get incoming message from FB
    incoming_message = request.POST.get("text")

    # store incoming message in the database
    Message.objects.create(text=incoming_message)

    # scrape Wikipedia for information about the incoming message
    response = requests.get(f"https://en.wikipedia.org/wiki/{incoming_message}")
    soup = BeautifulSoup(response.text, "html.parser")
    first_paragraph = soup.find("p").text

    # return the wikipedia response to fb
    return HttpResponse(first_paragraph)

