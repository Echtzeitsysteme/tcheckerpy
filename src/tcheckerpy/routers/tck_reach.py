import tempfile
from enum import Enum
from tcheckerpy.utils import call_tchecker

class Algorithm(Enum):
    COUVSCC = 0
    NDFS = 1

class SearchOrder(Enum):
    BFS = "bfs"
    DFS = "dfs"

class Certificate(Enum):
    GRAPH = 0
    SYMBOLIC = 1
    CONCRETE = 2
    NONE = 3

def reach(sys_decl: str, algorithm: Algorithm, search_order: SearchOrder = SearchOrder.BFS, 
          certificate: Certificate = Certificate.NONE, labels: list[str] = [],
          block_size: int | None = None, table_size: int | None = None):
    
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(sys_decl.encode('utf-8'))
        temp_file_path = temp_file.name

    # convert list to string
    labels_str = ", ".join(labels)
        
    # call TChecker function
    stats, cert = call_tchecker.call_tchecker_function_in_new_process(
        func_name="tck_reach",
        argtypes=["ctypes.c_char_p", "ctypes.c_char_p", "ctypes.c_int", "ctypes.c_char_p",
                  "ctypes.c_int", "ctypes.POINTER(ctypes.c_int)", "ctypes.POINTER(ctypes.c_int)"],
        has_result=True,
        args=[temp_file_path, labels_str, algorithm.value, search_order.value,
              certificate.value, block_size, table_size]
    )
 
    return "REACHABLE true" in stats, stats, cert
