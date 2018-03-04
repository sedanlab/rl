## Future Work : machine can print material type

def calculate_mask(job_slots, machines_remain_capa, machine_types):
    ret = []

    machine_types = machine_types
    machine_type_list = []
    for mtype in machine_types:
        for _ in machines_remain_capa[mtype]:
            machine_type_list.append(mtype)
    
    for jobs in job_slots:
        if len(jobs) > 0:
            # usage capa of job
            capa = jobs[0][0]
            
            mask = []
            # check machine_type
            for mtype in machine_type_list:
                if jobs[0][1] == mtype:
                    mask.append(1)
                else:
                    mask.append(0)

            # check job flow
            if check_pre_job_remain(job_slots, jobs[0][-1]):
                mask = [0 for _ in mask] # make all unavailable
            
            # check can't allocate to machine type
            flag_ = True
            for remain_capa in machines_remain_capa[jobs[0][1]]:
                if remain_capa >= capa:
                    flag_ = False
            if flag_:
                mask = [0 for _ in mask]

        else:
            capa = 0
            mask = [0] * ( 1 + len(machine_type_list)) # zero capa, all unavailable mask
        
        ret.append([capa] + mask)
    return ret

def check_pre_job_remain(job_slots, job_id):
    job_name, job_seq = job_id.split('_')
    job_seq = int(job_seq)
    if job_seq == 0:
        return False
    else:
        check_job_id = job_name + '_' +str(job_seq - 1)
        for jobs in job_slots:
            for job in jobs:
                if job[-1] == check_job_id:
                    return True
    return False