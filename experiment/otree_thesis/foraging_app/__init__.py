from otree import session
from otree.api import *
import random
from random import randrange
import itertools

c = Currency

doc = """

"""


# Models
class Constants(BaseConstants):
    name_in_url = 'foraging_app'
    players_per_group = None
    num_rounds = 16
    induction_videos = {'joy': 'sloths_', 'fear': 'wasps_', 'control': 'birds_'}
    probability_graphics_gain = {
        0.15: "shroom_015.png",
        0.3: "shroom_03.png",
        0.45: "shroom_045.png",
        0.6: "shroom_06.png"
    }
    probability_graphics_threat = {
        0.1: "wolf_01.png",
        0.2: "wolf_02.png",
        0.3: "wolf_03.png",
        0.4: "wolf_04.png"
    }


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treatment = models.StringField()
    death = models.BooleanField(default=False)
    success = models.BooleanField(default=False)
    foraging_choice = models.BooleanField()
    probability_threat = models.FloatField()
    probability_gain = models.FloatField()
    trial_in_game = models.IntegerField()
    clearing_number = models.IntegerField()
    dRT = models.FloatField(blank=True)
    timeout = models.BooleanField(default=False)

    def trial_parameters(self):
        """
        Sets gain and threat probabilities as attributes from probability vector based on round
        """
        self.probability_threat = self.participant.probability_vector_threat[(self.round_number - 1)]  # Move to player?
        self.probability_gain = self.participant.probability_vector_gain[(self.round_number - 1)]

    def trial_position(self):
        """
        Tracks the position the subjects are in, in the experiment
        (1) self.participant.trial_in_game shows position in experiment (1-16)
            this can differ from round number because trials can be skipped in case of death
        (2) self.clearing_number tracks position in forest
        (3) Initiates self.participant.forest_payoff variable
        """
        # (1,3)
        if self.round_number == 1:
            self.participant.trial_in_game = 1
            self.participant.forest_payoff = 0
        else:
            previous_player = self.in_round(self.round_number - 1)
            trial_in_game_mod = self.participant.trial_in_game % 4
            if previous_player.death and trial_in_game_mod != 0:
                self.participant.trial_in_game += 5 - trial_in_game_mod
            else:
                self.participant.trial_in_game += 1
        self.trial_in_game = self.participant.trial_in_game
        # (2)
        self.clearing_number = self.participant.trial_in_game % 4  # clearing number is always between 1 and 4
        if self.clearing_number == 0:
            self.clearing_number = 4

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

    def induction_flag(self):
        self.participant.induction_flag = False
        if self.clearing_number == 4 or self.death:
            self.participant.induction_flag = True

    def participant_payoff(self):
        """
        Adds forest payoff to total payoff
        """
        if self.death:
            self.participant.forest_payoff = 0
        elif self.clearing_number == 4:
            self.participant.payoff += self.participant.forest_payoff
            self.participant.forest_payoff = 0


def creating_session(subsession):
    emotions = itertools.cycle(['joy', 'fear', 'control'])
    for player in subsession.get_players():
        player.participant.treatment = next(emotions)
        player.participant.probability_vector_gain = []
        player.participant.probability_vector_threat = []
        for one in range(16):
            player.participant.probability_vector_gain.append(round(randrange(1, 5) * 0.15, 2))
            player.participant.probability_vector_threat.append(round(randrange(1, 5) * 0.1, 1))


# Pages
class Induction(Page):
    timeout_seconds = 10
    timer_text = ''

    def is_displayed(self):
        if self.round_number == 1:
            return True
        else:
            return self.participant.induction_flag

    def vars_for_template(self):
        if self.round_number == 1:
            self.participant.video_nr = 0
        self.participant.video_nr += 1
        return {"video": "{}{}.mp4".format(Constants.induction_videos[self.participant.treatment],
                                           self.participant.video_nr)}


class Foraging(Page):
    timeout_seconds = 5
    timer_text = 'Time Remaining:'
    form_model = "player"
    form_fields = ["foraging_choice", "dRT"]

    def vars_for_template(self):
        self.trial_parameters()
        self.trial_position()
        return {
            "clearing_number": self.clearing_number,
            "gain_image": Constants.probability_graphics_gain[self.probability_gain],
            "threat_image": Constants.probability_graphics_threat[self.probability_threat],
        }

    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.timeout = True


class Results(Page):
    timeout_seconds = 1
    timer_text = ''

    def vars_for_template(player: Player):
        player.trial_outcome()
        if player.death:
            message = "-"
        elif player.success:
            message = "1"
            player.participant.forest_payoff += 1  # track payoff for forest
        else:
            message = "0"
        return {"message": message, }

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        player.participant_payoff()
        player.induction_flag()
        if player.participant.trial_in_game >= 16 or player.participant.trial_in_game > 12 and player.death:
            return upcoming_apps[0]


page_sequence = [Induction, Foraging, Results]
