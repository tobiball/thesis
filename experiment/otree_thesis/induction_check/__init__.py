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
    valence = models.StringField(
        label="Please rate how the animal videos made you feel. 5 means very positive, 1 means very negative.",
        choices=[5, 4, 3, 2, 1],
        widget=widgets.RadioSelect)
    panas = models.StringField(
        label="Please pick the word that best descries how the videos made you feel.",
        choices=['Neutral', 'Attentive', 'Hostile', 'Active', 'Irritable', 'Alert', 'Ashamed', 'Excited', 'Guilty',
                 'Enthusiastic', 'Distressed', 'Determined', 'Upset', 'Inspired', 'Scared', 'Proud', 'Afraid',
                 'Interested', 'Jittery', 'Strong', 'Nervous'],
        widget=widgets.RadioSelect)


# PAGES
class Induction_Check(Page):
    form_model = 'player'
    form_fields = ['valence', 'panas']

    def vars_for_template(player: Player):
        return {
        "video_img": Constants.induction_images[player.participant.treatment],
        }



page_sequence = [Induction_Check]
