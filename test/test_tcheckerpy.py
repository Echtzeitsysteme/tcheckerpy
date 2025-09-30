from tcheckerpy.routers import tck_compare, tck_liveness, tck_reach, tck_simulate, tck_syntax
import asyncio
import os

test_systems_path = os.path.join(os.path.dirname(__file__), "examples")
with open(os.path.join(test_systems_path, "ad94.tck")) as file:
    system = file.read()
with open(os.path.join(test_systems_path, "ad94_first_step.json")) as file:
    first_step = file.read()
with open(os.path.join(test_systems_path, "ad94.gv")) as file:
    dot_format = file.read()
with open(os.path.join(test_systems_path, "ad94.json")) as file:
    json_format = file.read()
with open(os.path.join(test_systems_path, "ad94_product.tck")) as file:
    product = file.read()

def test_tck_compare():
    assert tck_compare.compare(system, system)[0]

def test_tck_liveness():
    result = tck_liveness.liveness(system, tck_liveness.Algorithm.COUVSCC)
    assert result[0]
    assert result[2] == ""

def test_tck_reach():
    assert not tck_reach.reach(system, tck_reach.Algorithm.COUVSCC)[0]

def test_tck_simulate():
    body = tck_simulate.TCKSimulationRequest(
        sysdecl=system,
        simulation_type=1
    )

    result = asyncio.run(tck_simulate.simulate_tck(body))
    assert result.body.decode().strip() == first_step


def test_tck_syntax():
    tck_syntax.check(system)
    assert tck_syntax.to_dot(system) == dot_format
    assert tck_syntax.to_json(system) == json_format
    assert tck_syntax.create_product(system) == product