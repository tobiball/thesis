import random

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


author = 'Marco'

doc = """
Introduction
"""


class Constants(BaseConstants):
    name_in_url = 'introduction'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            for p in self.get_players():
                p.participant.vars['treatment'] = random.choice(['three', 'three'])


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treatment = models.StringField()
    prolificID = models.StringField(
        label="Please put your Prolific ID here:"
    )


    def set_payoffs(self) -> object:
        self.payoff = 0
        self.treatment = self.participant.vars['treatment']

