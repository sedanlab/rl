# [] : ordered - flow, () : not ordered - parallel, {} single job
EXAMPLE_JOB = (
    {
        "name" : 'eagle',
        "job" : [{'3DP': 300}] # single job
    },
    {
        "name" : 'box',
        "job" : ([{'3DP': 300}], [{'3DP': 300}]) # parallel job
    },
    {
        "name" : 'clock',
        "job" : [ # job shop
            (
                (
                    [{'3DP': 200},{'CNC':10}],
                    [{'3DP': 200},{'CNC':5}]
                ),
                [{'3DP': 100}]
            ),
            {'CNC' : 10},
            {'Vapor' : 5}
        ]
    }
)
GENERATE_JOB_MESSAGE = "Overload generate_job method plz like " + str(EXAMPLE_JOB)

def sample_job_gen():
    return EXAMPLE_JOB