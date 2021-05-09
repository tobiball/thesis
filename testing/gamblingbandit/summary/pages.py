from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Results(Page):

    def vars_for_template(self):
        risk_payoff = self.participant.vars['scl_payoff']        
        risk_outcome = self.participant.vars['outcome_to_pay']
        survey_payoff = self.participant.vars['survey_payoff']
        survey_mistakes = self.participant.vars['survey_mistakes']
        quiz_payoff = self.participant.vars['quiz_payoff']
        quiz_mistakes = self.participant.vars['quiz_mistakes']
        game_payoff = self.participant.vars['game_payoff']
        total_payoff = 600 + risk_payoff + survey_payoff + game_payoff
        points = round(total_payoff,0)
        euro_payoff = round(float(points/800)+1/8000,2)

        return dict(
            risk_payoff = risk_payoff,
            risk_outcome = risk_outcome,
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
