from otree.api import Currency as c, currency_range

from ._builtin import Page, WaitPage
from .models import Constants

class InstructionsPage(Page):
    pass

class Feedback(Page):
    form_model = 'player'
    form_fields = ['longer', 'stop', 'stress', 'anger', 'checkq', 'worries', 'chase', 'greed', 'pray', 'regret']

class GamblingItems(Page):
    form_model = 'player'
    form_fields = ['gi_slot', 'gi_money', 'gi_bet', 'gi_trouble', 'gi_borrow', 'gi_lie', 'gi_fellacy1', 'gi_fellacy2', 'gi_strategy']

class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'nationality', 'religion', 'education', 'profession', 'income']

    def before_next_page(self):
        self.player.set_payoffs()



page_sequence = [InstructionsPage, Feedback, GamblingItems, Demographics]
