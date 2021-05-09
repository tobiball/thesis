from otree import session
from otree.api import *
import random
from random import randrange
import pandas as pd

c = Currency

doc = """
Displays one run of experimental task and ends after four rounds or predation
"""


# Models
class Constants(BaseConstants):
    name_in_url = 'foraging_r0'
    players_per_group = None
    num_rounds = 4
    probability_vector_gain = []
    probability_vector_threat = []
    probability_graphics_gain = {0.15:"shroom_015.png", 0.3:"shroom_03.png", 0.45:"shroom_045.png", 0.6:"shroom_06.png"}
    probability_graphics_threat = {0.1:"wolf_01.png", 0.2:"wolf_02.png", 0.3:"wolf_03.png", 0.4:"wolf_04.png"}

    for one in range(4):
        probability_vector_gain.append(round(randrange(1, 5) * 0.15, 2))  ### integrate images in these two lines
        probability_vector_threat.append(round(randrange(1, 5) * 0.1, 1))


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    death = models.BooleanField(default=False)
    success = models.BooleanField(default=False)
    foraging_choice = models.BooleanField()
    probability_threat = models.FloatField()
    probability_gain = models.FloatField()

    def trial_parameters(self):
        """
        Sets gain and threat probabilities as attributes from probability vector based on round
        """
        self.probability_threat = Constants.probability_vector_threat[(self.round_number - 1)]  # Move to player?
        self.probability_gain = Constants.probability_vector_gain[(self.round_number - 1)]

    def trial_outcome(self):
        """
        Picks up user input from Foraging Page and randomly draws success, death or none
        """
        choose_to_forage = self.foraging_choice
        if choose_to_forage:
            draw = random.random()
            if draw < self.probability_threat:
                self.death = True
            else:
                if draw < self.probability_threat + self.probability_gain:
                    self.success = True
                    self.payoff += 1


# PAGES
class Foraging(Page):
    form_model = "player"
    form_fields = ["foraging_choice"]

    def vars_for_template(player: Player):
        player.trial_parameters()
        gain_percent = int(player.probability_gain * 100)
        threat_percent = int(player.probability_threat * 100)
        return {
           # 'Image'    :  "".join(['', str(player.iImg) , '.jpg']) ,
            "gain_image": Constants.probability_graphics_gain[player.probability_gain],
            "threat_image": Constants.probability_graphics_threat[player.probability_threat],
        }


class Results(Page):
    timeout_seconds = 5

    @staticmethod
    def vars_for_template(player: Player):
        player.trial_outcome()
        success = player.success
        death = player.death
        return {
            "death": death,
            "success": success
        }

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.death:
            return upcoming_apps[0]


page_sequence = [Foraging, Results]
