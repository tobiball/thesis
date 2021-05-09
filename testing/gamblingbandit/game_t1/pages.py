from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class StartWaitPage(Page):
    timeout_seconds = 1

    def before_next_page(self):
        self.player.set_balance()


class BetPage(Page):
    form_model = 'player'
    form_fields = ['bet']

    def vars_for_template(self):
        max_bet = 51 - self.player.round_number
        if self.player.round_number == 1:
            balance = 0
        else:
            balance = self.player.in_round(self.player.round_number - 1).balance
        return dict(
            max_bet=max_bet,
            balance=balance,
        )

    def before_next_page(self):
        self.player.shuffle_urls()
        self.player.set_balance()


class GamblePage(Page):
    form_model = 'player'
    form_fields = ['time_clicked', 'last_picture_viewed', 'last_picture_viewed2']

    def is_displayed(self):
        return self.player.page_refreshed == 0

    def vars_for_template(self):
        self.player.page_refreshed = self.player.page_refreshed + 1
        random_pos = self.player.random_pos
        random_pos2 = self.player.random_pos2
        bet = self.player.bet
        url1 = self.player.url1_1
        url2 = self.player.url1_2
        url3 = self.player.url1_3
        url4 = self.player.url1_4
        url5 = self.player.url1_5
        url6 = self.player.url1_6
        url7 = self.player.url2_1
        url8 = self.player.url2_2
        url9 = self.player.url2_3
        url10 = self.player.url2_4
        url11 = self.player.url2_5
        url12 = self.player.url2_6

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
            random_pos=random_pos,
            random_pos2=random_pos2,
        )
    def before_next_page(self):
        self.player.check_outcome_update_balance()

class StartWaitPage2(Page):
    timeout_seconds = 1

    def before_next_page(self):
        self.player.check_outcome_update_balance()
        self.player.set_payoffs()

class Results(Page):
    form_model = 'player'

    def get_form_fields(self):
        if self.player.round_number < 50:
            return ['advance']
        else:
            return ['advance2']

    def vars_for_template(self):
        new_endowment = 50 - self.player.round_number
        unspent = new_endowment + 1 - self.player.bet
        potential_win = self.player.bet * 12

        return dict(
            new_endowment=new_endowment,
            unspent=unspent,
            potential_win=potential_win,
        )

    def before_next_page(self):
        self.player.set_payoffs()


class Summary(Page):
    def is_displayed(self):
        return self.player.advance == 1 or self.player.round_number == 50

    def vars_for_template(self):
        import time
        time_played = time.time() - self.player.start_time
        seconds_played = int(time_played%60)
        minutes_played = int((time_played-time_played%60)/60)
        return dict(
            seconds_played = seconds_played,
            minutes_played = minutes_played,
        )

    def app_after_this_page(self, upcoming_apps):
        if self.player.advance == 1 or self.player.round_number == 50:
            return "survey"

page_sequence = [BetPage, GamblePage, Results, Summary]
