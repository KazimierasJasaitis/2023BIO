from typing import List, Set

def set_cover(universe: Set[int], sets: List[Set[int]], selected_sets: List[int] = [], recursive_calls: int = 0) -> (List[int], int):
    """
    Implement the set cover algorithm in a recursive manner.

    :param universe: A set of all elements that need to be covered.
    :param sets: A list of sets where each set is a subset of the universe.
    :param selected_sets: A list to store the index of sets selected in the current recursion.
    :param recursive_calls: Counter for the number of recursive calls made.
    :return: A tuple containing the indices of the selected sets and the count of recursive calls.
    """

    recursive_calls += 1  # Increment the count of recursive calls

    # Base case: If universe is empty, return the selected sets and the count of recursive calls
    if not universe:
        return selected_sets, recursive_calls

    # Find the set that covers the most uncovered elements
    max_set = None
    max_elements_covered = 0
    for i, s in enumerate(sets):
        covered = len(universe.intersection(s))
        if covered > max_elements_covered:
            max_elements_covered = covered
            max_set = i

    if max_set is None:
        return None, recursive_calls  # No solution exists

    # Update the universe and selected sets
    selected_sets = selected_sets + [max_set]
    new_universe = universe - sets[max_set]

    # Recursively solve for the new universe
    return set_cover(new_universe, sets, selected_sets, recursive_calls)

# Example usage
universe = {1, 2, 3, 4, 5}
sets = [{1, 2, 3}, {2, 4}, {3, 4}, {4, 5}]
solution, recursive_calls = set_cover(universe, sets)

print(solution, recursive_calls)
