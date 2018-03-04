# job_reader.sequence = []
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

def get_job_slots_uses(job_slots):
    each = {}
    for index, slot in enumerate(job_slots):
        temp_sum = 0
        for value in slot:
            temp_sum += value[0]
        each[index] = temp_sum
    return each

def find_min_usage(job_slots):
    each = get_job_slots_uses(job_slots)
    min_slot_index = min(each, key=each.get)

    return min_slot_index

def allocate_jobsTojobslots(jobs, job_slots):

    for job in jobs:
        job_reader.sequence = []
        job_reader(job['job'])
        # allocate job to job_slot
        flow_uses = set() # {index: value, }
        target_slot_index = find_min_usage(job_slots)
        assem_num = 0
        for single_job in job_reader.sequence:
            if single_job == '<flow>': # change job_slot
                target_slot_index = find_min_usage(job_slots)
            elif single_job =='<assem>': # stack to max flow job_slot
                assem_num += 1
                job_slot_uses = get_job_slots_uses(job_slots)
                not_used_slot = set(job_slot_uses.keys()) - flow_uses
                not_used_slot = list(not_used_slot)
                for key in not_used_slot:
                    job_slot_uses.pop(key,None)
                target_slot_index = max(job_slot_uses, key=job_slot_uses.get)
                flow_uses = set()
            elif isinstance(single_job, dict): # allocating job to job_slot
                job_slots[target_slot_index].append([list(single_job.items())[0][1], list(single_job.items())[0][0], job['name']+'_'+str(assem_num)]) # [job_capa(int), working_machine(str), job_id(str)]
                flow_uses.add(target_slot_index)       

    return job_slots