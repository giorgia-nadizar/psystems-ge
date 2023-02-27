# P Systems inference via Grammatical Evolution

## Abstract
P systems are a bio-inspired framework for defining parallel models of computation.
Despite their relevance for both theoretical and application scenarios, the design of P systems remains a tedious and demanding task, requiring considerable time and expertise.
In this work, we try to address this problem by proposing an automated methodology based on Grammatical Evolution (GE)—an evolutionary computation technique—which does not require any domain knowledge.
We consider a setting where observations of successive configurations of a P system are available, and we rely on GE for automatically inferring the P system, i.e., its ruleset.
We assess the practicability of the proposed method on six problems of various difficulties and evaluate its behavior in terms of inference capability and time consumption.
Experimental results confirm our approach is a viable strategy for small problem sizes, where it achieves perfect inference in a few seconds without any human intervention.
Moreover, we also obtain promising results for larger problem sizes in a human-aided context, paving the way for fully- or partially-automated design of P systems.

## Code
- P systems code based on [Psystem-GA](https://github.com/gpietrop/Psystem-GA).
- Grammatical evolution code based on [PonyGE](https://github.com/PonyGE/PonyGE2).

### Install
```
pip install -r requirements.txt
```

### Run an experiment
```
cd src
python psystems_experiments.py --parameters psystems.txt
```
This will automatically create a sequence of membrane configurations and a suitable grammar for evolving the ruleset.
The file psystems.txt (located in the parameters folder) can be customized to edit parameters, e.g., alter number of generations or population size.
The default values for problem size, problem, and dataset generation seed, are 2, send_in, and 0, respectively.
It is possible to pass additional parameters to the script to change them, as for example:

```
cd src
python psystems_experiments.py --parameters psystems.txt --random_seed 1 --problem_size 3 --problem send_out --dataset_seed 0
```

We also provide some "simplified" grammars, relative to the send-in, send-out, and variable assigment problems.
To use them, it is necessary to add the following parameter:
```
--setting easy
```

Moreover, only for the elementary operations it is possibly to specify the parameter `p`, which is otherwise set to 
$\lceil \frac{n}{2} \rceil$ for addition and multiplication, and to $n$ for division.
```
--p_size 2
```

### Outcomes
Each experiment generates some files:
- the grammar used (all follow the same template, but differ in the objects and membranes) $\to$ grammars/psystems folder
- the training set $\to$ datasets/Psystems folder
- the results of the experiment $\to$ results/exp_name/machine_name_timestamp folder
  - stats.tsv reports the progress of evolution
  - parameters.txt summarized the employed parameters
  - best.txt reports the best individual
  - best_fitness.pdf displays the evolution of the fitness of the best individual

## Other files
The core lies in the src/fitness/psystems/IdentificationProblem.py where we define the parsing of rules from the grammar generated strings and the distance between membranes (i.e., the fitness function).
