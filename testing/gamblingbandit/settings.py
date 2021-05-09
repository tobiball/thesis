from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.00125, participation_fee=0.00, doc=""
)

SESSION_CONFIGS = [
    dict(
        name='gambling_bandit_nc',
        display_name="OAB (NC)",
        num_demo_participants=2,
        #app_sequence=['game_t0', 'game_t2', 'survey', 'summary_partial']
        #app_sequence=['introduction', 'game_instructions_t0', 'game_instructions_t2', 'game_trial_t0', 'game_trial_t2', 'game_t0', 'game_t2', 'survey', 'summary_partial']
        app_sequence = ['introduction', 'risk', 'game_instructions_t0', 'game_instructions_t2', 'game_trial_t0', 'game_trial_t2', 'game_t0', 'game_t2', 'survey', 'summary']
),
    dict(
        name='gambling_bandit_pc',
        display_name="OAB (PC)",
        num_demo_participants=2,
        app_sequence = ['introduction', 'risk', 'game_instructions_t1', 'game_trial_t1', 'game_t1', 'survey', 'summary']
),
#    dict(
#        name='gambling_bandit_pc',
#        display_name="OAB (PC)",
#        num_demo_participants=2,
#        app_sequence = ['introduction', 'risk', 'game_instructions_t1', 'game_instructions_t3', 'game_trial_t1', 'game_trial_t3', 'game_t1', 'game_t3', 'survey', 'summary']
#),
]


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '3ok4a5zlh2c-ri_8-hk(%30slm5a_9m6=&fk5ftk4!7)9r2s+%'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
