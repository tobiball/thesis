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

    comprehension_1 = models.StringField(
        label="Q1: Pick the correct statement",
        choices=[" 0 means animal attack",
                 " 1 means no foraging success",
                 " 1 means foraging success",
                 " - means no foraging success",
                 " 0 means foraging success",
                 ],
        widget=widgets.RadioSelect)
    comprehension_2 = models.StringField(
        label="Q2: Pick the most favourable chances",
        choices=[" success probability: 15% attack probability 40%",
                 " success probability: 30% attack probability 30%",
                 " success probability: 45% attack probability 10%",
                 " success probability: 45% attack probability 40%",
                 " success probability: 30% attack probability 40%",
                 ],
        widget=widgets.RadioSelect)
    comprehension_3 = models.StringField(
        label="Q3: Pick the correct sentence",
        choices=[" Being attacked leads to losing the food points from all forests.",
                 " The less food points you collect the better.",
                 " A large dangerous animal symbol is good.",
                 " Being attacked leads to losing the food points from the current forest.",
                 " A small mushroom symbol is good.",
                 ],
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
    form_fields = ['comprehension_1','comprehension_2','comprehension_3'] # this means player.name, player.age

    def vars_for_template(player: Player):
        print(player.comprehension_1)
        print(player.comprehension_2)
        print(player.comprehension_3)


page_sequence = [Demographics,Instructions]
