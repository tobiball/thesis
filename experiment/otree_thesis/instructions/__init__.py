from otree.api import *

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'instructions'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    gender = models.StringField(
        label="Please select your gender",
        choices=["female","male","other"],
        widget=widgets.RadioSelect)
    age = models.StringField(
        label="Please select your age",
        choices=["0 - 30","31 - 60","61 -"],
        widget=widgets.RadioSelect)



class Demographics(Page):
    form_model = 'player'
    form_fields = ['gender','age']  # this means player.name, player.age


# PAGES
class Instructions(Page):
    def vars_for_template(self):
        return {
            "m1":"shroom_015.png",
            "m2":"shroom_03.png",
            "m3":"shroom_045.png",
            "m4":"shroom_06.png",
            "w1":"wolf_01.png",
            "w2":"wolf_02.png",
            "w3":"wolf_03.png",
            "w4":"wolf_04.png",
            "one": "one.png",
            "null": "null.png",
            "minus": "minus.png",
            "example_clearing":"example_clearing.png"
            }


class Comprehension(Page):
    form_model = 'player'
    form_fields = ['name', 'age'] # this means player.name, player.age


page_sequence = [Demographics,Instructions, Comprehension]
