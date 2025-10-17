from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver




class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')

    def __str__(self):
        return self.user.username



class CurrentBalance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    current_balance = models.FloatField(default = 0)

    def __str__(self) -> str:
        return f"{self.user.username}'s balance: {self.current_balance}"
    


class TrackingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_balance = models.ForeignKey(CurrentBalance , on_delete= models.CASCADE)
    amount = models.FloatField()
    expense_type = models.CharField(choices =(('CREDIT' , 'CREDIT'), ('DEBIT', 'DEBIT')),max_length = 200)
    description = models.CharField(max_length = 200)
    created_at = models.DateTimeField(auto_now = True)
    created_at = models.DateTimeField(auto_now_add = True)


    def __str__(self) -> str:
        return f"{self.user.username}: {self.amount} for {self.description} ({self.expense_type})"
    


class RequestLogs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    request_info = models.TextField()
    request_type = models.CharField(max_length = 100)
    request_method = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.user.username if self.user else 'System'} - {self.request_type}"



@receiver(post_save, sender=User)
def create_user_balance(sender, instance, created, **kwargs):
    if created:
        CurrentBalance.objects.create(user=instance)

