from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class InstructionsPage(Page):
    pass

class QuizPage(Page):
    form_model = 'player'
    form_fields = ['quiz1', 'quiz2', 'quiz3', 'quiz4']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'count_correct'

class ResultsWaitPage2(WaitPage):
    after_all_players_arrive = 'set_payoff'

class Results(Page):
    pass


page_sequence = [InstructionsPage, QuizPage, ResultsWaitPage, ResultsWaitPage2, Results]
