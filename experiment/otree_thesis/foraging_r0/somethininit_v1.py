from otree import session
from otree.api import *
import random
from random import randrange
import pandas as pd

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'foraging_test'
    players_per_group = None
    num_rounds = 4


#    factor = yay.b


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    foraging_choice = models.BooleanField()
    death = models.BooleanField(default=False, id=111, app_name='foraging_test')
    success = models.BooleanField(default=False, id=111, app_name='foraging_test')
    def trial_outcome(self):
        choose_to_forage = self.foraging_choice
        # self.death = False
        # self.success = False
        print(self.success)
        if choose_to_forage:
            if random.random() < En.probability_threat:
                self.death = True
            else:
                if random.random() < En.probability_gain:
                    self.success = True
                    self.payoff += 1


# SYSTEM
class Engine():
    """
    Creates run details
    """

    def __init__(self):
        self.probability_vector_gain = []
        self.probability_vector_threat = []
        for one in range(4):
            self.probability_vector_gain.append(
                round(randrange(1, 5) * 0.15, 2))  ### integrate images in these two lines
            self.probability_vector_threat.append(round(randrange(1, 5) * 0.1, 1))

    def parameters_run(self, player):
        self.probability_gain = self.probability_vector_gain[(player.round_number - 1)]
        self.probability_threat = self.probability_vector_threat[(player.round_number - 1)]

    # def trial_outcome(self, player):
    #     choose_to_forage = player.foraging_choice
    #     self.death = False
    #     self.success = False
    #     if choose_to_forage:
    #         if random.random() < self.probability_threat:
    #             self.death = True
    #         else:
    #             if random.random() < self.probability_gain:
    #                 self.success = True


En = Engine()  ## where to best initiate? Session?


# PAGES
class Foraging(Page):
    form_model = "player"
    form_fields = ["foraging_choice"]

    def vars_for_template(player: Player):
        En.parameters_run(player)
        gain_percent = int(En.probability_gain * 100)
        threat_percent = int(En.probability_threat * 100)
        return {
            "gain_percent": gain_percent,
            "threat_percent": threat_percent
        }




class Induction(Page):
    pass


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
            return upcoming_apps[0]  # PAGES


page_sequence = [Foraging, Results]
