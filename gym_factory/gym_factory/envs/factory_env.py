import gym
from gym import error, spaces, logger
from gym.utils import seeding
import numpy as np

# [] : ordered - flow, () : not ordered - parallel, {} single job
EXAMPLE_JOB = (
    {
        "name" : 'eagle',
        "job" : {'3DP': 300}, # single job
        "count" : 1
    },
    {
        "name" : 'box',
        "job" : ({'3DP': 300}, {'3DP': 300}), # parallel job
        "count" : 2
    },
    {
        "name" : 'clock',
        "job" : [ # job shop
            (
                (
                    [{'3DP': 200},{'CNC':10}],
                    [{'3DP': 200},{'CNC':5}]
                ),
                {'3DP': 100}
            ),
            {'CNC' : 10},
            {'Vapor' : 5}
        ],
        "count" : 1
    }
)
GENERATE_JOB_MESSAGE = "Overload generate_job method plz like " + EXAMPLE_JOB

def job_reader(job_tree):
    if isinstance(job_tree, dict):
        job_reader.sequence.append(job_tree)
        return job_tree
    elif isinstance(job_tree, tuple):
        tt = list(map(tuple, zip(*map(job_reader, job_tree))))
        job_reader.sequence.append('<assem>')
        return tt
    elif isinstance(job_tree, list):
        tt= list(map(list, zip(*map(job_reader, job_tree))))
        job_reader.sequence.append('<flow>')
        return tt
    else:
        raise ValueError("Unknown job")

class FactoryEnv(gym.Env):
    """
    Factory Environment
    """
    metadata = {
        "render.modes":["human","array"]
    }

    def __init__(self, machine_map, job_type, job_slot):
        """
        Args:
            machine_map : machine type and (count, capa)
                - {'3DP': (5, 480), 'CNC': (1, 1000), 'VAPOR':(1,1000)}
            job_type : ['single','parallel','flow','flexible_flow','job','open']
                - See Example JOB
        """
        self.machine_map = machine_map
        self.job_type = job_type
        self.job_slot = job_slot

        self._reset()

    def _step(self, action):
        state_cur = self.get_state(self.machines_remain_capa, self.remain_jobs)
        self.machines_remain_capa, self.remain_jobs = self._next_state(self.get_state(self.machines_remain_capa, self.remain_jobs), action)
        
        if self._goal_test(self.get_state(self.machines_remain_capa, self.remain_jobs)):
            reward = +1
            done = True
        elif self.get_state(self.machines_remain_capa, self.remain_jobs) == state_cur: # move wrong
            reward = -1
            done = False
        else:
            reward = -0.01
            done = False

        info = {}

        return self._get_obs(), reward, done, info

    def _reset(self):
        # Initialize state
        self.machines_remain_capa = self.initalize_factory() # state 1
        self.remain_jobs = self.generate_jobs() # state 2

    def _render(self, mode='human',close=False):
        raise ValueError("Not yet")

    def _goal_test(self, state):
        raise ValueError("Not yet")

    def _next_state(self, state, action):
        raise ValueError("Not yet")

    def _get_obs(self):
        raise ValueError("Not yet")

    def get_full_obs(self):
        raise ValueError("Not yet")

    def get_partial_obs(self):
        raise ValueError("Not yet")

    #### utils ####
    def generate_job(self):
        """need overload"""
        raise ValueError(GENERATE_JOB_MESSAGE)
    
    def generate_jobs(self):
        temp_job = self.generate_job()
        if not (
            isinstance(temp_job, tuple) and
            isinstance(temp_job[0], dict) and
            temp_job[0].keys() == ['name','job','count']
            ):
            raise ValueError(GENERATE_JOB_MESSAGE)
        return temp_job

    def initalize_factory(self):
        """initalize factory machine's capa"""
        capa = {}
        
        for machine_type in self.machine_map.keys():
            capa[machine_type] = [self.machine_map[machine_type][1]]
            for _ in range(1, self.machine_map[machine_type][0]):
                capa[machine_type].append(self.machine_map[machine_type][1])
        return capa

    def get_state(self, machine_capa, job):
        return None