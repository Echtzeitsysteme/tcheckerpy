import tempfile
from enum import Enum
from tcheckerpy.utils import call_tchecker

class Algorithm(Enum):
    COUVSCC = 0
    NDFS = 1

class Certificate(Enum):
    GRAPH = 0
    SYMBOLIC = 1
    NONE = 2

def liveness(sys_decl: str, algorithm: Algorithm, certificate: Certificate = Certificate.NONE, 
             labels: list[str] = [], block_size: int | None = None, table_size: int | None = None):

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(sys_decl.encode('utf-8'))
        temp_file_path = temp_file.name
    
    # convert list to string
    labels_str = ", ".join(labels)

    # call the TChecker function
    stats, cert = call_tchecker.call_tchecker_function_in_new_process(
        func_name="tck_liveness",
        argtypes=["ctypes.c_char_p", "ctypes.c_char_p", "ctypes.c_int", "ctypes.c_int",
                  "ctypes.POINTER(ctypes.c_int)", "ctypes.POINTER(ctypes.c_int)"],
        has_result=True,
        args=[temp_file_path, labels_str, algorithm.value, certificate.value,
              block_size, table_size]
    )

    return "CYCLE false" in stats, stats, cert
