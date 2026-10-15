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
    
    scenarios = {}
    n = 200

    # Experiment A
    p_values = [10, 40, 80, 120, 160, 180]

    for error_dist in ["normal", "laplace"]:
        for p in p_values:
            scenario_id = f"A_{error_dist}_p{p:03d}"

            scenarios[scenario_id] = {
                "experiment": "A",
                "n": n,
                "p": p,
                "rho": 0.0,
                "error_distribution": error_dist,
            }

    # Experiment B
    rho_values = [0.0, 0.5, 0.8, 0.9, 0.95, 0.99]

    for rho in rho_values:
        scenario_id = f"B_rho{int(round(rho * 100)):02d}"

        scenarios[scenario_id] = {
            "experiment": "B",
            "n": n,
            "p": 100,
            "rho": rho,
            "error_distribution": "normal",
        }

    return scenarios

    # END TASK GRID
