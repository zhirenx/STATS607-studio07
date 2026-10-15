"""Specify the simulation design in one place."""


def make_scenarios():
    """Return {scenario_id: settings} for experiments A and B.

    IDs are unique, stable, filename-safe strings. Each settings dictionary
    has exactly experiment ('A'/'B'), n (int), p (int), rho (float), and
    error_distribution ('normal'/'laplace'). Assume 0 < p < n, 0 <= rho < 1.
    The study supplies all generation, fitting, evaluation, and replication.

    Keep n=200. For A, use rho=0 and both error laws over the SAME chosen
    p/n values. For B, use normal errors and p=100 and choose rho values.
    Choose the values yourselves; the handout grid is only an example.
    """
    # BEGIN TASK GRID
    raise NotImplementedError('Choose and construct your scenario dictionary.')
    # END TASK GRID
