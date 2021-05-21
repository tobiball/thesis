from os import environ

SESSION_CONFIGS = [
    dict(
        name='Foraging_Experiment',
        display_name="Foraging Experiment",
        app_sequence=["instructions", "comprehension","foraging_app","fin"],
        num_demo_participants=1,
    ),


    dict(
        name='foraging_test',
        display_name="foraging_test",
        app_sequence=["foraging_test","fin"],
        num_demo_participants=6,
    ),

    dict(
        name='foraging_simulation',
        display_name="foraging_simulation",
        app_sequence=["foraging_simulation","fin"],
        num_demo_participants=100,
    ),
    dict(
        name='instructions',
        display_name="instructions",
        app_sequence=["instructions","fin"],
        num_demo_participants=3,
    ),

    dict(
        name='comprehension',
        display_name="Comprehension",
        app_sequence=['comprehension','fin'],
        num_demo_participants=3,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = ['treatment','trial_in_game','clearing_number','induction_flag','video_nr', "forest_payoff","probability_vector_gain","probability_vector_threat"]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""

SECRET_KEY = '6404025034177'

INSTALLED_APPS = ['otree']