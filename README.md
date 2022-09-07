# Inferring P Systems From Their Computing Steps: An Evolutionary Approach

Python implementation for paper "Inferring P Systems From Their Computing Steps: An Evolutionary Approach": Alberto Leporatia, Luca Manzoni, Giancarlo Mauria, Gloria Pietropolli, Claudio Zandrona, 2021.

## Abstract
Inferring the structure and operation of a computing model, given some observations of its behavior, is in general a desirable but daunting task. In this paper we try to solve a constrained version of this problem. Given a P system Π with active membranes and using cooperative rewriting, communication, and division
rules, let C be a collection of pairs (Ci, Ci+1) of consecutive configurations of Π, for 0 ≤ i < n. We feed this collection as input to a (µ+λ) evolutionary algorithm that evolves a population of (initially random) P systems, each with its own rules, with the aim of obtaining an individual that approximates Π as well as
possible. We discuss the results obtained on four different benchmark problems, designed to test the ability to infer cooperative rewriting, communication, and
membrane division rules. We will also provide a description of how fitness results are influenced by different setting of the hyperparameters of the evolutionary
algorithm. The results show that the proposed approach is able to find correct solutions for small problems, and it is a promising research direction for the
automatic synthesis of P systems.

## Instructions

Code runs with python 3.8.5 on Ubuntu 20.04, after installing the following requirements:  

```bash
pip install -r requirements.txt 
```

To run the code, enter the following command:

```bash
python3 experiments.py --problem --size --number_run==1 --conf_file==conf.json --prefix=='out' 
```
where the inputs arguments stands for: 
* `--problem` is the benchmark considered (that can be: _send-in_, _send-out_, _assignment_ and _tm_)
* `--size` is the size of the problem considered (in this paper have been considered size: 2, 3, 4 and 5)
* `--size` is the number of run performed for the experiment considered (in this paper 30 run has been performed for each experiment)
* `--conf_file` is the .json configuration file containing the values of the hyperparameters:
  * `max_lhs`: maximum left-hand side dimension 
  * `max_rhs`: maximum right-hand side dimension
  * `min_ruleset_size`: miminum dimension for the ruleset
  * `max_ruleset_size`: maximum dimension for the ruleset
  * `max_mutation`: maximum number of mutation allowed
  * `mu` : population size
  * `lmbd`: number of offsprings
  * `generations`: number of generations
  
* `--prefix` is the name of the .csv file where results are saved 

The codes that reproduce the plots of the paper are contained in the folder `plot`.
To get __Figure 2-5__ it is sufficient to run:
```bash
python3 Fitness.py
```
For example, for the __send-in__ problem, the results obtained with different hyperparameters setting are plotted as: 

<img src="/img/send-in-2-fitness-subplot_comparison.png" width="250" height="200"> <img src="/img/send-in-3-fitness-subplot_comparison.png" width="250" height="200">
<img src="/img/send-in-4-fitness-subplot_comparison.png" width="250" height="200"> <img src="/img/send-in-5-fitness-subplot_comparison.png" width="250" height="200">

To get __Figure 1__ is sufficent to run: 
```bash
python3 Fitness.py --problem --mu --max_ruleset_size
```
For example, for mu=1 and m=20 we obtain:

<img src="/img/send-in-bp.png" width="250" height="200"> <img src="/img/send-out-bp.png" width="250" height="200">
<img src="/img/assignment-bp.png" width="250" height="200"> <img src="/img/tm-bp.png" width="250" height="200">
