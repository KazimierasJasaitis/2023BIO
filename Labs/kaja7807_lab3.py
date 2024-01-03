import sys
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate
from prettytable import PrettyTable

def read_data(filename):
    with open(filename, 'r') as file:
        return [['B']+list(line.strip()) for line in file.readlines()]

def calculate_hmm_counts(state_matrix):
    n = len(state_matrix[0])
    MM, MD, MI, IM, ID, II, DM, DD, DI = [0]*n, [0]*n, [0]*n, [0]*n, [0]*n, [0]*n, [0]*n, [0]*n, [0]*n
    
    aa = ['A','C','G','T']
    match_emissions = {base: [0]*n for base in aa}
    insert_emissions = {base: [0]*n for base in aa}

    next_insertion = len([seq[1] for seq in state_matrix if seq[1] == '-' ]) >= len(state_matrix) / 2
    for seq in state_matrix:
        if next_insertion:
            next
        else:
            if seq[1] in aa:
                MM[0] += 1
            else:
                MD[0] += 1

    i=1
    
    while i<n-1 :
        insertion = len([seq[i] for seq in state_matrix if seq[i] == '-' ]) >= len(state_matrix) / 2
        next_insertion = len([seq[i+1] for seq in state_matrix if seq[i+1] == '-' ]) >= len(state_matrix) / 2
        deletion_sum = len([seq[i] for seq in state_matrix if seq[i] == '-' ])
        insertion_length = 1
        if insertion:
            prior_states = [state_matrix[j][i-1] for j in range(len(state_matrix))]
            while insertion:
                deletion_num = len([seq[i+1] for seq in state_matrix if seq[i+1] == '-' ])
                deletion_sum += deletion_num 
                insertion_length += 1
                
                next_insertion = deletion_sum >= ((len(state_matrix)*insertion_length) / 2) 
                for j in range(len(state_matrix)):

                    if state_matrix[j][i] in aa:
                        insert_emissions[state_matrix[j][i]][i-1] += 1
                        if prior_states[j] in aa:
                            MI[i-1] += 1
                            prior_states[j] = 'M'
                        if prior_states[j] == '-':
                            DI[i-1] += 1
                            prior_states[j] = 'D'
                        
                            
                    if next_insertion:
                        if state_matrix[j][i] in aa:
                            if state_matrix[j][i+1] in aa:
                                II[i-1] += 1
                    else:
                        if state_matrix[j][i+1] in aa:
                            if prior_states[j] in aa:
                                MM[i-1] += 1
                                prior_states[j] = 'M'
                            elif prior_states[j] == '-':
                                DM[i-1] += 1
                                prior_states[j] = 'D'
                            else:
                                IM[i-1] += 1
                        else:
                            if prior_states[j] in aa:
                                MD[i-1] += 1
                                prior_states[j] = 'M'
                            elif prior_states[j] == '-':
                                DD[i-1] += 1
                                prior_states[j] = 'D'
                            else:
                                ID[i-1] += 1

                    state_matrix[j].pop(i)
                n-=1
                insertion = next_insertion
            i-=1
        else:
            for seq in state_matrix:
                if seq[i] in aa:
                    match_emissions[seq[i]][i] += 1
                    if next_insertion:
                        next
                    else:
                        if seq[i+1] in aa:
                            MM[i] += 1
                        else:
                            MD[i] += 1
                else:
                    if next_insertion:
                        next
                    else:
                        if seq[i+1] in aa:
                            DM[i] += 1
                        else:
                            DD[i] += 1

        i+=1

    for seq in state_matrix:
        if seq[n-1] in aa:
            match_emissions[seq[i]][i] += 1
            MM[n-1] += 1
        else:
            DM[n-1] += 1

    MM, MD, MI, IM, ID, II, DM, DD, DI = MM[:n], MD[:n], MI[:n], IM[:n], ID[:n], II[:n], DM[:n], DD[:n], DI[:n]
    match_emissions = {base: emissions[:n] for base, emissions in match_emissions.items()}
    insert_emissions = {base: emissions[:n] for base, emissions in insert_emissions.items()}

    state_transitions = MM, MD, MI, IM, ID, II, DM, DD, DI
    return match_emissions, insert_emissions, state_transitions






def print_data(match_emissions, insert_emissions, state_transitions):
    MM, MD, MI, IM, ID, II, DM, DD, DI = state_transitions

    table = PrettyTable()
    table.field_names = ["name", "key", "counts"]
    
    table.add_row(["Match Emissions", "", ""])
    for nucleotide, counts in match_emissions.items():
        table.add_row(["", nucleotide, counts])

    table.add_row(["Insert Emissions", "", ""])
    for nucleotide, counts in insert_emissions.items():
        table.add_row(["", nucleotide, counts])
    
    table.add_row(["State Transitions", "", ""])
    transition_labels = ['MM', 'MD', 'MI', 'IM', 'ID', 'II', 'DM', 'DD', 'DI']
    for label, count in zip(transition_labels, state_transitions):
        table.add_row(["", label, count])

    print(table)


states = read_data('data02.txt')
match_emissions, insert_emissions, state_transitions = calculate_hmm_counts(states)

print_data(match_emissions, insert_emissions, state_transitions)
