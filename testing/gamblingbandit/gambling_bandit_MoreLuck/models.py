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
    name_in_url = 'game_t1'
    players_per_group = None
    num_rounds = 50
    starting_endowment = 600
    starting_factor = 27
    maximum_bet = 30

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
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

    def shuffle_urls(self):
        urls = ["https://i.imgur.com/MpANPXG.png", "https://i.imgur.com/J6J8Dgj.png", "https://i.imgur.com/7dg9B3M.png", "https://i.imgur.com/bANsdm9.png", "https://i.imgur.com/OBDCNsY.png", "https://i.imgur.com/hUTNX3m.png"]
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

    def check_outcome_update_balance(self):
        p1 = self.get_player_by_id(1)
        if p1.page_refreshed > 1:
            self.result_output = "reloaded the game page. Therefore, the game counts as a loss"
            self.round_won = 0
            p1.balance = p1.balance - p1.bet
        else:
            if p1.last_picture_viewed == self.correct_pos and p1.last_picture_viewed2 == self.correct_pos2:
                self.round_won = 1
                p1.balance = round(p1.balance + (p1.factor-1)*p1.bet,1)
                p1.rounds_won = p1.rounds_won + 1
                self.result_output = "won the game"
            else:
                self.round_won = 0
                p1.balance = p1.balance - p1.bet
                self.result_output = "lost the game"
        p1.factor = round(p1.factor - 0.6, 1)

    def set_balance(self):
        p1 = self.get_player_by_id(1)
        if self.round_number == 1:
            p1.balance = Constants.starting_endowment
            p1.factor = Constants.starting_factor
        else:
            p1.balance = p1.in_round(self.round_number - 1).balance
            p1.factor = p1.in_round(self.round_number - 1).factor

    def set_payoff(self):
        p1 = self.get_player_by_id(1)
        p1.set_payoffs()



class Player(BasePlayer):
    page_refreshed = models.IntegerField(initial=0)
    time_clicked = models.IntegerField()
    last_picture_viewed = models.IntegerField()
    last_picture_viewed2 = models.IntegerField()
    advance = models.IntegerField(
        choices=[[0, 'Yes'], [1, 'No']],
        label='Do you want to play another round?',
        widget=widgets.RadioSelect,

    )
    rounds_won = models.IntegerField(initial=0)
    balance = models.FloatField()
    bet = models.IntegerField(widget=widgets.Slider, min=0, initial=0)

    def bet_max(self):
        return min(self.balance, Constants.maximum_bet)

    factor = models.FloatField()

    def set_payoffs(self) -> object:
        self.payoff = round(self.balance,2)
        self.participant.vars['game_payoff'] = self.payoff
        self.participant.vars['game_won'] = self.rounds_won