import tempfile
from enum import Enum
from tcheckerpy.utils import call_tchecker

class SimulationType(Enum):
    # INTERACTIVE = 0 # interactive simulation
    ONESTEP = 1 # one-step simulation (output initial or next states)
    RANDOMIZED = 2 # randomized simulation

def simulate_tck(sys_decl: str, simulation_type: SimulationType,
                 starting_state: str | None = None, nsteps: int | None = None) -> str:
    """
    Checks for reachability of timed automaton.

    :param sys_decl: system declaration of timed automaton
    :param simulation_type: simulation type (see `tck_reach.SimulationType`)
    :param starting_state: starting state, specified as a JSON object with keys vloc, intval and zone
                           vloc: comma-separated list of location names (one per process), in-between < and >
                           intval: comma-separated list of assignments (one per integer variable)
                           zone: conjunction of clock-constraints (following TChecker expression syntax)
    :param nsteps: number of steps for randomized simulation (obligatory for randomized simulation, omitted otherwise)
    :return: initial state/next states for one-step simulation, simulation trace for randomized simulation
    """
    
    if simulation_type == SimulationType.RANDOMIZED and nsteps == None:
        raise ValueError("Randomized simulation requires number of steps")
    
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(sys_decl.encode('utf-8'))
        temp_file_path = temp_file.name

    # call TChecker function
    _, result = call_tchecker.call_tchecker_function_in_new_process(
        func_name="tck_simulate",
        argtypes=["ctypes.c_char_p", "ctypes.c_int", "ctypes.c_int", "ctypes.c_char_p", 
                  "ctypes.POINTER(ctypes.c_int)", "ctypes.c_bool"],
        has_result=True,
        args=[temp_file_path, simulation_type.value, 1, starting_state or "",
              nsteps or 0, not simulation_type == SimulationType.ONESTEP] 
    )

    return result


    
