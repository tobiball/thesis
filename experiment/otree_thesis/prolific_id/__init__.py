from otree.api import *

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'prolific_id'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    prolific_id = models.StringField()


# PAGES
class Prolific_Id(Page):
    form_model = 'player'
    form_fields = ['prolific_id']

class Results(Page):
    pass


page_sequence = [Prolific_Id]
