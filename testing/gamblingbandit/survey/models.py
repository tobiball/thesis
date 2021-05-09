from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)


class Constants(BaseConstants):
    name_in_url = 'survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass



class Player(BasePlayer):
    risk_payoff = models.CurrencyField()
    survey_payoff = models.CurrencyField()
    quiz_payoff = models.CurrencyField()
    game_payoff = models.CurrencyField()
    total_payoff = models.CurrencyField()
    euro_payoff = models.FloatField()

    longer = models.IntegerField(
        choices=[[1, 'Strongly Agree'], [2, 'Agree'], [3, 'Disagree'], [4, 'Strongly Disagree']],
        label="I played the game longer than I wanted to."
    )
    stop = models.IntegerField(
        choices=[[1, 'Strongly Agree'], [2, 'Agree'], [3, 'Disagree'], [4, 'Strongly Disagree']],
        label="Sometimes I felt like stopping the game, but yet I played another round."
    )
    stress = models.IntegerField(
        choices=[[1, 'Strongly Agree'], [2, 'Agree'], [3, 'Disagree'], [4, 'Strongly Disagree']],
        label="It was stressful to play the game."
    )
    anger = models.IntegerField(
        choices=[[1, 'Strongly Agree'], [2, 'Agree'], [3, 'Disagree'], [4, 'Strongly Disagree']],
        label="At times, I got angry during the game."
    )
    checkq = models.IntegerField(
        choices=[[1, 'Strongly Agree'], [2, 'Agree'], [3, 'Disagree'], [4, 'Strongly Disagree']],
        label="In case you want extra points, choose to strongly agree here."
    )
    worries = models.IntegerField(
        choices=[[1, 'Strongly Agree'], [2, 'Agree'], [3, 'Disagree'], [4, 'Strongly Disagree']],
        label="While playing the game, I forgot worries I had on my mind."
    )
    chase = models.IntegerField(
        choices=[[1, 'Strongly Agree'], [2, 'Agree'], [3, 'Disagree'], [4, 'Strongly Disagree']],
        label="When I lost a round, I wanted to win back my losses as soon as possible."
    )
    greed = models.IntegerField(
        choices=[[1, 'Strongly Agree'], [2, 'Agree'], [3, 'Disagree'], [4, 'Strongly Disagree']],
        label="When I won a round, I felt the urge to win even more."
    )
    pray = models.IntegerField(
        choices=[[1, 'Strongly Agree'], [2, 'Agree'], [3, 'Disagree'], [4, 'Strongly Disagree']],
        label="Praying helped me to win."
    )
    regret = models.IntegerField(
        choices=[[1, 'Strongly Agree'], [2, 'Agree'], [3, 'Disagree'], [4, 'Strongly Disagree']],
        label="I regret playing the game."
    )

    gi_slot = models.IntegerField(
        choices=[[1, 'Very Frequently'], [2, 'Occasionally'], [3, 'Rarely'], [4, 'Never']],
        label="How often do you play slot machines (for example, in casinos or pubs)?."
    )
    gi_money = models.IntegerField(
        choices=[[1, 'Very Frequently'], [2, 'Occasionally'], [3, 'Rarely'], [4, 'Never']],
        label="How often do you play games for money?"
    )
    gi_bet = models.IntegerField(
        choices=[[1, 'Very Frequently'], [2, 'Occasionally'], [3, 'Rarely'], [4, 'Never']],
        label="How often do you bet money on sports competitions?"
    )
    gi_trouble = models.IntegerField(
        choices=[[1, 'Very Frequently'], [2, 'Occasionally'], [3, 'Rarely'], [4, 'Never']],
        label="How often did you get in trouble because of playing/betting?"
    )
    gi_borrow = models.IntegerField(
        choices=[[1, 'Very Frequently'], [2, 'Occasionally'], [3, 'Rarely'], [4, 'Never']],
        label="How often did you borrow money in order to play or bet?"
    )
    gi_lie = models.IntegerField(
        choices=[[1, 'Very Frequently'], [2, 'Occasionally'], [3, 'Rarely'], [4, 'Never']],
        label="How often did you lie to others related to playing and betting?"
    )
    gi_fellacy1 = models.IntegerField(
        choices=[[1, 'Strongly Agree'], [2, 'Agree'], [3, 'Disagree'], [4, 'Strongly Disagree']],
        label="When chance is against you this round, it is more likely that chance will be in your favour in the next round."
    )
    gi_fellacy2 = models.IntegerField(
        choices=[[1, 'Strongly Agree'], [2, 'Agree'], [3, 'Disagree'], [4, 'Strongly Disagree']],
        label="When chance is in your favor this round, it will most likely still be in your favour in the next round."
    )
    gi_strategy = models.IntegerField(
        choices=[[1, 'Strongly Agree'], [2, 'Agree'], [3, 'Disagree'], [4, 'Strongly Disagree']],
        label="You can influence the outcome of chance draws by applying systematic strategies."
    )

    age = models.IntegerField(label='What is your age?', min=13, max=125)
    gender = models.StringField(
        choices=[['Male', 'Male'], ['Female', 'Female'], ['Other', 'Other'], ['Prefer not to tell', 'Prefer not to tell']],
        label='What is your gender?',
        widget=widgets.RadioSelect,
    )
    nationality = models.StringField(label='What is your nationality?')
    religion = models.StringField(label='What is your religion?')
    education = models.IntegerField(
        choices=[[1, 'No formal education'], [2, 'Primary education'], [3, 'Secondary education (High school)'], [4, 'Bachelor degree'], [5, 'Master degree'], [6, 'PhD or higher']],
        label='What is your highest level of education?'
    )
    profession = models.IntegerField(
        choices=[[1, 'No Profession'], [2, 'Arts and Entertainment'], [3, 'Business'], [4, 'Industrial and Manufacturing'], [5, 'Law Enforcement and Armed Forces'], [6, 'Science and Technology'], [7, 'Healthcare and Medicine'], [8, 'Other']],
        label='What is your profession?'
    )
    income = models.IntegerField(
        choices=[[1, 'below 10,000'], [2, 'between 10,000 and 20,000'], [3, 'between 20,000 and 30,000'], [4, 'between 30,000 and 40,000'], [5, 'between 40,000 and 50,000'], [6, 'higher than 50,000']],
        label='What is your (approximate) annual income (in GBP)?'
    )

    mistakes = models.IntegerField()

    def set_payoffs(self) -> object:
        if self.checkq == 1:
            self.mistakes = 0
            self.payoff = 80
        else:
            self.mistakes = 1
            self.payoff = 0
        self.participant.vars['survey_payoff'] = self.payoff
        self.participant.vars['survey_mistakes'] = self.mistakes

        self.risk_payoff = self.participant.vars['scl_payoff']
        self.survey_payoff = self.payoff
        self.quiz_payoff = self.participant.vars['quiz_payoff']
        self.game_payoff = self.participant.vars['game_payoff']
        self.total_payoff = 600 + self.risk_payoff + self.payoff + self.game_payoff
        self.euro_payoff = round(float(self.total_payoff/800)+ 1/8000,2)