from otree.api import *

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'induction_check'
    players_per_group = None
    num_rounds = 1
    induction_images = {'joy': 'sloths_img.png', 'fear': 'wasps_img.png', 'control': 'birds_img.png'}


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    valence = models.IntegerField()
    arousal = models.IntegerField()
    dominance = models.IntegerField()


# PAGES
class Valence(Page):
    form_model = 'player'
    form_fields = ['valence']

    def vars_for_template(player: Player):
        return {
        "video_img": Constants.induction_images[player.participant.treatment],
        }

class Arousal(Page):
    form_model = 'player'
    form_fields = ['arousal']

    def vars_for_template(player: Player):
        return {
        "video_img": Constants.induction_images[player.participant.treatment],
        }

class Dominance(Page):
    form_model = 'player'
    form_fields = ['dominance']

    def vars_for_template(player: Player):
        return {
        "video_img": Constants.induction_images[player.participant.treatment],
        }


page_sequence = [Valence,Arousal,Dominance]
