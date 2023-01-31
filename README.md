# Elastic Optical Networks Routing Strategies
This project aims to compare different routing strategies for elastic optical networks in terms of deployed OEO devices (transponders for add/drop and regenerators) and free spectrum per link. The benchmarked algorithm is the routing, grooming, modulation level and spectrum assignment (RGMLSA) algorithm, which will be compared with diverse end-to-end aggregation strategies.

## Background
Elastic optical networks are based on optoelectronic interfaces that can dynamically tune their modulation schema and baud-rate depending on the capacity requirements of the services to route. In backbone optical networks, client traffic demands are set up along several periods and, in each period, a RGMLSA algorithm is used to determine the resources required to accommodate each demand.

## Methodologies
The different RGSA methods to be compared are:
1) MSE-MaxC (Most Spectral Efficient – Maximum Capacity): This method selects the OCh
format/path with highest spectral efficiency (SE), i.e., max{R(θ) / ∆f(θ)}, and break ties with the one
with maximum capacity, i.e. max{R(θ)}. 
2) MSE-MinS (Most Spectral Efficient – Minimum Spectrum): This method selects the OCh format/path with highest SE, i.e., max{R(θ) / ∆f(θ)}, and break ties with the one with minimum spectrum usage, i.e. min{∆f(θ)}.
3) JEC (Just Enough Capacity): Let r(d) denote the data rate of d and 𝑟(d) denote the cumulative data
rate of all traffic demands between this node pair. This method selects the OCh format/path with
best capacity fit, i.e. min{R(θ): R(θ) ≥ r(d) + 𝑟(d)} and break ties with the one with minimum
spectrum usage, i.e. min{∆f(θ)}. 

## Comparison and Results
WIP