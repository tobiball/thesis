from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import math
import numpy
import csv
from django.utils.translation import ugettext as _
from . import exp

author = 'Laura Marbacher & Jana B. Jarecki'

doc = """
Risk sensitive foraging
"""


class Constants(BaseConstants):
  name_in_url = 'rsft_gain_loss_experiment'
  players_per_group = None
  num_familiarization_rounds = 2
  num_repetitions = 1
  num_trials = 5
  num_multitrial = num_repetitions + num_familiarization_rounds
  num_oneshot = 0
  num_rounds = exp.num_rounds # in exp.py the number of rounds is calculated
  point_label = _('Punkte')
  trial_label = _('Entscheidung')
  action_label = _('Option')
  initial_state = 0
  num_actions = 2
  lang = 'de'
  attention_fail_error = "Nicht ganz richtig"
  attention_fail_error_e = "Not totally correct"
  duration = 55
  bonus_amount = 0.25


class Subsession(BaseSubsession):
  def concat_stimulus(self, i, stimuli):
    y = "_".join( str(x) for x in ['%.0f' % stimuli[i][0], '%.0f' % (stimuli[i][2] * 100), '%.0f' % stimuli[i][1]] )
    return(y)

  def creating_session(self):
  # Executed at the very start
  # Loops through all the round_numbers and players
    for p in self.get_players():
      if (self.round_number == 1):
        # Initialize the object 'Phasemanager' (see exp.py)
        p.participant.vars['PM'] = exp.Phasemanager(exp.phases, exp.stimuli, exp.blocks, exp.trials)
        # Initialize the object 'Appearancemanager' (see exp.py)
        p.participant.vars['AM'] = exp.Appearancemanager(p.participant.vars['PM'], exp.filepaths, exp.numfeatures, exp.numactions, exp.randomize_feature, exp.randomize_action, exp.randomize_stimulus_order)
      round_number = self.round_number
      phase_number = p.participant.vars['PM'].get_phaseN(round_number)
      phase = p.participant.vars['PM'].get_phaseL(round_number) # phase label
      stimuli = p.participant.vars['AM'].get_stimuli(round_number, phase_number)
      stimulus_position = p.participant.vars['AM'].get_action_position(round_number)
      feature_color = p.participant.vars['AM'].get_feature_appearance(round_number)[0]

      # Store variables
      p.phase = p.participant.vars['PM'].get_phaseL(round_number)
      p.block = p.participant.vars['PM'].get_block(round_number)      
      p.budget = stimuli[2][0]
      p.stimulus0 = self.concat_stimulus(0, stimuli)
      p.stimulus1 = self.concat_stimulus(1, stimuli)
      p.state = stimuli[2][1]
      # this is only if we have one-shot trials in there
      # if (phase in ['critical']):
      #   p.trial = stimuli[2][2]
      # else:
      p.trial = 1
      p.successes = 0

      # Do and store the randomizations
      p.layout_featurecolor = '_'.join(''.join(str(y) for y in x) for x in [feature_color])     
      p.layout_stimulusposition_01 = ''.join(str(x) for x in stimulus_position)

      # Initialize containers
      n = int(Constants.num_rounds + 1)
      if (self.round_number == 1):
        self.session.vars['instruction_rounds'] = p.participant.vars['PM'].get_instruction_rounds()
        p.participant.vars['bonus_rounds'] = p.participant.vars['PM'].get_bonus_rounds()
        p.participant.vars['stimulus_position'] = [None] * n
        p.participant.vars['img1'] = [None] * n
        p.participant.vars['img2'] = [None] * n
        p.participant.vars['max_earnings'] = [None] * n
        p.participant.vars['num_blocks'] = [None] * n
        p.participant.vars['decision_number'] = [None] * n
        p.participant.vars['outcomes'] = [None] * n
      p.participant.vars['stimulus_position'][round_number] = stimulus_position

      # Define the names of teh sprites for the images
      css_img_orig_position = [
        'sprite_' + p.stimulus0 + '_featurecolor' + p.layout_featurecolor,
        'sprite_' + p.stimulus1 + '_featurecolor' + p.layout_featurecolor
          ]
      p.participant.vars['img1'][round_number] = css_img_orig_position[stimulus_position[0]]
      p.participant.vars['img2'][round_number] = css_img_orig_position[stimulus_position[1]]
      if (phase in exp.phases):
        outcomes_orig_position = [p.draw_outcomes(x, Constants.num_trials) for x in p.participant.vars['AM'].get_stimuli(round_number, phase_number)[ :2]]
        p.participant.vars['outcomes'][round_number] = [outcomes_orig_position[i] for i in stimulus_position]
      maxx = max([max(list(map(abs, stimuli[i]))) for i in [0,1]])
      p.participant.vars['max_earnings'][round_number] = max(maxx * (Constants.num_trials), p.budget)
      p.participant.vars['num_blocks'][round_number] = p.participant.vars['PM'].get_num_trials_in_phase(round_number)
      p.participant.vars['decision_number'][round_number] = p.participant.vars['PM'].get_decision_number_in_phase(round_number)

      if (self.round_number == 1):
        p.successes = 0

class Group(BaseGroup):
  pass

# These functions 'make_..._field' generate the hidden html input fiels
#   which will store the responses of participants
def make_choice_field(trial):
  return models.IntegerField(
    doc = "Chosen stimulus in trial" +str(trial) +", this is the stimulus, not the shown stimulus position")

def make_state_field(trial):
  return models.IntegerField(
    doc = "Point state at the beginning of trial" +str(trial))

def make_rt_field(trial):
  return models.FloatField(
    doc = "Reaction time  in ms from the end of the page load until the choice, in trial" +str(trial) +" or until submit, in case of instruction pages.")


# Every round the player object is re-initialized
class Player(BasePlayer):
  # Attention-Check Questions (q1 = ...) and Correct Answers (value != ...)

  # ENGLISH --------------------------------------------------------------

  #Gains
  g1e = models.IntegerField(
    label = "What is the number of the current decision?")
  def g1e_error_message(self, value):
    if value != 3:
      return Constants.attention_fail_error_e # error msg is defined above

  g2e = models.IntegerField(
    label = "How high is the threshold?")
  def g2e_error_message(self, value):
    if value != 0:
      return Constants.attention_fail_error_e

  g3e = models.IntegerField(label = "How high is the current score?")
  def g3e_error_message(self, value):
    if value != -13:
      return Constants.attention_fail_error_e

  g4e = models.IntegerField(label = "What is the maximum number of points that the right option offers?")
  def g4e_error_message(self, value):
    if value != 9:
      return Constants.attention_fail_error_e

  # Losses
  l1e = models.IntegerField(
    label="How high is the threshold?")
  def l1e_error_message(self, value):
    if value != 0:
      return Constants.attention_fail_error_e

  l2e = models.IntegerField(label="How high is the current score?")
  def l2e_error_message(self, value):
    if value != 11:
      return Constants.attention_fail_error_e

  l3e = models.IntegerField(
    label = "What is the probability, that the right option deducts 2 points? (Number from 1-100)?")
  def l3e_error_message(self, value):
    if value != 60:
      return Constants.attention_fail_error_e

  l4e = models.IntegerField(
    label = "How high is the starting score?")
  def l4e_error_message(self, value):
    if value != 21:
      return Constants.attention_fail_error_e

  # Coverstory 0
  c1e = models.IntegerField(
    widget = widgets.RadioSelect,
    label = "In rounds, in which points are increasing, your goal is...",
    choices = [
      [1, "to meet or to exceed the threshold."],
      [2, "not to meet and not to exceed the threshold."],
      [3, "There is no goal."]
    ])
  def c1_error_message(self, value):
    if value != 1:
      return Constants.attention_fail_error

  c2e = models.BooleanField(
    widget = widgets.RadioSelectHorizontal,
    label = "Imagine you are in a round, in which points are increasing and the threshold is 10. Your score in the end of a round is 10 points. This means you...",
    choices = [
      [True, "have reached the goal."],
      [False, "have not reached the goal."]
    ])
  def c2e_error_message(self, value):
    if value == False:
      return Constants.attention_fail_error_e

  c3e = models.BooleanField(
    widget = widgets.RadioSelectHorizontal,
    label = "Imagine you are in a round, in which points are increasing and the threshold is 0. Your score in the end of a round is -2 points. This means you...",
    choices = [
      [False, "have reached the goal."],
      [True, "have not reached the goal."]
    ])
  def c3e_error_message(self, value):
    if value == False:
      return Constants.attention_fail_error_e

  c4e = models.IntegerField(
    widget = widgets.RadioSelect,
    label="In rounds, in which points are decreasing, your goal is...",
    choices=[
      [1, "to fall below the threshold."],
      [2, "not to fall below the threshold."],
      [3, "There is no goal."]
    ])
  def c4e_error_message(self, value):
    if value != 2:
      return Constants.attention_fail_error_e

  c5e = models.BooleanField(
    widget = widgets.RadioSelectHorizontal,

    label="Imagine you are in a round, in which points are decreasing and the threshold is -10 points. Your score in the end of a round is -11 points. This means you...",
    choices=[
      [False, "have reached the goal."],
      [True, "have not reached the goal."]
    ])
  def c5e_error_message(self, value):
    if value == False:
      return Constants.attention_fail_error_e

  c6e = models.BooleanField(
    widget = widgets.RadioSelectHorizontal,
    label="Imagine you are in a round, in which points are decreasing and the threshold is -10 points. Your score in the end of a round is -10 points. This means you...",
    choices=[
      [True, "have reached the goal."],
      [False, "have not reached the goal."]
    ])
  def c6e_error_message(self, value):
    if value == False:
      return Constants.attention_fail_error_e

  c7e = models.BooleanField(
    widget = widgets.RadioSelectHorizontal,
    label="Imagine you are in a round, in which points are decreasing and the threshold is 0 points. Your score in the end of a round is 3 points. This means you...",
    choices=[
      [True, "have reached the goal."],
      [False, "have not reached the goal."]
    ])
  def c7e_error_message(self, value):
    if value == False:
      return Constants.attention_fail_error_e

  #Incentives
  i4e = models.IntegerField(
    label="Which of the subsequent rounds are relevant for your bonus payment?",
    choices=[
      [1, "The first four rounds are relevant."],
      [2, "The last five rounds are relevant."],
      [3, "Each round is relevant, because four bonus rounds will be randomly drawn."]
    ])
  def i4_error_message(self, value):
    if value != 3:
      return Constants.attention_fail_error

  # GERMAN------------------------------------------------------------------
    # Gains
    g1 = models.IntegerField(
      label="Die wievielte Entscheidung treffen Sie gerade?")

    def g1_error_message(self, value):
      if value != 3:
        return Constants.attention_fail_error  # error msg is defined above

    g2 = models.IntegerField(
      label="Wie hoch ist der Schwellenwert?")

    def g2_error_message(self, value):
      if value != 0:
        return Constants.attention_fail_error

    g3 = models.IntegerField(label="Wie hoch ist Ihr Punktestand?")

    def g3_error_message(self, value):
      if value != -13:
        return Constants.attention_fail_error

    g4 = models.IntegerField(label="Wie viele Punkte ergibt die rechte Option maximal?")

    def g4_error_message(self, value):
      if value != 9:
        return Constants.attention_fail_error

    # Losses
    l1 = models.IntegerField(
      label="Wie hoch ist der Schwellenwert?")

    def l1_error_message(self, value):
      if value != 0:
        return Constants.attention_fail_error

    l2 = models.IntegerField(label="Wie hoch ist Ihr Punktestand?")

    def l2_error_message(self, value):
      if value != 11:
        return Constants.attention_fail_error

    l3 = models.IntegerField(
      label="Mit welcher Wahrscheinlichkeit ergibt die rechte Option -2 Punkte? (Zahl von 0-100)")

    def l3_error_message(self, value):
      if value != 60:
        return Constants.attention_fail_error

    l4 = models.IntegerField(
      label="Wie hoch ist der Startwert?")

    def l4_error_message(self, value):
      if value != 21:
        return Constants.attention_fail_error

    # Coverstory 0
    c1 = models.IntegerField(
      widget=widgets.RadioSelect,
      label="Ihr Ziel beim Punkte sammeln ist es ...",
      choices=[
        [1, "den Schwellenwert zu erreichen oder zu überschreiten."],
        [2, "den Schwellenwert nicht zu erreichen und nicht zu überschreiten."],
        [3, "Es gibt keine Zielvorgabe."]
      ])

    def c1_error_message(self, value):
      if value != 1:
        return Constants.attention_fail_error

    c2 = models.BooleanField(
      widget=widgets.RadioSelectHorizontal,
      label="Angenommen Sie sind beim Punkte sammeln und der Schwellenwert beträgt 10 Punkte. Ihr Punktestand am Ende der Runde ist 10. Dann haben Sie ...",
      choices=[
        [True, "das Ziel erreicht."],
        [False, "das Ziel nicht erreicht."]
      ])

    def c2_error_message(self, value):
      if value == False:
        return Constants.attention_fail_error

    c3 = models.BooleanField(
      widget=widgets.RadioSelectHorizontal,
      label="Angenommen Sie sind beim Punkte sammeln und der Schwellenwert beträgt 0 Punkte. Ihr Punktestand am Ende der Runde ist -2. Dann haben Sie ...",
      choices=[
        [False, "das Ziel erreicht."],
        [True, "das Ziel nicht erreicht."]
      ])

    def c3_error_message(self, value):
      if value == False:
        return Constants.attention_fail_error

    c4 = models.IntegerField(
      widget=widgets.RadioSelect,
      label="Ihr Ziel beim Punkte abgeben ist es...",
      choices=[
        [1, "den Schwellenwert zu erreichen oder zu unterschreiten."],
        [2, "den Schwellenwert nicht zu unterschreiten."],
        [3, "Es gibt keine Zielvorgabe."]
      ])

    def c4_error_message(self, value):
      if value != 2:
        return Constants.attention_fail_error

    c5 = models.BooleanField(
      widget=widgets.RadioSelectHorizontal,
      label="Angenommen Sie sind beim Punkte abgeben und der Schwellenwert beträgt -10 Punkte. Ihr Punktestand am Ende der Runde ist -11. Dann haben Sie ...",
      choices=[
        [False, "das Ziel erreicht."],
        [True, "das Ziel nicht erreicht."]
      ])

    def c5_error_message(self, value):
      if value == False:
        return Constants.attention_fail_error

    c6 = models.BooleanField(
      widget=widgets.RadioSelectHorizontal,
      label="Angenommen Sie sind beim Punkte abgeben und der Schwellenwert beträgt -10 Punkte. Ihr Punktestand am Ende der Runde ist -10. Dann haben Sie...",
      choices=[
        [True, "das Ziel erreicht."],
        [False, "das Ziel nicht erreicht."]
      ])

    def c6_error_message(self, value):
      if value == False:
        return Constants.attention_fail_error

    c7 = models.BooleanField(
      widget=widgets.RadioSelectHorizontal,
      label="Angenommen Sie sind beim Punkte abgeben und der Schwellenwert beträgt 0 Punkte. Ihr Punktestand am Ende der Runde ist 3. Dann haben Sie...",
      choices=[
        [True, "das Ziel erreicht."],
        [False, "das Ziel nicht erreicht."]
      ])

    def c7_error_message(self, value):
      if value == False:
        return Constants.attention_fail_error

    # Incentives
    i1 = models.IntegerField(
      widget=widgets.RadioSelectHorizontal,
      label="... das Ziel in keiner der 5 relevanten Runden erreicht wurde?",
      choices=[0, 1, 2, 3, 4, 5, 6, 7, 8])

    def i1_error_message(self, value):
      if value != 1:
        return Constants.attention_fail_error  # error msg is defined above

    i2 = models.IntegerField(
      widget=widgets.RadioSelectHorizontal,
      label="... das Ziel in 5 von 5 relevanten Runden erreicht wurde?",
      choices=[0, 1, 2, 3, 4, 5, 6, 7, 8])

    def i2_error_message(self, value):
      if value != 6:
        return Constants.attention_fail_error

    i3 = models.IntegerField(
      widget=widgets.RadioSelectHorizontal,
      label="... das Ziel in 2 von 5 relevanten Runden erreicht wurde?",
      choices=[0, 1, 2, 3, 4, 5, 6, 7, 8])

    def i3_error_message(self, value):
      if value != 3:
        return Constants.attention_fail_error

    i4 = models.IntegerField(
      label="Welche der nachfolgenden Runden sind relevant für Ihren Gewinnchancen?",
      choices=[
        [1, "Die ersten 5 Runden sind relevant."],
        [2, "Die letzten 5 Runden sind relevant."],
        [3, "Jede Runde ist relevant: es werden fünf Runden zufällig gezogen."]
      ])

    def i4_error_message(self, value):
      if value != 3:
        return Constants.attention_fail_error

  #
  # Variables needed in the experiment
  # --------------------------------------------------------------------------
  # prolificid = models.StringField(
  #  doc = "ID of the survey provider")
  browser = models.StringField(
    doc = "Browser and version", blank=True)
  phase = models.StringField(
    doc = "Phases during the experiment. Familiarization phase is not incentivized.")
  block = models.IntegerField(
    doc = "Current block")
  trial = models.FloatField(
    doc = "Current trial of 5")
  stimulus0 = models.StringField(
    doc = "Risky gamble number one, format x1_p1_x2.")
  stimulus1 = models.StringField(
    doc = "Risky gamble number two, format x1_p2_x2.")
  state = models.FloatField(
    doc = "Accumulated points before the current decision")
  budget = models.FloatField(
    doc = "Earnings requirement in current block")
  choice1 = make_choice_field(1)
  choice2 = make_choice_field(2)
  choice3 = make_choice_field(3)
  choice4 = make_choice_field(4)
  choice5 = make_choice_field(5)
  state1  = make_state_field(1)
  state2  = make_state_field(2)
  state3  = make_state_field(3)
  state4  = make_state_field(4)
  state5  = make_state_field(5)
  state6  = make_state_field(6)
  rt_ms1 = make_rt_field(1)
  rt_ms2 = make_rt_field(1)
  rt_ms3 = make_rt_field(1)
  rt_ms4 = make_rt_field(1)
  rt_ms5 = make_rt_field(1)
  success = models.IntegerField(doc = "Indicator if in the current block the earnings requirement (budget) was reached, 1 if yes, 0 otherwise")
  # outcome = models.IntegerField(doc = "Randomly drawn outcome of the chosen option given the choice in this trial")
  successes = models.FloatField(initial = 0, doc = "Count of the total number of blocks where the earnings requirement (budget) was reached")
  rt_ms = models.FloatField(
    doc = "Reaction time from the end of the page load until the choice or until submit, in case of instruction pages.")
  layout_featurecolor = models.StringField(
    doc = "Layout: Randomized feature colors per trial (light vs dark grey), 01 means that in this trial feature x1 was light grey and feature x2 dark grey, 10 means that x1 was dark grey and x2 light grey.")
  layout_stimulusposition_01 = models.StringField(
    doc = "Layout: Randomized stimulus position per trial (left vs right). 01 means that stimulus1 was shown left, 10 means that stimulus1 was shown right.")


  def draw_outcomes(self, action, size):
    p = action[2: ][1]
    indices = numpy.random.binomial(n=1, p=p, size=size)
    #indices = [0, 1, 0, 1, 1, 0, 1, 0, 1, 1]
    x = action[ :2]
    res = [x[i] for i in indices]
    return res


  def get_last_state(self):
    if (self.round_number > 1):
      lastself = self.in_round(self.round_number - 1)
      return lastself.state + lastself.outcome
    else:
      return self.state

  def update_successes(self):
    n_ignore = Constants.num_familiarization_rounds
    successes = 0
    if (self.round_number >  n_ignore):
      successes = sum([p.success for p in self.in_rounds(n_ignore + 1, self.round_number - 1)])
      self.successes = successes
    return(successes)
    
  
  def get_last_success(self):
    round_num_ignore = 1 + Constants.num_familiarization_rounds
    if (self.round_number > round_num_ignore):
      return self.in_round(self.round_number - 1).success
    else:
      return 0


  # Variables that can be used in the html pages to show
  def vars_for_template(self):
    n = self.round_number
    return {
      'img1': self.participant.vars['img1'][n],
      'img2': self.participant.vars['img2'][n],
      'stimulus_position': self.participant.vars['stimulus_position'][n],
      'state': self.state,
      'budget': self.budget,
      'trial': self.trial,
      'max_earning': self.participant.vars['max_earnings'][n],
      'max_less_state': self.participant.vars['max_earnings'][n] - 0,
      'num_blocks': self.participant.vars['num_blocks'][n],
      'decision_number': self.participant.vars['decision_number'][n],
      'multitrial': self.phase in ['familiarization_gain',"familiarization_loss", 'training']
    }

  def draw_bonus(self):
    if self.round_number in self.participant.vars['bonus_rounds']:
      self.payoff = self.success


