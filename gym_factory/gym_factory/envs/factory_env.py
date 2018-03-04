import gym
from gym import error, spaces, logger
from gym.utils import seeding

from env_util import sample_job_gen
from job_slot_util import get_job_slots_uses, find_min_usage, allocate_jobsTojobslots
from machine_util import initalize_factory
from job_util import generate_jobs
from selective_masking import calculate_mask

import numpy as np

class FactoryEnv(gym.Env):
    """
    Factory Environment
    """
    metadata = {
        "render.modes":["matrix","number"]
    }

    def __init__(self, machine_map, job_type, job_slot_num, generate_job_func=sample_job_gen):
        """
        Args:
            machine_map : machine type and (count, capa)
                - {'3DP': (5, 480), 'CNC': (1, 1000), 'VAPOR':(1,1000)}
            job_type : ['single','parallel','flow','flexible_flow','job','open']
                - See Example JOB
            job_slot_num : int ( 10 )
        """
        self.generate_job = generate_job_func
        self.machine_map = machine_map
        self.job_type = job_type
        self.job_slot_num = job_slot_num

        self._reset()

    def _step(self, action):
        state_cur = self.get_state()
        self._next_state(action) # self.machines_remain_capa, self.job_slots
        
        if self._goal_test():
            reward = +1
            done = True
        elif self.get_state() == state_cur: # move wrong
            reward = -1
            done = False
        else:
            reward = -0.01
            done = False

        info = {}

        return self._get_obs(), reward, done, info

    def _reset(self):
        # Initialize state
        self.machines_remain_capa = initalize_factory(self.machine_map) # state 1 ( factory )
        jobs = generate_jobs(self.generate_job)
        self.job_slots = [] # state 2 ( job )
        for i in range(self.job_slot_num):
            self.job_slots.append([])
        
        self.machine_types = list(self.machines_remain_capa.keys())

        self.machine_type_list = []
        
        for mtype in self.machine_types:
            for _ in self.machines_remain_capa[mtype]:
                self.machine_type_list.append(mtype)
        
        self.job_slots = allocate_jobsTojobslots(jobs, self.job_slots)

    def _render(self, mode='human',close=False):
        raise ValueError("Not yet")

    def _goal_test(self):
        # Caution : Do not access to mask info check with capa

        # check job_slot_empty == all job allocated
        # check job can't allocate to remain job
        flag = True
        for job_slot in self.job_slots:
            if len(job_slot) > 0:
                for remain_capa in self.machines_remain_capa[job_slot[0][1]]:
                    if job_slot[0][0] <= remain_capa:
                        flag = False
                        return flag
         
        return flag

    def _next_state(self, action):
        # action == one job allocate from job_slot to machine
        # 2D matrix
        allocate_job_slot, allocate_machine = np.where(np.asarray(action))
        allocate_job_slot = allocate_job_slot[0]
        allocate_machine_num = allocate_machine[0]

        num = 0
        
        break_out = False
        for mtype in self.machine_types:
            for count, _ in enumerate(self.machines_remain_capa[mtype]):
                if num == allocate_machine_num:
                    allocate_machine_type = mtype
                    allocate_machine_type_num = count
                    break_out = True
                num+=1
            if break_out:
                break
        
        try:
            job = self.job_slots[allocate_job_slot].pop(0)
            temp_capa = self.machines_remain_capa[allocate_machine_type][allocate_machine_type_num]
            temp_capa -= job[0]
            if temp_capa < 0:
                raise ValueError("too much minus | remain_machine_capa : " + str(temp_capa) + ' | allocated capa : ' + str(job[0]) + '_' + 
                str(self.machines_remain_capa[allocate_machine_type][allocate_machine_type_num]))
            self.machines_remain_capa[allocate_machine_type][allocate_machine_type_num] = temp_capa

        except ValueError as e:
            print(e)

    def _get_obs(self):
        raise ValueError("Not yet")

    def get_full_obs(self):
        raise ValueError("Not yet")

    def get_partial_obs(self):
        raise ValueError("Not yet")

    def get_state(self, mode='number'):
        if mode == 'number':
            ret = []
            # get machine remain capa
            
            for mtype in self.machine_types:
                for remain_capa in self.machines_remain_capa[mtype]:
                    ret.append(remain_capa)

            # job_slot remain
            ret.append(calculate_mask(self.job_slots, self.machines_remain_capa, self.machine_types))
            
        else:
            raise ValueError("Not Implemented")

        return ret 
    
    def rule_based_mask(self):
        raise ValueError("Working")