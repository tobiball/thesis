from otree.api import *

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'instructions'
    players_per_group = None
    num_rounds = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    comprehension_1 = models.StringField(
        label="Q1: Pick the correct statement",
        choices=[" '0' means animal attack",
                 " '1' means no foraging success",
                 " '1' means foraging success",
                 " '-' means no foraging success",
                 " '0' means foraging success",
                 ],
        widget=widgets.RadioSelect)
    comprehension_2 = models.StringField(
        label="Q2: Pick the most favourable chances",
        choices=[" success probability: 15% , attack probability: 40%",
                 " success probability: 30% , attack probability: 30%",
                 " success probability: 45% , attack probability: 10%",
                 " success probability: 45% , attack probability: 40%",
                 " success probability: 30% , attack probability: 40%",
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
    q1 = models.BooleanField(default=False)
    q2 = models.BooleanField(default=False)
    q3 = models.BooleanField(default=False)

class Instructions(Page):
    def vars_for_template(self):
        return {
            "m1": "shroom_015.png",
            "m2": "shroom_03.png",
            "m3": "shroom_045.png",
            "m4": "shroom_06.png",
            "w1": "wolf_01.png",
            "w2": "wolf_02.png",
            "w3": "wolf_03.png",
            "w4": "wolf_04.png",
            "one": "one.png",
            "null": "null.png",
            "minus": "minus.png",
            "example_clearing": "example_clearing.png"
        }

class Comprehension(Page):
    form_model = 'player'
    form_fields = ['comprehension_1','comprehension_2','comprehension_3'] # this means player.name, player.age

    def app_after_this_page(player, upcoming_apps):
        if player.comprehension_1 == " '1' means foraging success":
            player.q1 = True
        if player.comprehension_2 == " success probability: 45% , attack probability: 10%":
            player.q2 = True
        if player.comprehension_3 == " Being attacked leads to losing the food points from the current forest.":
            player.q3 = True
        if all([player.q1,player.q2,player.q3]):
            return upcoming_apps[0]
        elif int(player.round_number) == 2:
            return upcoming_apps[3]

class Error(Page):
    def vars_for_template(player):
        de_dictionary = {'q1':'Correct','q2':'Correct','q3':'Correct'}
        ic = ' is incorrect'
        if player.q1 == False:
            de_dictionary['q1'] = ("<b> {} </b>--> {}").format(player.comprehension_1, ic)
        if player.q2 == False:
            de_dictionary['q2'] = ("<b> {} </b>--> {}").format(player.comprehension_2, ic)
        if player.q3 == False:
            de_dictionary['q3'] = ("<b> {} </b>--> {}").format(player.comprehension_3, ic)

        return de_dictionary



page_sequence = [Instructions,Comprehension,Error]

