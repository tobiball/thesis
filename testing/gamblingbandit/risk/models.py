from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

author = 'Felix Holzmeister'
doc = """
Lottery choice task as proposed by Eckel/Grossman (2002), Evolution and Human Behavior 23 (4), 281–295.
"""


# ******************************************************************************************************************** #
# *** CLASS CONSTANTS *** #
# ******************************************************************************************************************** #
class Constants(BaseConstants):

    # ---------------------------------------------------------------------------------------------------------------- #
    # --- Task-specific Settings --- #
    # ---------------------------------------------------------------------------------------------------------------- #

    # number_task (N) of lotteries with <i = 1, 2, ..., N>
    num_lotteries = 5

    # sure_payoff; "low" and "high" payoff of the initial lottery (in currency units set in settings.py)
    # <sure_payoff> determines the 'starting point' for all lotteries in the single choice list (safe option in i = 1)
    # outcomes of subsequent lotteries are defined relative to the 'initial value' by the <delta> options below
    sure_payoff = 640

    # increments of lottery outcomes (refer to the documentation for more detailed information)
    # <delta_lo> defines the (negative) increment of the low outcome over the number_task of choices (<num_lotteries>)
    # similarly, <delta_hi> defines the (positive) increment of the high outcome for the <num_lotteries> choices
    delta_lo = 160
    delta_hi = 320

    # probability of lottery outcome "high" (in percent)
    # <probability> refers to the likelihood of outcome <lottery_hi> denoted in percent (as Integer or Float)
    # i.e. <probability = x> implies an x%-chance to win the "high" and a (1-x)%-chance to win the "low" payoff
    # note that the probability in this task is constant for each of the <num_lotteries> and only outcomes change
    probability = 50

    # additional lottery to separate risk-loving from risk-neutral preferences
    # if <risk_loving = True>, a lottery with the same expected value but a higher st. dev. as lottery <N> is added
    # note that <risk_loving = True> implies that the overall number_task of lotteries rendered will be <num_lotteries> + 1
    risk_loving = False

    # ---------------------------------------------------------------------------------------------------------------- #
    # --- Overall Settings and Appearance --- #
    # ---------------------------------------------------------------------------------------------------------------- #

    # order choices between lottery pairs randomly
    # if <random_order = True>, the ordering of binary decisions is randomized for display
    # if <random_order = False>, binary choices are listed in ascending order of the probability of the "high" outcome
    random_order = False

    # show instructions page
    # if <instructions = True>, a separate template "Instructions.html" is rendered prior to the task
    # if <instructions = False>, the task starts immediately (e.g. in case of printed instructions)
    instructions = True

    # show meta_results_fp page summarizing the task's outcome including payoff information
    # if <meta_results_fp = True>, a separate page containing all relevant information is displayed after finishing the task
    # if <meta_results_fp = False>, the template "Decision.html" will not be rendered
    results = True

    # ---------------------------------------------------------------------------------------------------------------- #
    # --- oTree Settings --- #
    # ---------------------------------------------------------------------------------------------------------------- #
    name_in_url = 'scl'
    players_per_group = None
    num_rounds = 1

# ******************************************************************************************************************** #
# *** CLASS SUBSESSION *** #
# ******************************************************************************************************************** #
class Subsession(BaseSubsession):

    def creating_session(self):
        for p in self.get_players():

            n = Constants.num_lotteries

            # create list of lottery indices
            # --------------------------------------------------------------------------------------------------------
            indices = [j for j in range(1, n + 1)]

            # create list of low and high outcomes (matched by index)
            # --------------------------------------------------------------------------------------------------------
            outcomes_lo = [c(Constants.sure_payoff - Constants.delta_lo * j) for j in range(0, n)]
            outcomes_hi = [c(Constants.sure_payoff + Constants.delta_hi * j) for j in range(0, n)]

            # append indices and outcomes by "risk loving" lottery if <risk_loving = True>
            # --------------------------------------------------------------------------------------------------------
            if Constants.risk_loving:
                indices.append(n + 1)
                outcomes_lo.append(c(outcomes_lo[-1] - Constants.delta_hi))
                outcomes_hi.append(c(outcomes_hi[-1] + Constants.delta_hi))

            # create list of lotteries
            # --------------------------------------------------------------------------------------------------------
            p.participant.vars['scl_lotteries'] = list(
                zip(indices, outcomes_lo, outcomes_hi)
            )

            # randomize order of lotteries if <random_order = True>
            # --------------------------------------------------------------------------------------------------------
            if Constants.random_order:
                random.shuffle(
                    p.participant.vars['scl_lotteries']
                )


# ******************************************************************************************************************** #
# *** CLASS GROUP *** #
# ******************************************************************************************************************** #
class Group(BaseGroup):
    pass


# ******************************************************************************************************************** #
# *** CLASS PLAYER *** #
# ******************************************************************************************************************** #
class Player(BasePlayer):

    # add model fields to class player
    # ----------------------------------------------------------------------------------------------------------------
    lottery_choice = models.IntegerField()
    outcome_to_pay = models.StringField()
    outcome_lo = models.CurrencyField()
    outcome_hi = models.CurrencyField()

    # set payoffs
    # ----------------------------------------------------------------------------------------------------------------
    def set_payoffs(self) -> object:

        # choose outcome to pay (high or low) dependent on <probability>
        # ------------------------------------------------------------------------------------------------------------
        p = Constants.probability
        rnd = random.randint(1, 100)
        self.outcome_to_pay = "B" if rnd <= p else "A"

        # select lottery choice out of list of lotteries
        # ------------------------------------------------------------------------------------------------------------
        lottery_selected = [i for i in self.participant.vars['scl_lotteries'] if i[0] == self.lottery_choice]
        lottery_selected = lottery_selected[0]

        # store payoffs of chosen lottery in the model
        # ------------------------------------------------------------------------------------------------------------
        self.outcome_lo = lottery_selected[1]
        self.outcome_hi = lottery_selected[2]

        # set player's payoff
        # ------------------------------------------------------------------------------------------------------------
        if self.outcome_to_pay == "B":
            self.payoff = self.outcome_hi
        else:
            self.payoff = self.outcome_lo

        # set global variables
        # ------------------------------------------------------------------------------------------------------------

        self.participant.vars['scl_payoff'] = self.payoff
        self.participant.vars['lottery_choice'] = self.lottery_choice
        self.participant.vars['outcome_lo'] = self.outcome_lo
        self.participant.vars['outcome_hi'] = self.outcome_hi
        self.participant.vars['outcome_to_pay'] = self.outcome_to_pay