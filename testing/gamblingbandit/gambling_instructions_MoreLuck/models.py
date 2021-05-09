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
    name_in_url = 'game_instructions_t1'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    def count_correct(self):
        p1 = self.get_player_by_id(1)
        p1.mistakes = 0
        if p1.quiz1 != 2:
            p1.mistakes = p1.mistakes + 1;
        if p1.quiz2 != 1:
            p1.mistakes = p1.mistakes + 1;
        if p1.quiz3 != 2:
            p1.mistakes = p1.mistakes + 1;
        if p1.quiz4 != 1:
            p1.mistakes = p1.mistakes + 1;

    def set_payoff(self):
        p1 = self.get_player_by_id(1)
        p1.set_payoffs()

class Player(BasePlayer):
    mistakes = models.IntegerField()
    quiz1 = models.IntegerField(
        choices=[[1, 500], [2, 600], [3, 800]],
        label='How many points will you be endowed with?',
        widget=widgets.RadioSelect,
    )
    quiz2 = models.IntegerField(
        choices=[[1, "Shamrock at both"], [2, "Coin at the right"], [3, "Lemon at the left"]],
        label='What is your win condition?',
        widget=widgets.RadioSelect,
    )
    quiz3 = models.IntegerField(
        choices=[[1, 40], [2, 60], [3, 80]],
        label='Assume your multiplicator is 1.5 and you win the game after betting 40. How much will be your reward?',
        widget=widgets.RadioSelect,
    )
    quiz4 = models.IntegerField(
        choices=[[1, 30], [2, 50], [3, 80]],
        label='What is the maximum bet that you can place (given that your balance is sufficient)?',
        widget=widgets.RadioSelect,
    )

    def set_payoffs(self) -> object:
        self.payoff = (1 - self.mistakes*0.2)*500
        self.participant.vars['quiz_payoff'] = self.payoff
        self.participant.vars['quiz_mistakes'] = self.mistakes
