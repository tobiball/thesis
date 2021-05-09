from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class InstructionsPage(Page):
    pass

class QuizPage(Page):
    form_model = 'player'
    form_fields = ['quiz1', 'quiz2', 'quiz3', 'quiz4']

    def before_next_page(self):
        self.player.count_correct()
        self.player.set_payoffs()

class Results(Page):
    def app_after_this_page(self, upcoming_apps):
        if self.player.mistakes == 0 and self.participant.vars['treatment'] == 'four':
            return "game_trial_t3"

page_sequence = [InstructionsPage, QuizPage, Results]
