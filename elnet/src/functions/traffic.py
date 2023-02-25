import random

import pandas as pd


def generate_sublambda_traffic(lower_bound: int, upper_bound: int) -> int:
    return random.randint(lower_bound, upper_bound)


def generate_services(
    count: int, nodes: pd.DataFrame, lower_bound: int, upper_bound: int
) -> pd.DataFrame:
    services = pd.DataFrame(columns=["src", "dst", "traffic"])
    services = services.astype(
        {"src": "string", "dst": "string", "traffic": "int"}
    )
    for i in range(count):
        src, dst = nodes["node"].sample(n=2).unique()
        # not using pandas.append since it is deprecated
        new_row = pd.DataFrame(
            {
                "src": [src],
                "dst": [dst],
                "traffic": [
                    generate_sublambda_traffic(lower_bound, upper_bound)
                ],
            },
        )
        services = pd.concat([services, new_row], ignore_index=True)
    return services
