# P Systems inference via Grammatical Evolution

## Abstract
P systems are a bio-inspired framework for defining parallel models of computation. Despite their relevance for both theoretical and application scenarios, the design and synthesis of P systems remain a tedious and demanding task. In this work, we try to address this problem by proposing an automated design methodology based on Grammatical Evolution (GE)—an evolutionary computation technique. We consider a situation where observations of the steps of a P system are available, and we rely on GE for automatically inferring its structure, i.e., its rules.

## Code
- P systems code based on [Psystem-GA](https://github.com/gpietrop/Psystem-GA).
- Grammatical evolution code based on [PonyGE](https://github.com/PonyGE/PonyGE2).

### Install
```
pip install -r requirements.txt
```

### Run an experiment
```
$ cd src
$ python psystems_experiments.py --parameters psystems.txt
```
This will automatically create a sequence of membrane configurations and a suitable grammar for evolving the generator ruleset.

Currently,
- n of rules = 2
- rule type = send_in
- id = 0

We will make them customizable.
