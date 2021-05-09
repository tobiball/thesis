from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Results(Page):

    def vars_for_template(self):
        survey_payoff = self.participant.vars['survey_payoff']
        survey_mistakes = self.participant.vars['survey_mistakes']
        quiz_payoff = self.participant.vars['quiz_payoff']
        quiz_mistakes = self.participant.vars['quiz_mistakes']
        game_payoff = self.participant.vars['game_payoff']
        total_payoff = survey_payoff + quiz_payoff + game_payoff
        points = round(total_payoff,0)
        euro_payoff = round(points/500,2)

        return dict(
            survey_payoff = survey_payoff,
            survey_mistakes = survey_mistakes,
            quiz_payoff = quiz_payoff,
            quiz_mistakes = quiz_mistakes,
            game_payoff = game_payoff,
            total_payoff = total_payoff,
            euro_payoff = euro_payoff,
            points = points,
        )


page_sequence = [Results]
