from otree.api import *

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'induction_positive_test'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class Induction(Page):
    def vars_for_template(player: Player):
        return {
            "video": "sloths_1.mp4"
        }

    timeout_seconds = 10
    timer_text = ''


page_sequence = [Induction]