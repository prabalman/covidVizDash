
import csv

from collections import defaultdict
from math import log10, log, isnan, isinf
from statistics import mean, stdev, NormalDist, variance, median

import pprint



def read_data(filename, n_zfill: int=None):

    data = dict()

    with open(filename, 'r') as file:

        f = csv.reader(file)

        header = next(f)            # just skip the header

        for row in f:

            fip, values = row[0], row[1:]
            fip = fip.zfill(n_zfill) if isinstance(n_zfill, int) else fip

            # if as_int:
                # data[fip] = tuple(int(n) if n != '' else int(0.0) for n in values)
            # else:
            data[fip] = tuple(float(n) if n != '' else float(0.0) for n in values)

            # if normalize:
            #     Σ = sum(data[fip])
            #     data[fip] = tuple(map(lambda n: n / Σ, data[fip]))

        return header, data

# -----------------------------------------------

def calc_surprise(data, models=['uniform', 'minimum', 'maximum']):

    MODELS = {'uniform', 'base-rate', 'minimum', 'maximum', 'gaussian', 'binomial', 'demoive', 'median', 'boom', 'bust'}

    for model in models:
        assert model in MODELS, f'{model} not recognized'

    model_history = {model: [] for model in models}

    n = len(models)

    surprise = {}
    
    for county in data.keys():
        surprise[county] = [0.0 for _ in range(len(data[county]))]

    diffs = {model: 0.0 for model in models}
    pMs   = {model: 1./n for model in models}
    pDMs  = {model: 0.0 for model in models}
    pMDs  = {model: 0.0 for model in models}

    # n_months = len(data['Alabama'])
    n_months = len(tuple(data.values())[0])
    n_events = len(tuple(data.values())[0])

    # these are the annual amounts over all the counties
    surprise = {state: [0.0 for _ in range(len(values))] for state, values in data.items()}
    
    for i in range(n_months):

        sum_diffs = {model: 0.0 for model in models}

        avg   = mean((data[state][i] for state in data.keys()))
        total =  sum([data[state][i] for state in data.keys()])
        min_  = min([data[state][i] for state in data.keys()])
        max_  = max([data[state][i] for state in data.keys()])

        if total == 0.0:
            # print('ZERO! ')
            total = 0.00000001

        for state in data.keys():

            for model in models:

                if model == 'base-rate':
                    #            p(ohio | year)         -    p(all-years)
                    diffs[model] = (data[state][i] / total) - (avg / total)
                elif model == 'uniform':
                    diffs[model] = (data[state][i] / total) - ((1.0 / n_events) * total)
                elif model == 'maximum': 
                    # diffs[model] = (data[state][i] / total) - (data[state][boom_year] / total)        # from the example
                    diffs[model] = (data[state][i] / total) - (max_ / total)
                elif model == 'minimum':
                    # diffs[model] = (data[state][i] / total) - (data[state][bust_year] / total)          # from the example
                    diffs[model] = (data[state][i] / total) - (min_ / total)
                #this is for the example from the paper's website --------------
                elif model == 'boom':
                    diffs[model] = (data[state][i] / total) - (data[state][-1] / total)
                elif model == 'bust':
                    diffs[model] = (data[state][i] / total) - (data[state][0] / total)

                diffs[model] = 0.0 if isnan(diffs[model]) or isinf(diffs[model]) else diffs[model]
                pDMs[model] = 1.0 - abs(diffs[model]) 

            # estimate p(M|D)
            # for model in models:
                pMDs[model] = pMs[model] * pDMs[model]
                pMDs[model] = 0.0000001 if pMDs[model] < 0.0 else pMDs[model]   # why is the necessary!? why does it work?
                pMs[model]  = 0.0000001 if pMs[model] < 0.0 else pMs[model]
                # if pMDs[model] < 0.0: print('Whow')
                
                # not sure how this is happening...
                if not (0.0 <= pMDs[model] <= 1.0): 
                     pMDs[model] = 0.0

                if not (0.0 <= pMs[model] <= 1.0): 
                     pMDs[model] = 0.0
            
            # estimate KL divergence
            kl = 0.0
            vote_sum = 0.0

            for model in models:
                div = pMDs[model] / (pMs[model] if pMs[model] != 0.0 else 0.0000001)
                kl += pMDs[model] * (log(div if div != 0.0 else 0.0000001) / log(2.0))
                vote_sum += diffs[model] * pMs[model]
                sum_diffs[model] += abs(diffs[model])
                
            kl = 0.0 if isnan(kl) or isinf(kl) else kl

            surprise[state][i] = abs(kl) if vote_sum >= 0 else -1.0 * abs(kl)

            # print(state, ' surprise: ', surprise[state][i], ' pM: ', pMs['base-rate']) #, ' pMD:', pMDs[0])

        for model in models:
            pDMs[model] = 1.0 - (0.5 * sum_diffs[model])
            pMDs[model] = pMs[model] * pDMs[model]
            pMs[model] = pMDs[model]

            # not sure how this is happening...
            if not (0.0 <= pMDs[model] <= 1.0): 
                    pMDs[model] = 0.0

            if not (0.0 <= pMs[model] <= 1.0): 
                    pMs[model] = 0.0
        
        t = abs(sum(pMs.values()))                          # a weird numerical issue around here…
        for model in models:
            pMs[model] /= abs(t)   #pMs[model] / t                       
            
        # print('t: ', t)
        
        for model in models:
            model_history[model].append(pMs[model])

    return {'history': model_history, 'surprise': surprise, 'pM': pMs}

# =============================================================================

# dates, data = read_data('/home/aaron/Desktop/BayesianSurprise/unemployment/data.csv', None)
# results = calc_surprise(data, ['boom', 'bust', 'base-rate'])


# print(results['surprise']['Puerto Rico'])
# print(results['surprise']['Alabama'])
# print(results['history']['base-rate'])
# print(results['pM']['base-rate'])

# print(results['surprise']['Puerto Rico'])
# print('-' * 25)
# print(results['history'])

# print(surprise['Washington'])
# print(pm)


# f = '/home/aaron/Desktop/BayesianSurprise/data/nyt-ma_data-ratio_dc.csv'

# dates, data = read_data(f)
# results = calc_surprise(data, models=['uniform', 'base-rate'])

# print(results['surprise'])