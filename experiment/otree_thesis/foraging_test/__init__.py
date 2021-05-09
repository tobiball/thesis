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
    name_in_url = 'foraging_test'
    players_per_group = None
    num_rounds = 16
    probability_vector_gain = []
    probability_vector_threat = []
    probability_graphics_gain = {0.15: "shroom_015.png", 0.3: "shroom_03.png", 0.45: "shroom_045.png",
                                 0.6: "shroom_06.png"}
    probability_graphics_threat = {0.1: "wolf_01.png", 0.2: "wolf_02.png", 0.3: "wolf_03.png", 0.4: "wolf_04.png"}

    for one in range(16):
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
    trial_in_game = models.IntegerField()
    clearing_number = models.IntegerField()


    def trial_parameters(self):
        """
        Sets gain and threat probabilities as attributes from probability vector based on round
        """
        self.probability_threat = Constants.probability_vector_threat[(self.round_number - 1)]  # Move to player?
        self.probability_gain = Constants.probability_vector_gain[(self.round_number - 1)]

    def trial_position_counter(self):  ### Think of Positions where to define clearing
        if self.round_number == 1:
            self.participant.trial_in_game = 1
            self.clearing_number = 1
        else:
            prev_player = self.in_round(self.round_number - 1)
            if prev_player.death:
                self.participant.trial_in_game += 5 - self.participant.trial_in_game % 4
            else:
                self.participant.trial_in_game += 1
        self.clearing_number = self.participant.trial_in_game % 4  # clearing number is always between 1 and 4
        if self.clearing_number == 0:
            self.clearing_number = 4
        self.trial_in_game = self.participant.trial_in_game

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
class Induction(Page):
    timeout_seconds = 10
    timer_text = ''

    def is_displayed(self):
        if self.round_number == 1:
            return True
        else:
            return self.participant.trial_in_game in [4, 8, 12] #There is a problematic edge case here because this is the previous number round but death takes it to the actualm round and hence skips the induction

    def vars_for_template(self):
        if self.round_number == 1:
            video_nr = 1
        else:
            video_nr = int(self.participant.trial_in_game / 4 + 1)
        return {
            "video": "sloths_{}.mp4".format(video_nr)  ####????
        }



class Foraging(Page):
    form_model = "player"
    form_fields = ["foraging_choice"]

    def vars_for_template(self):
        self.trial_parameters()
        self.trial_position_counter()
        return {
            "clearing_number": self.clearing_number,
            "gain_image": Constants.probability_graphics_gain[self.probability_gain],
            "threat_image": Constants.probability_graphics_threat[self.probability_threat],
        }


class Results(Page):
    timeout_seconds = 0.5
    timer_text = ''

    @staticmethod
    def vars_for_template(player: Player):
        player.trial_outcome()
        success = player.success
        death = player.death
        if death:
            message = "-"
        elif success:
            message = "1"
        else:
            message = "0"
        return {
            "message": message,
        }

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.participant.trial_in_game >= 16 or player.participant.trial_in_game > 13 and player.death:
            return upcoming_apps[0]


page_sequence = [Induction, Foraging, Results]
