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


author = 'Marco Lambrecht'

doc = """
gambling instructions
"""


class Constants(BaseConstants):
    name_in_url = 'game_instructions_t2'
    players_per_group = None
    num_rounds = 20


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    quiz_output = models.StringField()
    mistakes = models.IntegerField()
    quiz1 = models.IntegerField(
        choices=[[1, 40], [2, 50], [3, 60]],
        label='How many points will you receive in your first round?',
        widget=widgets.RadioSelect,
    )
    quiz2 = models.IntegerField(
        choices=[[1, "Lemon at the left"], [2, "Coin at the right"], [3, "Shamrock at both"]],
        label='What is your win condition?',
        widget=widgets.RadioSelect,
    )
    quiz3 = models.IntegerField(
        choices=[[1, "The second wheel stops randomly"], [2, "The STOP-button influences the second wheel"], [3, "The picture of the first wheel influences the second wheel"]],
        label='What determines the picture of the second wheel?',
        widget=widgets.RadioSelect,
    )
    quiz4 = models.IntegerField(
        choices=[[1, 0], [2, 1], [3, 10]],
        label='What is the minimum bet that you can place?',
        widget=widgets.RadioSelect,
    )

    def count_correct(self) -> object:
        self.mistakes = 0
        if self.quiz1 != 2:
            self.mistakes = self.mistakes + 1
        if self.quiz2 != 3:
            self.mistakes = self.mistakes + 1
        if self.quiz3 != 1:
            self.mistakes = self.mistakes + 1
        if self.quiz4 != 2:
            self.mistakes = self.mistakes + 1
        if self.mistakes == 0:
            self.quiz_output = "You answered all questions correctly. You can proceed to play the trial round."
        else:
            self.quiz_output = "Unfortunately, there were some mistakes in your answers. Please take another look at the instructions."

    def set_payoffs(self) -> object:
        self.payoff = 0
        self.participant.vars['quiz_payoff'] = self.payoff
        self.participant.vars['quiz_mistakes'] = self.mistakes
