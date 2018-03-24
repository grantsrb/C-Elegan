from gym.envs.registration import register

register(
    id='CElegan-v0',
    entry_point='c_elegan.envs:CEleganEnv',
)
