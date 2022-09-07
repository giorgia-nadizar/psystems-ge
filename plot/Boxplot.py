import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

import os
import csv
import sys


max_lhs = (1, 2, 3)
max_rhs = (1, 2, 3)

def mean_(path):
        rows = []
        if os.path.exists(path):
            with open(path, 'r') as file:
                csvreader = csv.reader(file)
                for row in csvreader:
                    rows.append(row)
            if len(rows[-1])!=30:
                fitness = rows[-2]
            else:
                fitness = rows[-1]
            fitness = [float(el) for el in fitness if el!=' ']
        else:
            fitness = []
        if fitness != []:
            mean = np.mean(fitness)
        
        return (fitness, mean)


if __name__ == '__main__':
    mu = sys.argv[2]
    max_ruleset_size = sys.argv[3]
    max_mutation = max_ruleset_size

    problem = sys.argv[1]

    directory = "results/" + str(mu) + "/" + str(max_ruleset_size) + "/" + str(max_mutation) + "/"

    directory1 = directory + str(max_lhs[0]) + "/" + str(max_rhs[0]) + "/"
    directory2 = directory + str(max_lhs[1]) + "/" + str(max_rhs[1]) + "/"
    directory3 = directory + str(max_lhs[2]) + "/" + str(max_rhs[2]) + "/"

    if not os.path.exists(directory + 'plot/'):
        os.mkdir(directory + 'plot/')

    res2_1 = directory1 + problem + "-2-fitness.csv"
    res2_2 = directory2 + problem + "-2-fitness.csv"
    res2_3 = directory3 + problem + "-2-fitness.csv"

    res3_1 = directory1 + problem + "-3-fitness.csv"
    res3_2 = directory2 + problem + "-3-fitness.csv"
    res3_3 = directory3 + problem + "-3-fitness.csv"

    res4_1 = directory1 + problem + "-4-fitness.csv"
    res4_2 = directory2 + problem + "-4-fitness.csv"
    res4_3 = directory3 + problem + "-4-fitness.csv"

    res5_1 = directory1 + problem + "-5-fitness.csv"
    res5_2 = directory2 + problem + "-5-fitness.csv"
    res5_3 = directory3 + problem + "-5-fitness.csv"

    fitness2_1, mean2_1 = mean_(res2_1)
    fitness2_2, mean2_2 = mean_(res2_2)
    fitness2_3, mean2_3 = mean_(res2_3)

    fitness3_1, mean3_1 = mean_(res3_1)
    fitness3_2, mean3_2 = mean_(res3_2)
    fitness3_3, mean3_3 = mean_(res3_3)

    fitness4_1, mean4_1 = mean_(res4_1)
    fitness4_2, mean4_2 = mean_(res4_2)
    fitness4_3, mean4_3 = mean_(res4_3)

    fitness5_1, mean5_1 = mean_(res5_1)
    fitness5_2, mean5_2 = mean_(res5_2)
    fitness5_3, mean5_3 = mean_(res5_3)


    fitness2 = np.array([fitness2_1, fitness2_2, fitness2_3])
    fitness3 = np.array([fitness3_1, fitness3_2, fitness3_3])
    fitness4 = np.array([fitness4_1, fitness4_2, fitness4_3])
    fitness5 = np.array([fitness5_1, fitness5_2, fitness5_3])

    df2 = pd.DataFrame(fitness2.T, columns=list(range(1,4))).assign(Trial=1)
    df3 = pd.DataFrame(fitness3.T, columns=list(range(1,4))).assign(Trial=2)
    df4 = pd.DataFrame(fitness4.T, columns=list(range(1,4))).assign(Trial=3)
    df5 = pd.DataFrame(fitness5.T, columns=list(range(1,4))).assign(Trial=4)

    cdf = pd.concat([df2, df3, df4, df5])                                
    mdf = pd.melt(cdf, id_vars=['Trial'], var_name=["LHS-RHS size"])     
    
    fig = plt.figure(figsize =(7, 6))
    sns.set_theme(style="whitegrid")

    bplot = sns.boxplot(y="Trial", 
                x="value", 
                hue="LHS-RHS size", 
                data = mdf, 
                orient = "h",
                linewidth = 2,
                palette=["w", "silver", "gray"])

    bplot.set_xlabel("")
    bplot.set_ylabel("")

    bplot.set_yticklabels(["2", "3", "4", "5"])
    plt.savefig(directory + 'plot/' + problem + '-bp.png')
    plt.show()
    plt.close()
