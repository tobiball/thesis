from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class StartWaitPage(WaitPage):
    after_all_players_arrive = 'set_balance'

class BetPage(Page):
    form_model = 'player'
    form_fields = ['bet']

    def vars_for_template(self):
        max_bet = min(self.player.balance, Constants.maximum_bet)
        factor = self.player.factor

        return dict(
            max_bet=max_bet,
            factor=factor,
        )

class ShuffleWaitPage(WaitPage):
    after_all_players_arrive = 'shuffle_urls'

class GamblePage(Page):
    form_model = 'player'
    form_fields = ['time_clicked', 'last_picture_viewed', 'last_picture_viewed2']

    def vars_for_template(self):
        self.player.page_refreshed = self.player.page_refreshed + 1
        bet = self.player.bet
        url1 = self.group.url1_1
        url2 = self.group.url1_2
        url3 = self.group.url1_3
        url4 = self.group.url1_4
        url5 = self.group.url1_5
        url6 = self.group.url1_6
        url7 = self.group.url2_1
        url8 = self.group.url2_2
        url9 = self.group.url2_3
        url10 = self.group.url2_4
        url11 = self.group.url2_5
        url12 = self.group.url2_6

        return dict(
            url1=url1,
            url2=url2,
            url3=url3,
            url4=url4,
            url5=url5,
            url6=url6,
            url7=url7,
            url8=url8,
            url9=url9,
            url10=url10,
            url11=url11,
            url12=url12,
            bet=bet,
        )

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'check_outcome_update_balance'

class ResultsWaitPage2(WaitPage):
    after_all_players_arrive = 'set_payoff'

class Results(Page):
    form_model = 'player'
    form_fields = ['advance']
    def app_after_this_page(self, upcoming_apps):
        if self.player.advance == 1:
            return "survey"

page_sequence = [StartWaitPage, BetPage, ShuffleWaitPage, GamblePage, ResultsWaitPage, ResultsWaitPage2, Results]
