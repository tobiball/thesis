from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
from random import shuffle

author = 'Marco Lambrecht'

doc = """
gambling app (one armed bandit)
"""


class Constants(BaseConstants):
    name_in_url = 'game_trial_t3'
    players_per_group = None
    num_rounds = 1
    starting_endowment = 0
    starting_factor = 27.0
    maximum_bet = 30

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    round_won = models.IntegerField()
    result_output = models.StringField()
    correct_pos = models.IntegerField()
    correct_pos2 = models.IntegerField()
    url1_1 = models.StringField()
    url1_2 = models.StringField()
    url1_3 = models.StringField()
    url1_4 = models.StringField()
    url1_5 = models.StringField()
    url1_6 = models.StringField()
    url2_1 = models.StringField()
    url2_2 = models.StringField()
    url2_3 = models.StringField()
    url2_4 = models.StringField()
    url2_5 = models.StringField()
    url2_6 = models.StringField()
    page_refreshed = models.IntegerField(initial=0)
    time_clicked = models.IntegerField()
    last_picture_viewed = models.IntegerField()
    last_picture_viewed2 = models.IntegerField()

    rounds_won = models.IntegerField(initial=0)
    balance = models.IntegerField()
    old_balance = models.IntegerField()
    bet = models.IntegerField(widget=widgets.RadioSelect, min=1, initial=0)

    def bet_max(self):
        return 51-self.round_number

    factor = models.FloatField()

    def set_payoffs(self) -> object:
        self.payoff = 0
        self.participant.vars['game_trial_payoff'] = round(self.balance,2)
        self.participant.vars['game_trial_won'] = self.rounds_won

    def set_balance(self):
        if self.round_number == 1:
            self.balance = Constants.starting_endowment
            self.factor = Constants.starting_factor
        else:
            self.balance = self.in_round(self.round_number - 1).balance
            self.factor = self.in_round(self.round_number - 1).factor
        self.old_balance = self.balance
        self.round_won = 0
        self.balance = self.balance + 51 - self.round_number - self.bet
        self.result_output = "lost the game"

    def check_outcome_update_balance(self):
        if self.last_picture_viewed == self.correct_pos and self.last_picture_viewed2 == self.correct_pos2:
            self.round_won = 1
            self.balance = round(self.balance + 72 * self.bet, 1)
            self.result_output = "won the game"

    def shuffle_urls(self):
        urls = ["https://i.imgur.com/MpANPXG.png", "https://i.imgur.com/J6J8Dgj.png", "https://i.imgur.com/7dg9B3M.png",
                "https://i.imgur.com/bANsdm9.png", "https://i.imgur.com/OBDCNsY.png", "https://i.imgur.com/hUTNX3m.png"]
        shuffle(urls)
        self.correct_pos = urls.index("https://i.imgur.com/J6J8Dgj.png")
        self.url1_1 = urls[0]
        self.url1_2 = urls[1]
        self.url1_3 = urls[2]
        self.url1_4 = urls[3]
        self.url1_5 = urls[4]
        self.url1_6 = urls[5]
        shuffle(urls)
        self.correct_pos2 = urls.index("https://i.imgur.com/J6J8Dgj.png")
        self.url2_1 = urls[0]
        self.url2_2 = urls[1]
        self.url2_3 = urls[2]
        self.url2_4 = urls[3]
        self.url2_5 = urls[4]
        self.url2_6 = urls[5]
