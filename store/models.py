from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import BaseUserManager
import os
import uuid
import re

def default_uuid():
    return str(uuid.uuid4())

class UserManager(BaseUserManager):
    def get_by_natural_key(self, username):
        return self.get(username=username)
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    company_phone = models.CharField(max_length=255, blank=True)
    company_email_address = models.CharField(max_length=255, blank=True)
    date_joined = models.TimeField(null=True)
    billing_address_line1 = models.CharField(max_length=255, blank=True)
    billing_address_line2 = models.CharField(max_length=255, blank=True)
    billing_city = models.CharField(max_length=255, blank=True)
    billing_state = models.CharField(max_length=255, blank=True)
    billing_zipcode = models.CharField(max_length=255, blank=True)
    billing_country = models.CharField(max_length=255, blank=True)
    shipping_address_line1 = models.CharField(max_length=255, blank=True)
    shipping_address_line2 = models.CharField(max_length=255, blank=True)
    shipping_city = models.CharField(max_length=255, blank=True)
    shipping_state = models.CharField(max_length=255, blank=True)
    shipping_zipcode = models.CharField(max_length=255, blank=True)
    shipping_country = models.CharField(max_length=255, blank=True)
    hrn_company_code = models.CharField(max_length=255, blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    objects = UserManager()

def category_upload_to(instance, filename):
    name, ext = os.path.splitext(filename)
    return f"category/{instance.id}.png"

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=category_upload_to, null=True, blank=True)
    def __str__(self):
        return self.name


def brand_upload_to(instance, filename):
    name, ext = os.path.splitext(filename)
    return f"brand/{instance.id}.png"

class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=brand_upload_to, null=True, blank=True)
    website = models.URLField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.name

def product_upload_to(instance, filename):
    name, ext = os.path.splitext(filename)
    return f"product/{instance.id}.png"

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    sku = models.CharField(max_length=255, default=default_uuid)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    wholesale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    your_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    source_upload = models.TextField(max_length=255, null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product_image = models.ImageField(upload_to=product_upload_to, null=True, blank=True)
    display_priority = models.IntegerField(null=True, blank=True)
    quantity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    wholesale_price_item_json = models.TextField(null=True)
    def __str__(self):
        return self.name

class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    external_id = models.CharField(max_length=255, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    checked_out = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    paid_transaction_id = models.CharField(max_length=255, blank=True)
    billing_address_line1 = models.CharField(max_length=255, blank=True)
    billing_address_line2 = models.CharField(max_length=255, blank=True)
    billing_city = models.CharField(max_length=255, blank=True)
    billing_state = models.CharField(max_length=255, blank=True)
    billing_zipcode = models.CharField(max_length=255, blank=True)
    billing_country = models.CharField(max_length=255, blank=True)
    shipping_address_line1 = models.CharField(max_length=255, blank=True)
    shipping_address_line2 = models.CharField(max_length=255, blank=True)
    shipping_city = models.CharField(max_length=255, blank=True)
    shipping_state = models.CharField(max_length=255, blank=True)
    shipping_zipcode = models.CharField(max_length=255, blank=True)
    shipping_country = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='carts', null=True, blank=True)
    def __str__(self):
        return self.cart_id

class CartProduct(models.Model):
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class APIData(models.Model):
    data = models.JSONField(null=True)  # Store JSON data
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp when the data was saved
    is_retrieving = models.BooleanField(default=False)  # Boolean indicating whether data is being retrieved

    def __str__(self):
        return f"API Data saved at {self.timestamp}"


class Token(models.Model):
    mint = models.CharField(max_length=100, unique=True, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    symbol = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image_uri = models.URLField(null=True, blank=True)
    metadata_uri = models.URLField(null=True, blank=True)
    twitter = models.CharField(max_length=300, null=True, blank=True)
    telegram = models.CharField(max_length=100, null=True, blank=True)
    bonding_curve = models.CharField(max_length=100, null=True, blank=True)
    associated_bonding_curve = models.CharField(max_length=100, null=True, blank=True)
    creator = models.CharField(max_length=100, null=True, blank=True)
    created_timestamp = models.DateTimeField(null=True, blank=True)
    raydium_pool = models.CharField(max_length=100, null=True, blank=True)
    complete = models.BooleanField(default=False)
    virtual_sol_reserves = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    virtual_token_reserves = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    hidden = models.BooleanField(default=False)
    total_supply = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    show_name = models.BooleanField(default=False)
    last_trade_timestamp = models.DateTimeField(null=True, blank=True)
    king_of_the_hill_timestamp = models.DateTimeField(null=True, blank=True)
    market_cap = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    reply_count = models.IntegerField(null=True, blank=True)
    last_reply = models.CharField(max_length=100, null=True, blank=True)
    nsfw = models.BooleanField(default=False)
    market_id = models.IntegerField(null=True, blank=True)
    market_id_two = models.IntegerField(null=True, blank=True)
    inverted = models.BooleanField(default=False)
    username = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.URLField(null=True, blank=True)
    usd_market_cap = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    ai_analysis = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name  # or any other field you want to represent the object with

class Accesstoken(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    access_cookie = models.CharField(max_length=255)
    public_wallet_address = models.CharField(max_length=255, unique=True)
    token_balance = models.FloatField()
    is_scam_filter_on = models.BooleanField(default=False)
    bank_balance = models.IntegerField()
    def __str__(self):
        return f'{self.public_wallet_address} - {self.access_cookie}'

class RaidLink(models.Model):
    token_mint = models.CharField(max_length=100)
    url = models.URLField()
    click_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)

    def __str__(self):
        return f"RaidLink(token_mint={self.token_mint}, url={self.url}, click_count={self.click_count}, created_at={self.created_at}, created_by={self.created_by.username})"

class RaidLink(models.Model):
    token_mint = models.CharField(max_length=100)
    url = models.URLField()
    click_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)

    def __str__(self):
        return f"RaidLink(token_mint={self.token_mint}, url={self.url}, click_count={self.click_count}, created_at={self.created_at}, created_by={self.created_by.username})"

class Game(models.Model):
    game_id = models.TextField(unique=True)
    session_id = models.TextField(null=True)
    deck = models.CharField(max_length=159)
    public_wallet_address = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    secret_key = models.TextField(unique=True)
    number_of_players = models.IntegerField()
    current_blind = models.IntegerField(default=0)
    current_player = models.IntegerField(default=0)
    pot_size = models.IntegerField(default=0)
    game_state = models.TextField(default="Pre-flop")
    last_action_play = models.TextField(default="Big Blind")
    last_action = models.TextField(default="Big Blind")
    raise_amount = models.IntegerField(default=0)
    flop = models.CharField(max_length=8)
    turn = models.CharField(max_length=2)
    river = models.CharField(max_length=2)
    winner = models.IntegerField(default=0)
    winning_hand = models.CharField(max_length=20)

    def __str__(self):
        return self.game_id  # Or any other field you want to display

    class Meta:
        verbose_name = "Game"
        verbose_name_plural = "Games"


class Hand(models.Model):
    hand_id = models.TextField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    game_id = models.TextField()
    player_id = models.TextField(null=True)
    player_public_key = models.TextField()
    hand = models.TextField()
    player_state_last = models.TextField()
    player_state = models.TextField()
    last_raise = models.BooleanField(default=False)
    bet_amount = models.IntegerField(default=0)

    def __str__(self):
        return self.hand_id  # Or any other field you want to display

    class Meta:
        verbose_name = "Hand"
        verbose_name_plural = "Hands"

class Player(models.Model):
    player_id = models.TextField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    session_id = models.TextField()
    token_balance = models.FloatField()
    player_type = models.TextField()
    def __str__(self):
        return self.hand_id  # Or any other field you want to display

    class Player:
        verbose_name = "Player"
        verbose_name_plural = "Players"

class Handhistory(models.Model):
    hand_id = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    game_id = models.TextField()
    player_id = models.TextField(null=True)
    player_public_key = models.TextField()
    hand = models.TextField()
    player_state = models.TextField()
    reasoning = models.TextField()
    game_state = models.TextField()
    player_type = models.TextField(null=True)
    token_balance = models.FloatField(null=True)

    def __str__(self):
        return self.hand_id  # Or any other field you want to display

    class Handhistory:
        verbose_name = "Handhistory"
        verbose_name_plural = "Handhistorys"

class SocialMediaHandle(models.Model):
    handle = models.CharField(max_length=255, unique=True)
    follower_count = models.PositiveIntegerField()
    is_active = models.BooleanField(default=False)  # New field for active indicator

    def __str__(self):
        return f"{self.handle} - {self.follower_count} followers"


class TokenMarketingContent(models.Model):
    marketing_content = models.TextField()
    contract_address = models.CharField(max_length=42)  # Assuming a typical length for contract addresses
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Marketing Content for {self.contract_address} at {self.timestamp}"


class Tweet(models.Model):
    content = models.TextField()  # The text content of the tweet
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the tweet was created
    is_processed = models.BooleanField(default=False)  # Indicates if the tweet has been processed
    
    def __str__(self):
        return self.content[:50]  # Display the first 50 characters of the tweet

    class Meta:
        ordering = ['-created_at']  # Sort by most recent tweets

class TwitterStatus(models.Model):
    x_user = models.CharField(max_length=100, blank=True)
    status_id = models.CharField(max_length=20, unique=True, null=False)  # Make status_id unique and not nullable
    created_by_user = models.CharField(max_length=150)  # Stores username or user identifier
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of record creation
    processed = models.BooleanField(default=False)  # Indicates if the status has been processed

    def save(self, *args, **kwargs):
        super(TwitterStatus, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.x_user} - {self.status_id}"

class UserQuery(models.Model): 
    created_date = models.DateTimeField(auto_now_add=True)  # Timestamp of record creation
    username = models.CharField(max_length=255)
    question = models.TextField()
    reasoning = models.TextField()
    response = models.TextField()
    connanicall_action_text = models.TextField(null=True, blank=True)  # New field

    def __str__(self):
        return f"Question by {self.username} at {self.created_date}"
    

class ConvoLog(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)  # Timestamp of record creation
    username = models.CharField(max_length=255)
    topic = models.CharField(max_length=1000)  # New field for topic
    from_user = models.CharField(max_length=255)  # New field for 'from'
    to_users = models.CharField(max_length=255)  # New field for 'to'
    message = models.TextField()  # New field for message
    processed = models.BooleanField(default=False)  # New field for processed status
    upvote_count = models.IntegerField(default=0) 
    def __str__(self):
        return f"Question by {self.username} at {self.created_date}"
 
class ConversationTopic(models.Model):
    title = models.CharField(max_length=1000)            # Title of the conversation topic
    created_date = models.DateTimeField(auto_now_add=True)  # Timestamp of record creation

    def __str__(self):
        return self.title    
    
class Comment(models.Model):
    wallet_id = models.CharField(max_length=255)
    token_balance = models.DecimalField(max_digits=20, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    comment_signed = models.TextField()
    ip_address = models.GenericIPAddressField()
    convo_log_id = models.CharField(max_length=255)
    is_visible = models.BooleanField(default=True)
    upvote_count = models.IntegerField(default=0) 

    def __str__(self):
        return f"Comment by {self.wallet_id} on {self.date}"


class Room(models.Model):
    id = models.AutoField(primary_key=True)  # Default primary key
    external_id = models.CharField(max_length=255, unique=True)  # External ID field
    external_date_created = models.DateTimeField()  # External date created field
    created_at = models.DateTimeField(auto_now_add=True)  # Internal creation timestamp

    def __str__(self):
        return self.external_id

    class Meta:
        db_table = 'rooms'  # Explicitly define the table name
        ordering = ['-created_at']  # Optional: order by newest created first

class Relationship(models.Model):
    id = models.AutoField(primary_key=True)  # Default primary key
    user_a = models.CharField(max_length=255)  # Representing userA
    user_b = models.CharField(max_length=255)  # Representing userB
    status = models.CharField(max_length=50)  # Relationship status
    user_id = models.CharField(max_length=255)  # Representing userId (additional identifier)
    created_at_external = models.DateTimeField()  # External creation timestamp
    created_at = models.DateTimeField(auto_now_add=True)  # Internal creation timestamp

    def __str__(self):
        return f"{self.user_a} - {self.user_b} ({self.status})"

    class Meta:
        db_table = 'relationships'  # Explicitly define the table name
        ordering = ['-created_at']  # Optional: order by newest created first        

class Participant(models.Model):
    id = models.AutoField(primary_key=True)  # Default primary key
    user_id = models.CharField(max_length=255)  # User ID field
    room_id = models.CharField(max_length=255)  # Room ID field
    user_state = models.CharField(max_length=50)  # User state in the room
    last_message_read = models.DateTimeField(null=True, blank=True)  # Timestamp of the last message read
    created_at_external = models.DateTimeField()  # External creation timestamp
    created_at = models.DateTimeField(auto_now_add=True)  # Internal creation timestamp

    def __str__(self):
        return f"User {self.user_id} in Room {self.room_id} ({self.user_state})"

    class Meta:
        db_table = 'participants'  # Explicitly define the table name
        ordering = ['-created_at']  # Optional: order by newest created first

class Goal(models.Model):
    id = models.AutoField(primary_key=True)  # Default primary key
    user_id = models.CharField(max_length=255)  # User ID field
    name = models.CharField(max_length=255)  # Goal name
    status = models.CharField(max_length=50)  # Status of the goal
    description = models.TextField(null=True, blank=True)  # Detailed description of the goal
    room_id = models.CharField(max_length=255, null=True, blank=True)  # Associated room ID
    objectives = models.TextField(null=True, blank=True)  # Objectives in a serialized format
    created_at_external = models.DateTimeField()  # External creation timestamp
    created_at = models.DateTimeField(auto_now_add=True)  # Internal creation timestamp

    def __str__(self):
        return f"Goal: {self.name} (Status: {self.status})"

    class Meta:
        db_table = 'goals'  # Explicit table name
        ordering = ['-created_at']  # Optional: order by newest created first

class Log(models.Model):
    id = models.AutoField(primary_key=True)  # Default primary key
    user_id = models.CharField(max_length=255)  # User ID field
    body = models.TextField()  # Log content
    type = models.CharField(max_length=50)  # Log type
    room_id = models.CharField(max_length=255, null=True, blank=True)  # Associated room ID
    created_at_external = models.DateTimeField()  # External creation timestamp
    created_at = models.DateTimeField(auto_now_add=True)  # Internal creation timestamp

    def __str__(self):
        return f"Log by User {self.user_id} (Type: {self.type})"

    class Meta:
        db_table = 'logs'  # Explicit table name
        ordering = ['-created_at']  # Optional: order by newest created first


class Memory(models.Model):
    id = models.AutoField(primary_key=True)  # Default primary key
    external_id = models.CharField(max_length=255, unique=True) 
    type = models.CharField(max_length=100)  # Type of memory
    created_at_external = models.DateTimeField()  # External creation timestamp
    created_at = models.DateTimeField(auto_now_add=True)  # Internal creation timestamp
    content = models.TextField()  # Memory content
    embedding = models.TextField(null=True, blank=True)  # Serialized embedding data
    user_id = models.CharField(max_length=255)  # User ID associated with the memory
    room_id = models.CharField(max_length=255, null=True, blank=True)  # Associated room ID
    agent_id = models.CharField(max_length=255, null=True, blank=True)  # Associated agent ID
    unique = models.BooleanField(default=False)  # Indicates if the memory is unique

    def __str__(self):
        return f"Memory {self.id} - {self.type}"

    class Meta:
        db_table = 'memories'  # Explicit table name
        ordering = ['-created_at']  # Optional: order by newest created first

class Account(models.Model):
    id = models.AutoField(primary_key=True)  # Default primary key
    name = models.CharField(max_length=255)  # Full name of the account holder
    username = models.CharField(max_length=150, unique=True)  # Username, must be unique
    email = models.EmailField(unique=True)  # Email address, must be unique
    avatar_url = models.URLField(max_length=500, null=True, blank=True)  # Optional URL to the avatar image
    details = models.TextField(null=True, blank=True)  # Additional details about the account
    created_at_external = models.DateTimeField()  # External creation timestamp
    created_at = models.DateTimeField(auto_now_add=True)  # Internal creation timestamp

    def __str__(self):
        return f"{self.username} ({self.email})"

    class Meta:
        db_table = 'accounts'  # Explicitly define the table name
        ordering = ['-created_at']  # Optional: order by newest created first
