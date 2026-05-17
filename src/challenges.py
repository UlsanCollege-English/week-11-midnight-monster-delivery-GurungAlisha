"""Tests for Week 11: Midnight Monster Delivery."""

import pytest
from math import inf
from week11 import (
    HAUNTED_CITY,
    validate_haunted_map,
    monster_delivery_costs,
    shortest_monster_delivery,
    best_next_monster_stop,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def small_graph() -> dict:
    """A simple 3-node graph for quick checks."""
    return {
        "A": {"B": 1, "C": 4},
        "B": {"C": 2},
        "C": {},
    }


@pytest.fixture
def disconnected_graph() -> dict:
    """Graph where one node is unreachable."""
    return {
        "A": {"B": 3},
        "B": {},
        "C": {},          # C is isolated
    }


# ---------------------------------------------------------------------------
# validate_haunted_map
# ---------------------------------------------------------------------------

def test_validate_accepts_valid_graph():
    validate_haunted_map(HAUNTED_CITY)  # should not raise


def test_validate_rejects_non_dict():
    with pytest.raises(ValueError):
        validate_haunted_map("not a graph")  # type: ignore


def test_validate_rejects_non_dict_neighbors():
    with pytest.raises(ValueError):
        validate_haunted_map({"A": ["B"]})  # type: ignore


def test_validate_rejects_unknown_neighbor():
    with pytest.raises(ValueError):
        validate_haunted_map({"A": {"Z": 1}})  # Z not in graph


def test_validate_rejects_zero_weight():
    with pytest.raises(ValueError):
        validate_haunted_map({"A": {"B": 0}, "B": {}})


def test_validate_rejects_negative_weight():
    with pytest.raises(ValueError):
        validate_haunted_map({"A": {"B": -3}, "B": {}})


def test_validate_accepts_small_graph(small_graph):
    validate_haunted_map(small_graph)  # should not raise


# ---------------------------------------------------------------------------
# monster_delivery_costs
# ---------------------------------------------------------------------------

def test_costs_start_is_zero():
    costs = monster_delivery_costs(HAUNTED_CITY, "Crypt Kitchen")
    assert costs["Crypt Kitchen"] == 0


def test_costs_known_values():
    costs = monster_delivery_costs(HAUNTED_CITY, "Crypt Kitchen")
    # Crypt Kitchen → Fog Alley = 2
    assert costs["Fog Alley"] == 2
    # Crypt Kitchen → Fog Alley → Moon Bridge = 2+1 = 3
    assert costs["Moon Bridge"] == 3
    # Crypt Kitchen → Fog Alley → Moon Bridge → Werewolf Den = 3+5 = 8
    assert costs["Werewolf Den"] == 8
    # Best path to Goblin Market: Crypt Kitchen→Fog Alley→Moon Bridge→Goblin Market = 2+1+3=6
    assert costs["Goblin Market"] == 6
    # Best path to Vampire Tower: through Werewolf Den = 8+2 = 10
    assert costs["Vampire Tower"] == 10


def test_costs_unreachable_is_inf(disconnected_graph):
    costs = monster_delivery_costs(disconnected_graph, "A")
    assert costs["C"] == inf


def test_costs_invalid_start():
    with pytest.raises(ValueError):
        monster_delivery_costs(HAUNTED_CITY, "Nowhere")


def test_costs_all_nodes_present():
    costs = monster_delivery_costs(HAUNTED_CITY, "Crypt Kitchen")
    assert set(costs.keys()) == set(HAUNTED_CITY.keys())


def test_costs_small_graph(small_graph):
    costs = monster_delivery_costs(small_graph, "A")
    assert costs["A"] == 0
    assert costs["B"] == 1
    assert costs["C"] == 3   # A→B→C = 1+2, cheaper than A→C = 4


# ---------------------------------------------------------------------------
# shortest_monster_delivery
# ---------------------------------------------------------------------------

def test_shortest_start_equals_target():
    cost, path = shortest_monster_delivery(HAUNTED_CITY, "Crypt Kitchen", "Crypt Kitchen")
    assert cost == 0
    assert path == ["Crypt Kitchen"]


def test_shortest_known_path():
    cost, path = shortest_monster_delivery(
        HAUNTED_CITY, "Crypt Kitchen", "Vampire Tower"
    )
    assert cost == 10
    assert path[0] == "Crypt Kitchen"
    assert path[-1] == "Vampire Tower"


def test_shortest_path_is_valid_route():
    """Every consecutive pair in the returned path must be a real edge."""
    cost, path = shortest_monster_delivery(
        HAUNTED_CITY, "Crypt Kitchen", "Vampire Tower"
    )
    for i in range(len(path) - 1):
        assert path[i + 1] in HAUNTED_CITY[path[i]], (
            f"No edge from {path[i]} to {path[i+1]}"
        )


def test_shortest_missing_start():
    cost, path = shortest_monster_delivery(HAUNTED_CITY, "Nowhere", "Vampire Tower")
    assert cost == inf
    assert path == []


def test_shortest_missing_target():
    cost, path = shortest_monster_delivery(HAUNTED_CITY, "Crypt Kitchen", "Nowhere")
    assert cost == inf
    assert path == []


def test_shortest_unreachable_target(disconnected_graph):
    cost, path = shortest_monster_delivery(disconnected_graph, "A", "C")
    assert cost == inf
    assert path == []


def test_shortest_small_graph(small_graph):
    cost, path = shortest_monster_delivery(small_graph, "A", "C")
    assert cost == 3
    assert path == ["A", "B", "C"]


# ---------------------------------------------------------------------------
# best_next_monster_stop  (stretch)
# ---------------------------------------------------------------------------

def test_best_stop_picks_cheapest():
    result_target, result_cost = best_next_monster_stop(
        HAUNTED_CITY,
        "Crypt Kitchen",
        ["Goblin Market", "Vampire Tower"],
    )
    # Goblin Market costs 6, Vampire Tower costs 10
    assert result_target == "Goblin Market"
    assert result_cost == 6


def test_best_stop_ignores_unreachable(disconnected_graph):
    target, cost = best_next_monster_stop(disconnected_graph, "A", ["C"])
    assert target == ""
    assert cost == inf


def test_best_stop_tie_picks_first():
    # Build a graph where two targets have equal cost.
    graph = {
        "Start": {"X": 3, "Y": 3},
        "X": {},
        "Y": {},
    }
    target, cost = best_next_monster_stop(graph, "Start", ["X", "Y"])
    assert target == "X"   # X appears first in targets list
    assert cost == 3


def test_best_stop_no_targets():
    target, cost = best_next_monster_stop(HAUNTED_CITY, "Crypt Kitchen", [])
    assert target == ""
    assert cost == inf


def test_best_stop_invalid_start():
    # Invalid start not in graph → returns ("", inf) gracefully
    target, cost = best_next_monster_stop(HAUNTED_CITY, "Nowhere", ["Goblin Market"])
    assert target == ""
    assert cost == inf