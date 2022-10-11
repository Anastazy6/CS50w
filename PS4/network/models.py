from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import CharField


class User(AbstractUser):
    # TODO:
    #   Strona profilowa
    #   Followerzy

    pass

class Post(models.Model):
    author    = models.ForeignKey     (User, on_delete=models.CASCADE, related_name='posts')
    body      = models.CharField      (max_length=4096)
    timestamp = models.DateTimeField  (auto_add_now=True)
    likes     = models.ManyToManyField(User, on_delete=models.CASCADE, related_name='likes')
    # TODO:
    #   Twórca
    #   Treść
    #   Czas stworzenia posta
    #   Liczba polubień (raczej nie ma sensu robić tego w modelu, tylko za pomocą funkcji mielącej bazę danych, ale można wypróbować też M2M)
    #   Opcjonalnie: tytuł posta
    #   Wyświetlanie: 10 na stronę
    #   Edycja posta: prawdopodobnie trzeba będzie użyć fetch(...{method: 'PUT'})
    #     Za pomocą JavaScriptu ma się to odbywać BEZ przeładowywania strony
    #     Zabezpieczyć przed edycją cudzego posta (dane identyfikacyjne posta nie powinny być dostępne w linku, ani w innych wrażliwych miejscach)
    pass

class Follower(models.Model):
    following = models.ForeignKey     (User, on_delete=models.CASCADE, related_name='followers') # obserwujący
    followed  = models.ForeignKey     (User, on_delete=models.CASCADE, related_name='followed')  # obserwowany
    # TODO:
    #   wymyślić koncepcję followera
    #     a) tabela relacji w bazie danych (id relacji, id obserwowanego, id obserwującego)
    #     b) many to many w parametrach klasy User
    #   strona z obserwowanymi użytkownikami: 
    #     coś jak zwykła strona z postami, ale wyświetlająca tylko posty obserwowanych użytkowników
    #     widoczna tylko dla zalogowamych (nie powinna się wyświetlać w pasku nawigacyjnym, jeśli ktoś się nie zalogował)
    #   zabezpieczyć przed obserwowaniem samego siebie
    pass

# class Like(models.Model):
    # TODO:
    #   wymyślić koncepcję lajka
    #     a) tabela relacji w bazie danych (id relacji, id lajkowanego, id lajkującego)
    #     b) many to many w parametrach klasy Post
    #   Polubienie posta ma nie tylko zaktualizować bazę danych, ale i licznik polubień na stronie danego posta.