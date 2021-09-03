from django.db import models
from django.db.models.signals import post_save  # listens just before we commit to the database
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass 

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username 

class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    agent = models.ForeignKey("Agent", on_delete=models.CASCADE)

    #SOURCE_CHOICES = (
    #    ('YouTube', 'YouTube'),
    #    ('Google', 'Google'),
    #    ('Newsletter', 'Newsletter')
    #)
    # This type of fields can help to show the progress of the shipment, other way to do it is on the front end directly
    # but the app would have to be deployed again. 
    #phoned = models.BooleanField(default=False)
    #source = models.CharField(choices=SOURCE_CHOICES, max_length=100)

    #profile_picture = models.ImageField(blank=True, null=True)
    #special_files = models.FileField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # 'organisation' refers to the user that is logged in
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)      # if the user is deleted, the agent will be as well. 


    def __str__(self):
        return self.user.email

        
def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(post_user_created_signal, sender=User)
      