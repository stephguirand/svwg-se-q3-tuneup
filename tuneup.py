#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tuneup assignment

Use the timeit and cProfile libraries to find bad code.
"""

__author__ = """
stephguirand
Help from demo, lessons and activities, youtube videos in canvas and
own search on youtube,
stack overflow, Tutors, Facilitators and talking about assignment
in study group.
"""

import cProfile as c
import pstats
# import functools
import timeit
from collections import Counter

"""A cProfile decorator function that can be used to
    measure performance.
    """
# Be sure to review the lesson material on decorators.
# You need to understand how they are constructed and used.


def profile(func):
    # raise NotImplementedError("Complete this decorator function")

    # nesting a function to perform more functions....

    def inner(*args, **kwargs):
        pr = c.Profile()
        pr.enable()
        result = func(*args, **kwargs)
        pr.disable()
        sort_by = 'cumulative'
        ps = pstats.Stats(pr).sort_stats(sort_by)
        ps.print_stats()
        return result
    return inner


def read_movies(src):
    """Returns a list of movie titles."""
    print(f'Reading file: {src}')
    with open(src, 'r') as f:
        return f.read().splitlines()


def is_duplicate(title, movies):
    """Returns True if title is within movies list."""
    for movie in movies:
        if movie.lower() == title.lower():
            return True
    if title in movies:
        return True
    return False


@profile
def find_duplicate_movies(src):
    """Returns a list of duplicate movies from a src list."""
    # Not optimized
    movies = read_movies(src)
    duplicates = []
    while movies:
        movie = movies.pop()
        if is_duplicate(movie, movies):
            duplicates.append(movie)
    return duplicates

#
# Students: write a better version of find_duplicate_movies
#


def optimized_find_duplicate_movies(src):
    movies = read_movies(src)
    counter_for_movies = Counter(movies)
    duplicates = [movie for movie,
                  val in counter_for_movies.items() if val > 1]
    return duplicates


def timeit_helper(func_name, func_param):
    """Part A: Obtain some profiling measurements using timeit"""
    assert isinstance(func_name, str)
    # f"find_duplicate_movies('movies.txt')"
    stmt = f"{func_name}('{func_param}')"
    setup = f'from {__name__} import {func_name}'
    t = timeit.Timer(stmt, setup)
    runs_per_repeat = 3
    num_repeats = 5
    result = t.repeat(repeat=num_repeats, number=runs_per_repeat)
    time_cost = min(result) / runs_per_repeat
    print(
        f"func={func_name}  num_repeats={num_repeats}\
             runs_per_repeat={runs_per_repeat} time_cost={time_cost:.3f} sec"
    )
    return t


def main():
    """Computes a list of duplicate movie entries."""
    # Students should not run two profiling functions at the same time,
    # e.g. they should not be running 'timeit' on a function that is
    # already decorated with @profile

    filename = 'movies.txt'

    print("--- Before optimization ---")
    result = find_duplicate_movies(filename)
    print(f'Found {len(result)} duplicate movies:')
    print('\n'.join(result))

    print("\n--- Timeit results, before optimization ---")
    timeit_helper('find_duplicate_movies', filename)

    print("\n--- Timeit results, after optimization ---")
    timeit_helper('optimized_find_duplicate_movies', filename)

    print("\n--- cProfile results, before optimization ---")
    profile(find_duplicate_movies)(filename)

    print("\n--- cProfile results, after optimization ---")
    profile(optimized_find_duplicate_movies)(filename)


if __name__ == '__main__':
    main()
    print("Completed.")
