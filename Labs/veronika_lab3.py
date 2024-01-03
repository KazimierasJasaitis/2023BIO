import sys
import matplotlib.pyplot as plt
import numpy as np

def read_data(filename):
    with open(filename, 'r') as file:
        return [['B']+list(line.strip()) for line in file.readlines()]

def calculate_hmm_counts(state_matrix):
    n = len(state_matrix[0])
    state_transitions = {
        'MM': [], 'MD': [], 'MI': [], 'IM': [], 'ID': [],
        'II': [], 'DM': [], 'DD': [], 'DI': []
    }

    aa = ['A', 'C', 'G', 'T']
    match_emissions = {base: [0] * n for base in aa}
    insert_emissions = {base: [0] * n for base in aa}

    # First column
    for seq in state_matrix:
        if seq[1] in aa:
            state_transitions['MM'].append(0) if seq[1] in aa else state_transitions['MD'].append(0)

    i = 1
    while i < n - 1:
        insertion = len([seq[i] for seq in state_matrix if seq[i] == '-']) > len(state_matrix) / 2
        next_insertion = len([seq[i + 1] for seq in state_matrix if seq[i + 1] == '-']) > len(state_matrix) / 2
        
        if insertion:
            prior_states = [state_matrix[j][i - 1] for j in range(len(state_matrix))]
            while insertion:
                next_insertion = len([seq[i + 1] for seq in state_matrix if seq[i + 1] == '-']) > len(state_matrix) / 2
                for j in range(len(state_matrix)):
                    if state_matrix[j][i] in aa:
                        insert_emissions[state_matrix[j][i]][i - 1] += 1
                        if prior_states[j] in aa:
                            state_transitions['MI'][i - 1].append(i - 1)
                            prior_states[j] = 'M'
                        elif prior_states[j] == '-':
                            state_transitions['DI'][i - 1].append(i - 1)
                            prior_states[j] = 'D'

                    if next_insertion:
                        if state_matrix[j][i] in aa:
                            state_transitions['II'][i - 1].append(i - 1) if state_matrix[j][i + 1] in aa else None
                    else:
                        if state_matrix[j][i + 1] in aa:
                            if prior_states[j] in aa:
                                state_transitions['MM'][i - 1].append(i - 1)
                                prior_states[j] = 'M'
                            elif prior_states[j] == '-':
                                state_transitions['DM'][i - 1].append(i - 1)
                                prior_states[j] = 'D'
                            else:
                                state_transitions['IM'][i - 1].append(i - 1)
                        else:
                            if prior_states[j] in aa:
                                state_transitions['MD'][i - 1].append(i - 1)
                                prior_states[j] = 'M'
                            elif prior_states[j] == '-':
                                state_transitions['DD'][i - 1].append(i - 1)
                                prior_states[j] = 'D'
                            else:
                                state_transitions['ID'][i - 1].append(i - 1)

                    state_matrix[j].pop(i)
                n -= 1
                insertion = next_insertion
            i -= 1
        else:
            for seq in state_matrix:
                if seq[i] in aa:
                    match_emissions[seq[i]][i] += 1
                    if not next_insertion:
                        state_transitions['MM'].append(i) if seq[i + 1] in aa else state_transitions['MD'].append(i)
                else:
                    if not next_insertion:
                        state_transitions['DM'].append(i) if seq[i + 1] in aa else state_transitions['DD'].append(i)
        i += 1

    # Last column
    for seq in state_matrix:
        if seq[n - 1] in aa:
            state_transitions['MM'].append(n - 1) if seq[n - 1] in aa else state_transitions['MD'].append(n - 1)

    # Return match_emissions, insert_emissions, state_transitions
    return match_emissions, insert_emissions, state_transitions




def print_data(match_emissions, insert_emissions, state_transitions):
    # Accessing the transition counts directly from the dictionary
    MM = state_transitions['MM']
    MD = state_transitions['MD']
    MI = state_transitions['MI']
    IM = state_transitions['IM']
    ID = state_transitions['ID']
    II = state_transitions['II']
    DM = state_transitions['DM']
    DD = state_transitions['DD']
    DI = state_transitions['DI']

    print('---------------------------------')
    print('Match Emissions:')
    for nucleotide, counts in match_emissions.items():
        print(f'{nucleotide}: {counts}')
    print('---------------------------------')

    print('Insert Emissions:')
    for nucleotide, counts in insert_emissions.items():
        print(f'{nucleotide}: {counts}')
    print('---------------------------------')

    # Printing the indices where each transition occurs
    print('MM transitions at indices:', MM)
    print('MD transitions at indices:', MD)
    print('MI transitions at indices:', MI)
    print('---------------------------------')
    print('IM transitions at indices:', IM)
    print('ID transitions at indices:', ID)
    print('II transitions at indices:', II)
    print('---------------------------------')
    print('DM transitions at indices:', DM)
    print('DD transitions at indices:', DD)
    print('DI transitions at indices:', DI)
    print('---------------------------------')


states = read_data('data02.txt')
match_emissions, insert_emissions, state_transitions = calculate_hmm_counts(states)

print_data(match_emissions, insert_emissions, state_transitions)
