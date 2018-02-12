from gym.envs.registration import register

register(
    id='factory-v0',
    entry_point='gym_factory.envs:FactoryEnv_S'
)

register(
    id='factory-v0',
    entry_point='gym_factory.envs:FactoryEnv_PM'
)

register(
    id='factory-v0',
    entry_point='gym_factory.envs:FactoryEnv_FS'
)

register(
    id='factory-v0',
    entry_point='gym_factory.envs:FactoryEnv_FFS'
)

register(
    id='factory-v0',
    entry_point='gym_factory.envs:FactoryEnv_OS'
)

register(
    id='factory-v0',
    entry_point='gym_factory.envs:FactoryEnv_JS'
)