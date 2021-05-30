from otree.api import *

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'fin_prolific'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treatment = models.StringField()
    gender = models.StringField(
        label="Please select your gender",
        choices=["female", "male", "other"],
        widget=widgets.RadioSelect)
    age = models.StringField(
        label="Please select your age",
        choices=["18 - 30", "31 - 65", "65 + "],
        widget=widgets.RadioSelect)
    education = models.StringField(
        label="Highest level of education obtained",
        choices=[[1, 'Primary education'],[2, 'High school or equivalent'],[3, 'Higher education'],[4, 'Bachelors degree'],[5, 'Masters degree'],[6, 'Doctorate'],[7, 'Other'], ],
        widget = widgets.RadioSelect)

# PAGES

class Demographics(Page):
    form_model = 'player'
    form_fields = ['gender', 'age','education']  # this means player.name, player.age


class Fin(Page):
    pass

    def vars_for_template(player: Player):
        player.treatment = player.participant.treatment
        return {"food_points": player.participant.payoff,
                "cash":cu(player.participant.payoff).to_real_world_currency(player.session)
                }


page_sequence = [Demographics, Fin]
