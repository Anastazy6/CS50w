from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import CharField


class User(AbstractUser):
    
    def __str__(self):
        return f"{self.username}"


class Post(models.Model):
    author    = models.ForeignKey     (User, on_delete=models.CASCADE, related_name='posts')
    body      = models.CharField      (max_length=4096)
    likes     = models.ManyToManyField(User,          blank=True,      related_name='likes')
    timestamp = models.DateTimeField  (auto_now_add=True)
    title     = models.CharField      (max_length=64, blank=True)
    
    def get_author(self):
        return self.author

    def total_likes(self):
        return self.likes.all().count()

    def get_reactions(self, user=None):
        reactions = {}

        for reaction_obj in self.reactions.all():
            category = reaction_obj.category.reaction
            if category in reactions.keys():
                reactions[category]['count'] += 1
            else:
                reactions[category]          = {}
                reactions[category]['emoji'] = reaction_obj.category.emoji
                reactions[category]['count'] = 1
        if user:
            user_reaction = self.reactions.filter(user=user)
            if len(user_reaction) == 1:
                key = str(user_reaction[0].category.reaction)
                reactions[key]['your_reaction'] = True
        return reactions

    def __str__(self):
        title = self.title if len(self.title) <= 26 else f"{self.title[0:25]}[...]"
        body  = self.body  if len(self.body)  <= 61 else f"{self.body[0:60]}[...]"

        return f"Post #{self.id}: <{title}>  |  {body} | by {self.author}"



class Follower(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers') # obserwujący
    followed  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed')  # obserwowany



# More specific reactions than a siple like. A like can be used to agree with a post's author even if the
#   content is depressing, angering etc. These reactions are meant to be more specific. Someone lost a cat? Like and 'sad'.
#   Some shitty dictator started a war and the post's author is spreading the news? Like and 'angry'.
class ReactionCategory(models.Model):
    reaction  = models.CharField(max_length=32)
    emoji     = models.CharField(max_length=8) # UTF-8 emoji code in an HTML-readable format

    class Meta:
        verbose_name_plural = 'Reaction categories'

    def __str__(self):
        return f"{self.reaction}: {self.emoji}"

class Reaction(models.Model):
    user      = models.ForeignKey(User,             on_delete=models.CASCADE, related_name='reactions')
    post      = models.ForeignKey(Post,             on_delete=models.CASCADE, related_name='reactions')
    category  = models.ForeignKey(ReactionCategory, on_delete=models.CASCADE, related_name='instances')

    def __str__(self):
        return f"User: {self.user}; Post: {self.post.id}; Reaction category: {self.category}"

    def serialize_short(self):
        return {
            'id'      : self.id,
            'user'    : self.user.id,
            'post'    : self.post.id,
            'category': self.category.reaction
        }