from tcheckerpy.routers import tck_compare, tck_liveness, tck_reach, tck_simulate, tck_syntax
import asyncio
import os

system_declaration_path = os.path.join(os.path.dirname(__file__), "examples/ad94.tck")
with open(system_declaration_path) as file:
    system = file.read()

def test_tck_compare():
    body = tck_compare.TckCompareBody(
        first_sysdecl=system,
        second_sysdecl=system,
        relationship=0
    )

    result = asyncio.run(tck_compare.compare(body))
    assert "RELATIONSHIP_FULFILLED true" in result["stats"]

def test_tck_liveness():
    body = tck_liveness.TckLivenessBody(
        sysdecl=system,
        labels="",
        algorithm=0,
        certificate=2
    )

    result = asyncio.run(tck_liveness.liveness(body))
    assert "CYCLE false" in result["stats"]
    assert result["certificate"] == ""

def test_tck_reach():
    body = tck_reach.TckReachBody(
        sysdecl=system, 
        labels="", 
        algorithm=0,
        search_order="bfs",
        certificate=0
    )

    result = asyncio.run(tck_reach.reach(body))
    assert "REACHABLE false" in result["stats"]
    assert not result["certificate"] == ""

def test_tck_simulate():
    body = tck_simulate.TCKSimulationRequest(
        sysdecl=system,
        simulation_type=1
    )

    first_step = '{"initial":[{"status":1,' \
                 '"state":{"intval":"","labels":"",' \
                 '"vloc":"<l0>",' \
                 '"zone":"(x==0 && y==0 && x==y)"},' \
                 '"transition":{"guard":"","reset":"","src_invariant":"","sync":"","tgt_invariant":"","vedge":"<>"}}]}'

    result = asyncio.run(tck_simulate.simulate_tck(body))
    assert result.body.decode() == first_step


def test_tck_syntax():
    assert tck_syntax.check(system)["status"] == "success" 