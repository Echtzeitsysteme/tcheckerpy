import tempfile
from enum import Enum
from tcheckerpy.utils import call_tchecker

class SimulationType(Enum):
    # INTERACTIVE = 0
    ONESTEP = 1
    RANDOMIZED = 2

def simulate_tck(sys_decl: str, simulation_type: SimulationType,
                 starting_state: str | None = None, nsteps: int | None = None):
    
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


    
