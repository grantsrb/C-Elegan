import gym
import c_elegan
import numpy as np

env = gym.make('CElegan-v0')

obs = env.reset()

for i in range(100):
    print("iter:", i)
    #action = np.random.randint(0,4)
    inp = str(input("\ninput action:"))
    action = 1
    if inp == 'a':
        action = 0
    elif inp == 'd':
        action = 2
    obs, rew, done, info = env.step(action)
    print("obs:", obs)
    print('rew:', rew)
    print('done', done)
    print('info', info)
    env.render(mode='human')
    if done:
        obs = env.reset()
