import tempfile
from enum import Enum
from tcheckerpy.utils import call_tchecker

class Relationship(Enum):
    STRONG_TIMED_BISIM = 0 # strong timed bisimilarity

def compare(first_sys_decl: str, second_sys_decl: str, relationship: Relationship = Relationship.STRONG_TIMED_BISIM, 
            generate_witness = False, block_size: int | None = None, table_size: int | None = None) -> tuple[bool, str, str]:
    """
    Checks for bisimilarity of two timed automata.

    \param output_filename Path to the output file (comparison results)
    \param first_sysdecl_filename Path to the first system declaration file
    \param second_sysdecl_filename Path to the second system declaration file
    \param relationship Type of relationship to check (see tck_compare_relationship_t)
    \param block_size Pointer to the block size for internal computation (nullptr for default)
    \param table_size Pointer to the table size for internal computation (nullptr for default)
    \param starting_state_attributes_first
    \param starting_state_attributes_second
    \param inter_constraint
    \param generate_witness
    """
    
    with tempfile.NamedTemporaryFile(delete=False) as temp_file_first_sysdecl:
        temp_file_first_sysdecl.write(first_sys_decl.encode('utf-8'))
        temp_file_path_first_sysdecl = temp_file_first_sysdecl.name
    with tempfile.NamedTemporaryFile(delete=False) as temp_file_second_sysdecl:
        temp_file_second_sysdecl.write(second_sys_decl.encode('utf-8'))
        temp_file_path_second_sysdecl  = temp_file_second_sysdecl.name
        
    # call TChecker function
    stats, witness = call_tchecker.call_tchecker_function_in_new_process(
        func_name="tck_compare",
        argtypes=["ctypes.c_char_p", "ctypes.c_char_p", "ctypes.c_int",
                  "ctypes.POINTER(ctypes.c_int)", "ctypes.POINTER(ctypes.c_int)", "ctypes.c_bool"],
        has_result=True,
        args=[temp_file_path_first_sysdecl, temp_file_path_second_sysdecl, relationship.value, 
              block_size, table_size, None, None, None, generate_witness]
    )

    return "RELATIONSHIP_FULFILLED true" in stats, stats, witness
