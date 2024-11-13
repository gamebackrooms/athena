from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.urls import reverse

from django.http import FileResponse, Http404
from django.http import JsonResponse
from django.http import HttpResponse

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

from django.views.generic.edit import CreateView
from django.views.generic import View


from django.core.paginator import Paginator
from django import template


from django.views.decorators.csrf import csrf_exempt
from django.template.context_processors import csrf

import os
import csv
import io
from io import BytesIO
import socket 

import urllib.request
from django.core.files.base import ContentFile

from django.db.models import Q

from django.utils import timezone  # Import Django's timezone module

import openai

import json
from PIL import Image
import requests
import random 
import uuid
import hashlib

from django.views.decorators.csrf import csrf_exempt
from django.template.context_processors import csrf
from lxml import html
import pandas as pd


from datetime import datetime
from django.utils.dateparse import parse_datetime

from django.core.serializers import serialize

from django.views.decorators.http import require_POST

register = template.Library()
import time 
import re
import os

from .models import Accesstoken
from .models import Game
from .models import Hand
from .models import Player
from .models import Handhistory
from .models import SocialMediaHandle
from .models import TwitterStatus
from .models import UserQuery

from .models import TokenMarketingContent

from .models import Tweet
 
from .models import ConvoLog
from .models import ConversationTopic

from .forms import TokenMarketingContentForm
from .forms import TweetForm 

from .serializers import ConversationTopicSerializer

from .serializers import TwitterStatusSerializer
from .serializers import UserQuerySerializer
from .serializers import ConvoLogSerializer

import base64
import base58
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, get_object_or_404

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser

from .serializers import TwitterStatusSerializer

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate

pokerGPT_version = "00.00.06"
small_blind_size = 10
big_blind_size = 20
bank_default_balance = 1000
bank_default_balance_range = 350

deck = [
    "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "JH", "QH", "KH", "AH",
    "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD", "AD",
    "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC", "AC",
    "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS", "AS"
]
#MY_TOKEN = "DF2LXZ9msqFihobc8MVMo8fL7zPfLjJbuNTR1JMCpump"
MY_TOKEN = "6uVTQwuKrBqrHoZjnRGLbF6q4VfMRn8kMgh4Eoyjpump"
poker_player_types = [{"type": "Drunk Player", "description": "Often makes reckless bets, unpredictable, and can be aggressive."}, {"type": "Sober and Desperate", "description": "Plays cautiously but may make risky moves out of desperation."}, {"type": "Wealthy Player", "description": "Has a lot of chips to play with, may play loose and aggressive."}, {"type": "Professional Player", "description": "Highly skilled, plays strategically, and is hard to read."}, {"type": "Novice Player", "description": "Inexperienced, makes basic mistakes, and is easy to bluff."}, {"type": "Tight Player", "description": "Plays very few hands, only bets with strong cards."}, {"type": "Loose Player", "description": "Plays many hands, often makes large bets with weak hands."}, {"type": "Aggressive Player", "description": "Frequently raises and bets, often tries to intimidate opponents."}, {"type": "Passive Player", "description": "Rarely raises, often calls, and tends to fold under pressure."}, {"type": "Bluffer", "description": "Frequently bluffs, making it hard to tell when they have a good hand."}, {"type": "Calling Station", "description": "Calls almost every bet, rarely folds, and doesn't raise often."}, {"type": "Recreational Player", "description": "Plays for fun, not very skilled, and doesn't take the game too seriously."}, {"type": "Strategist", "description": "Carefully analyzes each move, often follows a calculated game plan."}, {"type": "Experienced Veteran", "description": "Has played for many years, understands the game deeply, and can adapt to different opponents."}, {"type": "Psychologist", "description": "Tries to read opponents' tells and body language to gain an advantage."}]


def admin_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

def about_us(request):
    return render(request, 'about_us.html')

@admin_required
@require_POST
def delete_conversation_topic(request, pk):
    topic = get_object_or_404(ConversationTopic, pk=pk)
    topic.delete()
    return redirect('conversation_topics')

@admin_required
def delete_convo_log(request, id):
    convo_log = get_object_or_404(ConvoLog, id=id)
    convo_log.delete()
    messages.success(request, 'Conversation log deleted successfully.')
    return redirect('index')  # Replace 'convo_log_list' with your list view name


def conversation_topics(request):
    topics = ConversationTopic.objects.all().order_by('-created_date')  # Order by most recent
    
    if request.headers.get('Content-Type') == 'application/json' or request.GET.get('format') == 'json':
        # Prepare data for JSON response
        topics_data = [
            {
                'id': topic.id,
                'title': topic.title,
                'created_date': topic.created_date, 
            }
            for topic in topics
        ]
        return JsonResponse({'topics': topics_data})

    return render(request, 'conversation_topics.html', {'topics': topics})


@csrf_exempt
@admin_required 
@api_view(['POST'])
def create_conversation_topic(request):
    print("create_conversation_topic")
    if request.method == 'POST':
        serializer = ConversationTopicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@admin_required
@api_view(['POST'])
def create_convo_log(request):
    if request.method == 'POST':
        serializer = ConvoLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@admin_required
@api_view(['POST'])
def create_user_query(request):
    if request.method == 'POST':
        serializer = UserQuerySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve all UserQuery records
@api_view(['GET'])
def list_user_queries(request):
    if request.method == 'GET':
        user_queries = UserQuery.objects.all()
        serializer = UserQuerySerializer(user_queries, many=True)
        return Response(serializer.data)

# Retrieve a single UserQuery record by ID
@api_view(['GET'])
def get_user_query(request, query_id):
    try:
        user_query = UserQuery.objects.get(id=query_id)
    except UserQuery.DoesNotExist:
        return Response({'error': 'User query not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UserQuerySerializer(user_query)
        return Response(serializer.data)
 
def convo_log_detail(request, pk):
    convo_log = get_object_or_404(ConvoLog, pk=pk)
    return render(request, 'convo_log_detail.html', {'convo_log': convo_log})


def user_queries_view(request):
    # Fetch all queries from the database 
    #queries = UserQuery.objects.all().order_by('-created_date')
    queries = UserQuery.objects.all().order_by('-created_date')[:50]


    # If the request is an AJAX request, return JSON response
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        json_queries = queries.values('connanicall_action_text', 'username', 'question', 'reasoning', 'response', 'created_date')
        return JsonResponse(list(json_queries), safe=False)

    # Otherwise, return the regular HTML view
    context = {
        'user_queries': queries,
    }
    return render(request, 'user_queries.html', context)

    
@csrf_exempt
@admin_required
def processed_status(request, status_id):
        # Fetch the TwitterStatus object by status_id
    twitter_status = get_object_or_404(TwitterStatus, status_id=status_id)
    
    # Check if the processed field is False and convert it to True 
    twitter_status.processed = True
    twitter_status.save()  # Save the changes
    
    # Response data after the update
    data = {
        'message': 'Status updated successfully',
        'status_id': twitter_status.status_id,
        'processed': twitter_status.processed,
    }
    return JsonResponse(data)
    
    # If already processed, return a message
    data = {'message': 'Status is already processed', 'processed': twitter_status.processed}
    return JsonResponse(data)
    
def twitter_status_detail(request, status_id):
    # Fetch the TwitterStatus object by status_id
    print(status_id)
    twitter_status = get_object_or_404(TwitterStatus, status_id=status_id)
    
    # Prepare the data to be returned as JSON
    data = {
        'x_user': twitter_status.x_user,
        'status_id': twitter_status.status_id,
        'created_by_user': twitter_status.created_by_user,
        'created_at': twitter_status.created_at,
        'processed': twitter_status.processed,
    }
    
    return JsonResponse(data)

class TwitterStatusDetailView(View):
    def get(self, request, status_id):
        # Fetch the TwitterStatus object by status_id
        twitter_status = get_object_or_404(TwitterStatus, status_id=status_id)
        # Prepare the data to be returned as JSON or any other format
        data = {
            'x_user': twitter_status.x_user,
            'status_id': twitter_status.status_id,
            'created_by_user': twitter_status.created_by_user,
            'created_at': twitter_status.created_at,
            'processed': twitter_status.processed,
        }
        return JsonResponse(data)

def extract_twitter_info(url):
    match = re.search(r'https://x\.com/([^/]+)/status/(\d+)', url)
    if match:
        username = match.group(1)
        status_id = match.group(2)
        return username, status_id
    return None, None

# View all TwitterStatus entries (API)
@api_view(['GET'])
def list_twitter_status(request):
    if request.method == 'GET':
        statuses = TwitterStatus.objects.all()
        serializer = TwitterStatusSerializer(statuses, many=True)
        return Response(serializer.data)

@require_POST
def delete_status(request, status_id):
    status = get_object_or_404(TwitterStatus, id=status_id)
    status.delete()
    return redirect('view_twitter_status')  # Replace with the URL name for your status list view



@csrf_exempt
@admin_required
def save_twitter_status(request):
    try:
        # Load the JSON body from the request
        url = request.GET.get('url', 'got empty')   
        created_by_user = request.GET.get('created_by', 'got empty')
        print(url)
        print(created_by_user)
        username, status_id = extract_twitter_info(url)  # Ensure this function is correct
        if username and status_id:
            twitter_status = TwitterStatus(
                x_user=username,
                status_id=status_id,
                created_by_user=created_by_user
            )
            twitter_status.save()
            return JsonResponse({"message": "Twitter status saved successfully."}, status=201)
        else:
            print("Username or status ID is missing")
            return JsonResponse({"error": "Username or status ID is missing."}, status=400)

    except Exception as e:
        print(f"An error occurred: {e}")
        return JsonResponse({"error": "An unexpected error occurred."}, status=500)


def view_twitter_status(request):
    statuses = TwitterStatus.objects.all()
    return render(request, 'twitter_status_list.html', {'statuses': statuses})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


@csrf_exempt
@admin_required
def delete_tweet_by_content(request):
    content = request.GET.get('content')  # Get the content from the query string
    if not content:
        return redirect('tweet_list')  # Redirect if no content is provided

    # Retrieve all tweets that match the content
    tweets = Tweet.objects.filter(content=content)
    if not tweets.exists():
        return redirect('tweet_list')  # Redirect if no tweets are found

    # Delete all tweets with the matching content
    tweets.delete()
    return redirect('tweet_list')  # Redirect to the list after deletion


# View to delete a tweet without confirmation

@csrf_exempt
@admin_required
def delete_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    tweet.delete()  # Delete the tweet immediately
    return redirect('tweet_list')  # Redirect to the list after deletion

def tweet_list(request):
    tweets = Tweet.objects.all()

    # Check if the request is for JSON format
    if request.GET.get('format') == 'json':
        tweet_data = list(tweets.values())  # Convert the QuerySet to a list of dictionaries
        return JsonResponse(tweet_data, safe=False)

    return render(request, 'tweet_list.html', {'tweets': tweets})

@method_decorator(csrf_exempt, name='dispatch')
def create_tweet_api(request):
    if request.method == 'POST':
        try:
            # Parse the JSON request body
            data = json.loads(request.body)
            tweet_url = data.get('url')
            
            # Create and save the new tweet instance
            if tweet_url:
                new_tweet = Tweet(content=tweet_url)  # Assuming you have a 'url' field in the Tweet model
                new_tweet.save()
                
                # Return a success response
                return JsonResponse({"message": "Tweet saved successfully", "id": new_tweet.id}, status=201)
            else:
                return JsonResponse({"error": "No URL provided"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    else:
        return JsonResponse({"error": "POST request required"}, status=405)

# View to create a new tweet

@csrf_exempt
@admin_required
def create_tweet(request):
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tweet_list')  # Redirect to the list after saving
    else:
        form = TweetForm()
    
    return render(request, 'index.html', {'form': form})    

@csrf_exempt
@require_POST
def add_social_media_handle(request):
    try:
        data = json.loads(request.body)
        handle = data.get('handle')
        follower_count = data.get('follower_count')

        if not handle or not isinstance(follower_count, int):
            return JsonResponse({'error': 'Invalid data'}, status=400)

        # Create and save the SocialMediaHandle instance
        SocialMediaHandle.objects.create(handle=handle, follower_count=follower_count)
        return JsonResponse({'message': 'Social media handle added successfully'}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def generate_response():
    authors = ["Mark Twain", "Jane Austen", "George Orwell", "J.K. Rowling", "Ernest Hemingway", "Virginia Woolf", "Leo Tolstoy", "F. Scott Fitzgerald", "Charles Dickens"]

    random_author = random.choice(authors)
    SECRET_KEY = os.getenv('OPENAI_SECRET_KEY')
    openai.api_key = SECRET_KEY
    model_engine = "gpt-3.5-turbo" 
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": "You are a helpful assistant " + random_author},
            {"role": "user", "content": "generate a short tweet about 80 characters long max, about me graduating Schizo University because i am cured and no longer schizo time to connect with alumni, make it positive, funny, intresting and pardoxical"},
        ])

    message_gpt = response.choices[0]['message']['content']
    print("RESPONSE FROM GPT")
    print(message_gpt)
    print("RESPONSE FROM GPT DONE")
    return message_gpt

# View to forward to x.com
def forward_to_x(request): 
    msg = generate_response()
    encoded_msg = urllib.parse.quote(msg.strip('"') + " #schizou $schizou")
    return redirect('https://x.com/intent/post?text=' + encoded_msg)


class TokenMarketingContentCreateView(View):

    def post(self, request, *args, **kwargs):
        marketing_content = request.POST.get('marketing_content')
        contract_address = request.POST.get('contract_address')
        
        if marketing_content and contract_address:
            # Create a new TokenMarketingContent object
            TokenMarketingContent.objects.create(
                marketing_content=marketing_content,
                contract_address=contract_address
            )
            # Return success response
            return JsonResponse({'message': 'Marketing content added successfully!'})
        else:
            # Return error response
            return JsonResponse({'error': 'Both marketing content and contract address are required.'}, status=400)


    def get(self, request, *args, **kwargs):
        return render(request, 'token_marketing_content_form.html')

def toggle_handle_status(request, handle_id):
    handle = get_object_or_404(SocialMediaHandle, id=handle_id)
    handle.is_active = not handle.is_active  # Toggle status
    handle.save()
    return redirect('index')  # Redirect to the list view (update the name if different)


def index(request):
    access_id = request.COOKIES.get('access_id')
    access_token = None
    create_token = False

    try:
        if access_id:
            access_token = Accesstoken.objects.get(access_cookie=access_id)
        else:
            create_token = True
    except Accesstoken.DoesNotExist:
        create_token = True

    if create_token:
        public_key = '0xUN' + generate_id()
        access_id = generate_id()
        token_amount_float = 10.0
        bank_default_balance = 1000
        access_token, created = Accesstoken.objects.get_or_create(
            public_wallet_address=public_key,
            defaults={
                'access_cookie': access_id,
                'token_balance': token_amount_float,
                'bank_balance': bank_default_balance,
            }
        )

    cart_id = request.COOKIES.get('cartId')
    if cart_id is None:
        cart_id = generate_id()

    # Query and sort the social media handles by follower count
    social_media_handles = SocialMediaHandle.objects.all().order_by('-follower_count')

    filter_option = request.GET.get('filter', 'all')
    
    # Filter handles based on the filter_option
    if filter_option == 'active':
        social_media_handles = SocialMediaHandle.objects.filter(is_active=True)
    elif filter_option == 'inactive':
        social_media_handles = SocialMediaHandle.objects.filter(is_active=False)
    else:  # 'all' or any other value
        social_media_handles = SocialMediaHandle.objects.all()


    random_handles = social_media_handles.order_by('?')[:50]

    latest_marketing_content = None


    topic_id = request.GET.get('id')  # Get 'id' from the query string

    if topic_id:
        try:
            # Use the topic_id to get the ConversationTopic title
            topic = ConversationTopic.objects.get(id=topic_id)
            # Filter ConvoLogs by topic title
            convo_logs = ConvoLog.objects.filter(topic=topic.title).order_by('-created_date')
        except ConversationTopic.DoesNotExist:
            convo_logs = ConvoLog.objects.all().order_by('-created_date')
    else:
        convo_logs = ConvoLog.objects.all().order_by('-created_date')


    # Set up pagination for convo_logs
    paginator = Paginator(convo_logs, 25)  # Show 10 logs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form = TweetForm()
    
    context = {
        'access_token': access_token,
        'tokenMintAddress': MY_TOKEN,
        'pokerGPT_version': pokerGPT_version,
        'social_media_handles': random_handles,  # Add this line
        'filter_option': filter_option,
        'latest_marketing_content': latest_marketing_content,  # Add this line
        'form': form,
        'page_obj': page_obj,
        'topic_id': topic_id, 
    }
    response = render(request, 'index.html', context)
    response.set_cookie('access_id', access_id)


    return response

def generate_id():
    return uuid.uuid4().hex

def view_game(request, game_id):
    game = get_object_or_404(Game, game_id=game_id)

    hands = Hand.objects.filter(game_id=game_id)
    handhistorys = Handhistory.objects.filter(game_id=game_id)

    all_players = Player.objects.filter(session_id=game.session_id)
    context = {
        'game': game,
        'hands': hands,  # Add the hands to the context
        'players': all_players, 
        'handhistorys' : handhistorys,
    }  

    return render(request, 'view_game.html', context)

def all_games(request):
    games = Game.objects.all().order_by('-date_created')
    #games = Game.objects.filter(game_state='End of Hand').order_by('-date_created')  # Filter games with state "End of Hand"
        
    paginator = Paginator(games, 10)  # Show 10 games per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}
    return render(request, 'all_games.html', context)

def game_create(request):
    access_id = request.COOKIES.get('access_id')
    access_token = Accesstoken.objects.get(access_cookie=access_id)
    access_token.bank_balance = bank_default_balance
    access_token.save()

    if request.method == "POST":
        number_of_players = int(request.POST.get('number_of_players' ))

        if number_of_players != 0 and request.POST.get( 'player2_type', None) == None: 
            session_id = str(uuid.uuid4())
            players = range(1, number_of_players)
            context = {'poker_player_types': poker_player_types, 'number_of_players': number_of_players, 'poker_player_types': poker_player_types, 'players': players}
            response = render(request, 'game.html', context)
            return response
        else:    
            #[add code]
            players = range(1, number_of_players)
            
            player_types = []
            for player in range(1, number_of_players + 1):
                player_type = request.POST.get(f"player{player}_type", None)
                if player_type == 'Select one' :

                    selected_player_type = random.choice(poker_player_types)
                    player_type = selected_player_type['type']
                    player_types.append(player_type)
                else:    
                    player_types.append(player_type)

                print(f"Player {player} - Type: {player_type}")      

            session_id = str(uuid.uuid4())
            return init_game(request, 0, number_of_players, session_id, player_types)

    else:    
        context = {'poker_player_types': poker_player_types}
        response = render(request, 'game.html', context)
        return response

def init_game(request, current_blind, number_of_players, session_id, player_types):
    access_id = request.COOKIES.get('access_id')
    names = ["Alice", "Bob", "Charlie", "Diana", "Edward", "Fiona", "George", "Hannah", "Ian", "Julia", "Kevin", "Laura", "Michael", "Nina", "Oscar", "Paula", "Quincy", "Rachel", "Steven", "Tina", "Umar", "Violet", "Walter", "Xena", "Yasmine", "Zachary"]

    random.shuffle(deck)
    game_id = str(uuid.uuid4())
    secret_key = str(uuid.uuid4())
    if number_of_players == '2':
        current_player = 1
    else:
        current_player = current_blind + 3  

    # Converting the deck to a comma-separated string
    deck_string = ",".join(deck)

    flop = ",".join(deck[0:3])
    turn = deck[3]
    river = deck[4]
    
    pot_size = small_blind_size + big_blind_size
    # Save game data to Game model
    game = Game.objects.create(
        game_id=game_id,
        session_id=session_id,
        deck=deck_string,
        secret_key=secret_key,
        number_of_players=int(number_of_players),
        current_blind=current_blind,
        pot_size=pot_size,
        current_player=current_player,
        flop=flop,
        turn=turn,
        river=river
    )

    game_object = Game.objects.get(game_id=game_id)

    combined_string = deck_string + secret_key
    # Generate hash (SHA-256 example)
    hash_object = hashlib.sha256(combined_string.encode())
    generated_hash = hash_object.hexdigest()

    public_wallet_address = None
    try:
        access_token = Accesstoken.objects.get(access_cookie=access_id)
        public_wallet_address = access_token.public_wallet_address
        game_object.public_wallet_address = public_wallet_address
        game_object.save()
    except Accesstoken.DoesNotExist:
        # Handle the case where the access token is not found
        public_wallet_address = None
    all_players = Player.objects.filter(session_id=session_id)
    players = Player.objects.filter(session_id=session_id, token_balance__gt=small_blind_size)
    # Create hands for each player
    if not players:
        for i in range(int(number_of_players)):
            # Select two cards for each player (adjust your logic here)
            player_cards = deck[5 + i*2:7 + i*2]
            # Convert player cards to a string representation (adjust as needed)
            player_hand_string = ",".join(player_cards)

            # Generate hand ID for the player's hand
            hand_id = str(uuid.uuid4())
            player_type = "Me"
            bet_amount = 0
            # Determine the player_public_key
            if i == 0:
                player_public_key = "Me"
                access_token.bank_balance -= small_blind_size
                access_token.save()
                bet_amount = small_blind_size
            else:
                player_type = player_types[i-1]
                print(player_type)
                player_public_key = random.choice(names)
                names.remove(player_public_key)

            if i == current_blind:
                player_state = ''
            elif i == current_blind + 1:
                player_state = "Big Blind"
            else:
                player_state = ''

            player_id = str(uuid.uuid4())
            
            lower_bound = max(0, bank_default_balance - bank_default_balance_range)
            upper_bound = bank_default_balance + bank_default_balance_range
            random_number = random.randint(lower_bound, upper_bound)
            bank_default_balance_tmp = random_number

            bet_amount = 0
            if i == 0:
                bank_default_balance_tmp -= small_blind_size
                bet_amount = small_blind_size

            if i == 1:
                bank_default_balance_tmp -= big_blind_size
                bet_amount = big_blind_size

            Player.objects.create(
                player_id=player_id,
                session_id=session_id,
                token_balance=bank_default_balance_tmp,
                player_type=player_type
            )

            Hand.objects.create(
                hand_id=hand_id,
                game_id=game_id,
                player_id=player_id,
                player_public_key=player_public_key,
                hand=player_hand_string,
                player_state=player_state,
                bet_amount=bet_amount
            )
    else:
        print(len(players))
        for player_index, player in enumerate(players):
            player_cards = deck[5 + player_index * 2: 7 + player_index * 2]        
            # Convert player cards to a string representation (adjust as needed)
            player_hand_string = ",".join(player_cards)

            # Generate hand ID for the player's hand
            hand_id = str(uuid.uuid4())
            # Determine the player_public_key
            player_type = "Me"
            if player_index == 0:
                player_public_key = "Me"
            else:
                player_public_key = random.choice(names)
                names.remove(player_public_key)

            if player_index == current_blind:
                player.token_balance -= small_blind_size
                player.save()
                player_state = "Blind"
            elif player_index == current_blind + 1:
                player.token_balance -= big_blind_size
                player.save()
                player_state = "Big Blind"
            else:
                player_state = ''
            
            
            Hand.objects.create(
                hand_id=hand_id,
                game_id=game_id,
                player_id=player.player_id,
                player_public_key=player_public_key,
                hand=player_hand_string,
                player_state=player_state,
                player_type=player.player_type,
                token_balance=player.token_balance
            )

    hands = Hand.objects.filter(game_id=game_id)
    context = {
        'game': game_object,
        'players': all_players, 
        'generated_hash': generated_hash,
        'hands': hands,  # Add the hands to the context
        'small_blind_size': small_blind_size, 
        'big_blind_size': big_blind_size,
        'access_id': access_id, 
    }        
    response = render(request, 'game.html', context)
    return response

def extract_json_from_string(text):
    # Find the first occurrence of a JSON-like object
    pattern = r'\{(?:[^{}]|)*\}'
    match = re.search(pattern, text)
    if match:
        json_str = match.group()
        return json_str
    else:
        return None        
    
def game_next(request):
    cart_id = request.COOKIES.get('cartId')
    access_id = request.COOKIES.get('access_id')
    winning_hand = None
    access_token = Accesstoken.objects.get(access_cookie=access_id)
    poker_game_states = ["Pre-flop", "Flop", "Turn (Fourth Street)", "River (Fifth Street)", "Showdown", "End of Hand"]

    game_id = request.POST.get('game_id')  

    action = request.POST.get('action')
    raise_amount = request.POST.get('raise_amount', 0) 

    game_object = get_object_or_404(Game, game_id=game_id)

    if game_object.public_wallet_address != access_token.public_wallet_address:
        return HttpResponseForbidden("Unauthorized access")

    all_players = Player.objects.filter(session_id=game_object.session_id)
    hands = Hand.objects.filter(game_id=game_id)

    combined_string = game_object.deck + game_object.secret_key
    # Generate hash (SHA-256 example)
    hash_object = hashlib.sha256(combined_string.encode())
    generated_hash = hash_object.hexdigest()
    
    # Find the next active player
    current_player_index = game_object.current_player - 1  # Convert to zero-indexed
    if action == "Fold" or action == "Call" or action == "Raise":
        hand_object = hands[current_player_index]
        #call openai to get reason and analysis of this action 

        openai_var = os.getenv('OPENAI')
        openai.api_key = openai_var
        prompt = 'reponde with json string with fromat {"action": "", "amount": , "reasoning":  } with educational reasoning and action being Raise, Fold or Call with your next move given the following Texas Holdem poker hand ' + hand_object.hand + ' the game is in the following stage ' + game_object.game_state 
        
        if game_object.last_action_play == 'Big Blind':
            prompt += ' previous player is the Big Blind you are under the gun and big blind amount is at ' + str(big_blind_size) + ' number of players in the game ' + str(game_object.number_of_players)
        else:
            prompt += ' previous player did the following ' + game_object.last_action 
        
        prompt +=  ' your chip stack balance is ' + str(access_token.bank_balance)
        
        if game_object.last_action == "Raise":
           prompt +=  ' for the amount of ' + str(game_object.raise_amount)
        
        if game_object.game_state == poker_game_states[1] or game_object.game_state == poker_game_states[2] or game_object.game_state == poker_game_states[3]:
            prompt += ' the flop cards are the following ' + game_object.flop
        if game_object.game_state == poker_game_states[2] or game_object.game_state == poker_game_states[3]:
            prompt += ' the turn card is the following ' + game_object.turn
        if game_object.game_state == poker_game_states[3]:
            prompt += ' the river card is the following ' + game_object.river
        
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": "You are a professional poker player."},
                {"role": "user", "content": prompt},
            ])

        message_gpt = response.choices[0]['message']['content']
        print("RESPONSE FROM GPT")
        print(message_gpt)


        json_data = json.loads(extract_json_from_string(message_gpt))

        reasoning = json_data['reasoning']

        Handhistory.objects.create(
            hand_id=hand_object.hand_id,
            game_id=hand_object.game_id,
            player_id=hand_object.player_id,
            player_public_key=hand_object.player_public_key,
            player_state=action,
            reasoning=reasoning,
            game_state=game_object.game_state,
            player_type='Me'
        )            
        json_data = json.loads(extract_json_from_string(message_gpt))


    if action == "Fold":
        # Handle fold action
        print(action)    
        hand_object = hands[current_player_index]
        hand_object.player_state = "Fold"
        hand_object.save()
        game_object.last_action_play = "Fold"
        game_object.save()
  

    elif action == "Call":
        # Handle call action
        print(action)     
        access_token.bank_balance -= game_object.raise_amount - hand_object.bet_amount
        access_token.save()
        hand_object = hands[current_player_index]
        hand_object.player_state = "Call"
        hand_object.bet_amount = game_object.raise_amount
        hand_object.save()
        game_object.last_action_play = "Call"
        game_object.last_action = "Call"
        game_object.save()

    elif action == "Check":
        hand_object = hands[current_player_index]
        hand_object.player_state = "Check"
        hand_object.save()
        game_object.last_action_play = "Check"
        game_object.save()

    elif action == "Raise":
        # Handle raise action
        access_token.bank_balance -= int(raise_amount) - hand_object.bet_amount
        access_token.save()
        game_object.pot_size += int(raise_amount)  
        hand_object = hands[current_player_index]
        hand_object.player_state = "Raise"
        game_object.last_action_play = "Raise"
        game_object.last_action = "Raise"
        game_object.raise_amount = int(raise_amount)
        hand_object.save()
        game_object.save()
        game_state_manager_action(game_object, hands, all_players, current_player_index) 

    elif action == "Next":
        # Handle next action (advance to the next player)
        hand_object = hands[current_player_index]
        player = Player.objects.get(player_id=hand_object.player_id)

        openai_var = os.getenv('OPENAI')
        openai.api_key = openai_var
        prompt = 'reponde with json string with fromat {"action": "", "amount": , "reasoning":  } with reasoning and action being Raise, Fold or Call with your next move given the following Texas Holdem poker hand ' + hand_object.hand + ' the game is in the following stage ' + game_object.game_state 
        
        if game_object.last_action_play == 'Big Blind':
            prompt += ' previous player is the Big Blind you are under the gun and big blind amount is at ' + str(big_blind_size) + ' number of players in the game ' + str(game_object.number_of_players)
        else:
            prompt += ' previous player did the following ' + game_object.last_action 
        
        prompt +=  ' your chip stack balance is ' + str(player.token_balance)
        
        if game_object.last_action == "Raise":
           prompt +=  ' for the amount of ' + str(game_object.raise_amount)
        
        if game_object.game_state == poker_game_states[1] or game_object.game_state == poker_game_states[2] or game_object.game_state == poker_game_states[3]:
            prompt += ' the flop cards are the following ' + game_object.flop
        if game_object.game_state == poker_game_states[2] or game_object.game_state == poker_game_states[3]:
            prompt += ' the turn card is the following ' + game_object.turn
        if game_object.game_state == poker_game_states[3]:
            prompt += ' the river card is the following ' + game_object.river

        prompt += ' remember you are a ' + player.player_type + " poker player."    
        
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": "You are a persona of a " + player.player_type + " poker player."},
                {"role": "user", "content": prompt},
            ])

        message_gpt = response.choices[0]['message']['content']
        print("RESPONSE FROM GPT")
        print(message_gpt)
        json_data = json.loads(extract_json_from_string(message_gpt))

        if json_data:
            print("Extracted JSON:", json_data)
            print(json_data['action'])       
            action = json_data['action']

            # Now check if action is "Raise"
            if action == "Raise":
                print("Action is Raise")
                game_object.last_action_play = json_data['action']
                game_object.last_action = json_data['action']                     
                game_object.pot_size += int(json_data['amount']) - hand_object.bet_amount
                game_object.raise_amount += int(json_data['amount']) 
                game_object.save()
                player.token_balance -= game_object.raise_amount + int(json_data['amount']) - hand_object.bet_amount
                player.save()
                hand_object.bet_amount = game_object.raise_amount + game_object.raise_amount
                hand_object.save()
                game_state_manager_action(game_object, hands, all_players, current_player_index) 

                # Your code logic when action is Raise
            elif action == "Call":  
                game_object.last_action_play = json_data['action']
                game_object.last_action = json_data['action']     
                game_object.save()
                if game_object.raise_amount == 0:
                    player.token_balance -= big_blind_size
                    player.save()                  
                else:    
                    game_object.pot_size += game_object.raise_amount - hand_object.bet_amount
                    game_object.save()
                    player.token_balance -= game_object.raise_amount - hand_object.bet_amount
                    player.save()                  
                    hand_object.bet_amount = game_object.raise_amount
                    hand_object.save()
            else:
                game_object.last_action_play = json_data['action']
                print("Action is not Raise")
                #game_object.raise_amount = 0
                # Your code logic when action is not Raise

            if player.token_balance < 0: 
                hand_object.player_state = 'All In' 
            else:
                hand_object.player_state = json_data['action']   

            hand_object.save()  

            reasoning = json_data['reasoning']
            print(reasoning)    
            #ARM
            
            Handhistory.objects.create(
                hand_id=hand_object.hand_id,
                game_id=hand_object.game_id,
                player_id=hand_object.player_id,
                player_public_key=hand_object.player_public_key,
                player_state=hand_object.player_state,
                game_state=game_object.game_state,
                reasoning=reasoning,
                player_type=player.player_type
            )            
            # Now you can parse json_data using json.loads() if needed
        else:
            print("No JSON object found in the string.")


        print("RESPONSE FROM GPT DONE")



    hands = Hand.objects.filter(game_id=game_id)

    while True:
        current_player_index = (current_player_index + 1) % game_object.number_of_players
        if current_player_index >= len(hands):
            break  # Should not happen if number_of_players <= len(hands)
        
        # Check if this player's hand state is not "fold"
        if hands[current_player_index].player_state != "Fold" and hands[current_player_index].player_state != "All In" :
            game_object.current_player = current_player_index + 1  # Convert back to one-indexed
            game_object.save()
            break

    # UPDING THE STATE ENGINE MANAGER HERE 
    # NEED TO CREATE ABILITY TO RERAISE GO IN CIRCLES

    remaining_hands = Hand.objects.filter(game_id=game_id).exclude(player_state__in=['Fold', 'All In'])
    num_remaining_hands = remaining_hands.count()
    if num_remaining_hands == 1:
        game_object.game_state = poker_game_states[-1]  # Set game state to the last item in the array
        winning_hand = remaining_hands.first()
        game_object.save()

    
    no_empty_player_states = not Hand.objects.filter(game_id=game_id, player_state='').exists()

    if no_empty_player_states:
        print("There are no hands with empty player_state.")
        current_index = poker_game_states.index(game_object.game_state)
        if current_index + 1 < len(poker_game_states):
            game_object.game_state = poker_game_states[current_index+1]
            game_object.raise_amount = 0
            game_object.save()            

            if game_object.game_state == poker_game_states[-1] :
                found_winner = game_state_manager_action_find_winner(game_object, hands, all_players)
            else :    
                for index, hand in enumerate(hands):
                    if hand.player_state != "Fold" and hand.player_state != "All In":
                        hand.player_state = ''
                        hand.bet_amount = 0
                        hand.save()    
            

        else:
            game_object.game_state = poker_game_states[-1]
            game_object.save()
            found_winner = game_state_manager_action_find_winner(game_object, hands, all_players)
            #current_blind = game_object.current_blind + 1 
            #return init_game(request, current_blind, game_object.number_of_players, game_object.session_id)
    
    #game_object = game_state_manager(game_object, hands, all_players, game_object.current_player, False, False, 0, action)
    
    
    hash_object = hashlib.sha256(combined_string.encode())
    
    hands = Hand.objects.filter(game_id=game_id)
    game_object = get_object_or_404(Game, game_id=game_id)
    handhistorys = Handhistory.objects.filter(game_id=game_id)
    has_raise_or_big_blind = Hand.objects.filter(
        Q(game_id=game_id) & Q(player_state__in=['Raise', 'Big Blind'])
    ).exists()


    context = {
        'game': game_object,
        'generated_hash': generated_hash,
        'hands': hands,  # Add the hands to the context
        'players': all_players,
        'small_blind_size': small_blind_size,  
        'big_blind_size': big_blind_size,
        'access_id': access_id, 
        'winning_hand': winning_hand,
        'handhistorys' : handhistorys,
        'has_raise_or_big_blind': has_raise_or_big_blind
    }        
    
    response = render(request, 'game.html', context)
    return response


def verify_signature(request):
    if request.method == 'GET':
        public_key = request.GET.get('publicKey', '').strip()  # Ensure no leading/trailing spaces
        print(public_key)
        signature_base64 = request.GET.get('signature', '')
        
        print(signature_base64)
        
        message_or_transaction = 'Hello from ChatGPTdotfun!'
        
        try:
            
            # Decode the base64 signature into bytes
            signature_bytes = base64.b64decode(signature_base64)
            
            # Prepare the message as bytes
            message_bytes = message_or_transaction.encode('utf-8')

            # Decode the Solana public key from Base58 to bytes
            public_key_bytes = base58.b58decode(public_key)

            # Create a VerifyKey instance
            verify_key = VerifyKey(public_key_bytes)
            #print('Made it here')
            verify_key.verify(message_bytes, signature_bytes)
            #print("Signature is valid!")

             
            url = "https://solana-mainnet.g.alchemy.com/v2/t7AGL7qRXHF4jvodUVH7gWn3lvSfk_jl"
            headers = {"accept": "application/json", "content-type": "application/json"}

            payload = {
                "id": 1,
                "jsonrpc": "2.0",
                "method": "getTokenAccountsByOwner",
                "params": [
                    public_key,
                    {"mint": MY_TOKEN},
                    {"encoding": "jsonParsed"},
                ],
            }
            response = requests.post(url, json=payload, headers=headers)

            try:
                token_amount_str = response.json()["result"]["value"][0]["account"]["data"]["parsed"]["info"]["tokenAmount"]["uiAmount"]
                print("Test next")
                token_amount_float = float(token_amount_str)
            except (KeyError, IndexError, TypeError, ValueError) as e:
                token_amount_float = 0
                print(f"An error occurred: {e}")

            
            access_id = request.COOKIES.get('access_id')

            try:
                access_token = Accesstoken.objects.get(access_cookie=access_id)
                public_wallet_address = access_token.public_wallet_address
            except Accesstoken.DoesNotExist:
                # Handle the case where the access token is not found
                public_wallet_address = None

            if token_amount_float >= 1000000:    
                print("Token amount is greater than 1,000,000")
                access_id = generate_id()
                print(access_id)
                response_data = {
                    'valid': True,
                    'message': 'Signature is valid.'
                }
                response = JsonResponse(response_data)
                response.set_cookie('access_id', access_id)     
 
                access_token, created = Accesstoken.objects.get_or_create(
                    public_wallet_address=public_key,
                    defaults={
                        'access_cookie': access_id,
                        'token_balance': token_amount_float,
                        'bank_balance' : bank_default_balance,
                    }
                )

                # If not created, update existing access_token
                if not created:
                    access_token.access_cookie = access_id
                    access_token.token_balance = token_amount_float
                    access_token.save()

                # Optionally, you can print or log the instance for verification
                print(access_token)                

                return response    
            else:
                print("Token amount is not greater than 1,000,000")
                print("Token Amount as Float:", token_amount_float)
                return JsonResponse({'valid': True, 'message': 'Signature is valid.'})
        except BadSignatureError:
            print("Signature verification failed: Invalid signature")
            return JsonResponse({'valid': False, 'message': 'Invalid signature'})
        except Exception as e:
            print(f"Signature verification failed: {str(e)}")
            return JsonResponse({'valid': False, 'message': str(e)}, status=500)



def game_state_manager_action(game, hands, players, current_player_index):

    for hand in hands:
        hand.last_raise = False
        hand.save()

    hand_object = hands[current_player_index]
    hand_object.last_raise = True
    hand_object.save()


    update_hands = Hand.objects.filter(
        Q(game_id=game.game_id),
        Q(player_state='Check') | Q(player_state='Call')| Q(player_state='Raise') | Q(player_state='Blind') | Q(player_state='Big Blind')
    )
    if update_hands:
        for index, hand in enumerate(update_hands): 
            if hand.last_raise != True :
                hand.player_state = ''
                hand.save() 
 
 
def game_state_manager_action_find_winner(game, hands, players):


    openai_var = os.getenv('OPENAI')
    openai.api_key = openai_var
    prompt = 'reponde with json string with fromat {"winner": "", "winning_hand": ""} with winner being the plyer number and winning_hand being the Royal Flush, Straight Flush, Four of a Kind, Full House, Flush, Straight, Three of a Kind, Two Pair, One Pair, High Card.' 
    print(prompt)
    for index, player in enumerate(players):
        hand = hands[index]
        prompt += f' player number {index + 1} has the following cards {hand.hand} last action was {hand.player_state}.\n'
        print(f"Counter: {index + 1}, Player ID: {player.id}")
    
    prompt +=  ' the following cards are the flop ' + str(game.flop)     
    prompt +=  ' the following card is the turn ' + str(game.turn)     
    prompt +=  ' the following card is the river ' + str(game.river)   
    prompt +=  ' make sure you are correct when juding the player hand and consider their last action if it is Fold do not count them as winner'     
    
    print(prompt)

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": "You are a persona of a professional poker player."},
            {"role": "user", "content": prompt},
        ])

    message_gpt = response.choices[0]['message']['content']
    print("RESPONSE FROM GPT")
    print(message_gpt)
    json_data = json.loads(extract_json_from_string(message_gpt))

    if json_data:
        print("Extracted Winner JSON:", json_data)
        print(json_data['winner'])       
        winner = json_data['winner']
        game.winner = int(winner) -1
        game.winning_hand = json_data['winning_hand']
        game.save()
 
