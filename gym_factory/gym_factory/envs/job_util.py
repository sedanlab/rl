from env_util import EXAMPLE_JOB, GENERATE_JOB_MESSAGE

def generate_jobs(generate_job):
    temp_job = generate_job()
    if not (
        isinstance(temp_job, tuple) and
        isinstance(temp_job[0], dict) and
        set(temp_job[0].keys()) == {'name','job'}
        ):
        raise ValueError(GENERATE_JOB_MESSAGE + 'your key is '+str(temp_job[0].keys()))
    return temp_job