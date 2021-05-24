from otree.api import *

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'fin'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    gender = models.StringField(
        label="Please select your gender",
        choices=["female", "male", "other"],
        widget=widgets.RadioSelect)
    age = models.StringField(
        label="Please select your age",
        choices=["18 - 30", "31 - 65", "65 - "],
        widget=widgets.RadioSelect)

# PAGES

class Demographics(Page):
    form_model = 'player'
    form_fields = ['gender', 'age']  # this means player.name, player.age


class Fin(Page):
    pass


page_sequence = [Demographics, Fin]
