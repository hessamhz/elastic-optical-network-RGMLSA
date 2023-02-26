import random

import pandas as pd


def generate_services(
    count: int,
    nodes: pd.DataFrame,
    min_traffic=None,
    possible_traffics=None,
) -> pd.DataFrame:
    # creating a new pd.DataFrame for services
    services = pd.DataFrame(columns=["src", "dst", "traffic"])
    services = services.astype(
        {"src": "string", "dst": "string", "traffic": "int"}
    )

    # list of possible traffics for a elastic network
    if possible_traffics is None:
        possible_traffics = [10, 40, 100]

    # populating the services
    for i in range(count):
        src, dst = nodes["node"].sample(n=2).unique()
        # not using pandas.append since it is deprecated
        # creating random rows for service demands
        new_row = pd.DataFrame(
            {
                "src": [src],
                "dst": [dst],
                "traffic": [random.choice(possible_traffics)],
            },
        )
        services = pd.concat([services, new_row], ignore_index=True)

    # Since for the initial service generation we need to satisfy
    # the need for having at least a minimum traffic.
    # this is not required for generation of extra services
    # when we are testing.
    done = False

    # Checking if it's the initial service generation or not
    if min_traffic is None:
        done = True
    # This is the initial service generation
    else:
        # Calculate outgoing and incoming traffic for each node
        outgoing_traffic = (
            services.groupby("src")["traffic"]
            .sum()
            .reset_index()
            .rename(columns={"src": "node", "traffic": "out_traffic"})
        )
        # print(outgoing_traffic)
        incoming_traffic = (
            services.groupby("dst")["traffic"]
            .sum()
            .reset_index()
            .rename(columns={"dst": "node", "traffic": "in_traffic"})
        )
        # print(incoming_traffic)

        # Calculate the sum of incoming and outgoing traffic for each node
        traffic_sum = pd.merge(
            outgoing_traffic, incoming_traffic, on="node", how="outer"
        )
        traffic_sum["traffic_sum"] = traffic_sum["out_traffic"].fillna(
            0
        ) + traffic_sum["in_traffic"].fillna(0)

        # Putting 0 in NaN
        traffic_sum.fillna(0, inplace=True)

        # Checking if there's a node that doesn't satisfy the traffic requirements
        if (traffic_sum["traffic_sum"] >= min_traffic).all():
            done = True

    return services, done
