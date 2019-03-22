# FencingTournament.py
# Written by Rory Laster on 18 March, 2019.
#
#
# The program structure is shown in the following.
#
# main
#   |
#   |--read_input
#   |    |
#   |     --map_to_integer
#   |
#   |--define_groups
#   |    |
#   |    |--count
#   |    |
#   |    |--define_num_groups
#   |    |
#   |    |--distribute
#   |    |     |
#   |    |      --map_to_rank
#   |    |
#   |     --resolve_conflicts
#   |         |
#   |          --map_to_integer
#   |
#    --write_output
#   
#      handle_argument_error
#   
#      handle_file_error
#
#
# Known issues:
#
#   (1) the algorithm in resolve_conflicts is slow (but hopefully readable) and
#   (2) the program doesn't throw and error if n isn't between 12 and 100.

import sys
import csv
from math import floor, ceil

#

def main():

    try:

        filename = sys.argv[1] # Throws IndexError.

        # Process the input.

        participants = read_input(filename) # Throws OSError.

        # Define the tournament's groups.

        groups = define_groups(participants)

        # Write the groups to standard output.

        write_output(groups)
    
    except IndexError:
        handle_argument_error()

    except OSError:        
        handle_file_error()

#

def read_input(filename):

    try:

        participants = {}

        with open(filename) as file:

            reader = csv.reader(file, delimiter = ',')

            for row in reader:

                if (len(row) == 4): # The participant's data is valid.

                    # Store the participants' data.

                    last_name = row[0].strip().upper()
                    first_name = row[1].strip()
                    club = row[2].strip().upper()
                    rank_letter = row[3].strip()[0].upper()
                    rank_number = row[3].strip()[1:]
                    rank = map_to_integer(row[3].strip().upper())

                    # Put the participants into the dictionary with their ranks
                    # as the keys. The keys function is O(1) and returns a set;
                    # the in function for sets is also O(1).
                    
                    if rank in participants.keys(): # Append the participant.
                        
                        participants[rank].append([
                            first_name,
                            last_name,
                            club,
                            rank_letter,
                            rank_number
                        ])

                    else: # Create an array with one element: the participant.
                        
                        participants[rank] = [[
                            first_name,
                            last_name,
                            club,
                            rank_letter,
                            rank_number
                        ]]

                # else: Ignore the participant's bad data.

            sorted_participants = []

            # Sort the ranks of the participants. The sorted function uses
            # Timsort, an O(nlogn) algorithm.
            
            for key in sorted(participants.keys(), reverse = True):
                for i in range(len(participants[key])):
                    sorted_participants.append(participants[key][i])

    except OSError:
        raise OSError

    return sorted_participants

#

def map_to_integer(rank):

    int_value_of = {
        'U': 0,
        'E': 100,
        'D': 200,
        'C': 300,
        'B': 400,
        'A': 500
    }

    rank_letter = rank[0]
    rank_number = rank[1:]

    if (rank_number == ''): # Case 'U'.
        rank_number = 0

    else: # Case not 'U'.  
        rank_number = int(rank_number)

    return int_value_of[rank_letter] + rank_number

#

def map_to_rank(integer):

    letter_value_of = {
        0: 'U',
        1: 'E',
        2: 'D',
        3: 'C',
        4: 'B',
        5: 'A'
    }

    rank_letter = letter_value_of[floor(integer / 100)]

    if (integer % 100 == 0): # Case 'U'.
        rank_number = ''

    else: # Case not 'U'.
        rank_number = str(integer % 100)

    return rank_letter + rank_number

#

def define_groups(participants):

    # These two dictionaries are for fast mapping between the groups and
    # participants arrays.

    map_to_groups = {}
    map_to_participants = {}

    # Count and print participants.

    clubs = count_and_print(participants)

    # Define the number of groups.

    num_groups = define_num_groups(participants)

    # Distribute participants into groups.

    groups = distribute(
        participants,
        num_groups,
        clubs,
        map_to_groups,
        map_to_participants
    )

    # Resolve club conflicts.

    resolve_conflicts(
        participants,
        groups,
        clubs,
        map_to_groups,
        map_to_participants
    )

    return groups

#

def count_and_print(participants):

    clubs = {}

    print ('Competitor List')

    for i in range(len(participants)):

        # Store participant's data.

        first_name = participants[i][0]
        last_name = participants[i][1]
        club = participants[i][2]
        rank_letter = participants[i][3]
        rank_number = participants[i][4]

        # Add club to dictionary.

        if (club != ''):
            if club not in clubs.keys():
                clubs[club] = []

        # Print participant to output.

        print (
            f'{first_name:21}' +
            f'{last_name:24}' +
            f'{club:24}' +
            f'{rank_letter:8}' +
            f'{rank_number:2}'
        )

    print ('')

    return clubs

#

def define_num_groups(participants):

    num_participants = len(participants)

    # It's possible to group the participants into groups of 6 and 7 if and only if
    #
    #   num_participants (mod 6) <= floor(num_participants / 6).
    #
    # Since this the most desirable case, we check this condition first.

    if ((num_participants % 6) <= (num_participants / 6)):

        num_groups = floor(num_participants / 6)

        # Although we don't implement it, more can be said here: for
        # n = num_participants >= 42, there are two ways to make groups of 6
        # and 7. They are
        #
        #   (1) n (mod 6) groups of 7 and floor(n / 6) - n (mod 6) groups of 6
        #   (2) ceil(n / 7) - (7 * ceil(n / 7) - n) groups of 7 and
        #       7 * ceil(n / 7) - n groups of 6.
        #
        # Although it would be inefficient, perhaps it's possible to do a
        # density check on the ranks to decide which case to choose.

    # Similarly, we can group the participants into groups of 7 and 8 if and only
    # if
    #
    #   num_participants (mod 7) <= floor(num_participants / 7).
    #
    # As the case of second priority, we check this condition second.

    elif ((num_participants % 7) <= (num_participants / 7)):
        
        num_groups = floor(num_participants / 7)

        # Similar to the previous case, there are two ways to make groups of 7
        # and 8 for n = num_participants >= 56.

    # For num_participants between 12 and 100, there's exactly one case where we
    # can't make groups of 6 and 7 or 7 and 8: when
    #
    #   num_participants = 17.

    else:
        
        num_groups = 3

    return num_groups

#

def distribute(participants, num_groups, clubs, map_to_groups, map_to_participants):

    # Initialize the groups to empty arrays and club counts to 0.

    groups = []

    for i in range(num_groups):

        groups.append([])

        for key in clubs.keys():
            clubs[key].append(0)

    # Put the participants into groups.

    for i in range(len(participants)):

        # Following the hint in the requirements, we assign paritipants to
        # groups in a snake-like fashion. Doing this, for
        # i = participants_so_far, we're assigning in the reverse order if
        # and only if
        #
        #   i mod (2 * num_groups) <= i mod (num_groups).

        if (i % (2 * num_groups) <= i % num_groups):
            group_num = i % num_groups

        else:
            group_num = num_groups - (i % num_groups) - 1

        groups[group_num].append(participants[i])

        club = participants[i][2]

        if (club != ''):
            clubs[club][group_num] += 1
        
        map_to_groups[i] = str(group_num) + ',' + str(floor(i / num_groups))
        map_to_participants[str(group_num) + ',' + str(floor(i / num_groups))] = i

    return groups

#

def resolve_conflicts(participants, groups, clubs, map_to_groups, map_to_participants):
    
    iterations = 0
    conflict_exists = True

    while (conflict_exists and iterations < 10000):

        iterations += 1
        conflict_exists = False
        club_to_swap = ''

        # Find if a conflict exists.

        for key in clubs.keys():

            min_club_count = floor(sum(clubs[key]) / len(groups))
            max_club_count = ceil(sum(clubs[key]) / len(groups))

            for i in range(len(groups)):

                if (not conflict_exists and (clubs[key][i] > max_club_count or clubs[key][i] < min_club_count)):

                    conflict_exists = True
                    club_to_swap = key

        if (conflict_exists):

            # Get groups with maximum and minimum number of conflicting members.

            max_groups = set()
            min_groups = set()
            min_club_count = floor(sum(clubs[club_to_swap]) / len(groups))
            max_club_count = ceil(sum(clubs[club_to_swap]) / len(groups))

            for i in range(len(clubs[club_to_swap])):
                if (clubs[club_to_swap][i] == max(clubs[club_to_swap])):
                    max_groups.add(i)
                if (clubs[club_to_swap][i] == min(clubs[club_to_swap])):
                    min_groups.add(i)

            # For each group of max size, look for a club member to swap.

            swapped = False

            for i in max_groups:

                for j in range(len(groups[i])):

                    if (not swapped and groups[i][j][2] == club_to_swap):

                        # Find index of participant in participants list.

                        participants_i = map_to_participants[str(i) + ',' + str(j)]

                        # Starting at the participant's index, walk up
                        # participants list until changing rank or top of list.

                        rank_letter = participants[participants_i][3]
                        rank_number = participants[participants_i][4]

                        k = participants_i

                        while k >= 0 and participants[k][3] == rank_letter and participants[k][4] == rank_number:
                            k -= 1

                        k += 1

                        # Variable k now holds the index of the first
                        # participant of the same rank.

                        # While there are participants of the same rank, find a
                        # partipicant of equal rank to swap with.

                        while not swapped and k < len(participants) and participants[k][3] == rank_letter and participants[k][4] == rank_number:

                            group_num_of_k = int(map_to_groups[k].partition(',')[0])

                            # Check if we've found a swap candidate.

                            if (group_num_of_k != i and participants[k][2] != club_to_swap):
                                
                                if (group_num_of_k in min_groups):

                                    swapped = True

                                    # Update clubs dict.

                                    clubs[club_to_swap][i] -= 1
                                    clubs[club_to_swap][group_num_of_k] += 1

                                    if (participants[k][2] != ''):
                                        clubs[participants[k][2]][i] += 1
                                        clubs[participants[k][2]][group_num_of_k] -= 1

                                    # Swap map_to_groups.

                                    temp = map_to_groups[k]
                                    map_to_groups[k] = map_to_groups[participants_i]
                                    map_to_groups[participants_i] = temp

                                    # Swap map_to_participants.

                                    temp = map_to_participants[map_to_groups[participants_i]]
                                    map_to_participants[map_to_groups[participants_i]] = map_to_participants[map_to_groups[k]]
                                    map_to_participants[map_to_groups[k]] = temp

                                    # Swap groups.

                                    i_1 = int(map_to_groups[k].partition(',')[0])
                                    j_1 = int(map_to_groups[k].partition(',')[2])
                                    i_2 = int(map_to_groups[participants_i].partition(',')[0])
                                    j_2 = int(map_to_groups[participants_i].partition(',')[2])

                                    temp = groups[i_1][j_1]
                                    groups[i_1][j_1] = groups[i_2][j_2]
                                    groups[i_2][j_2] = temp         
                                
                            k += 1

            # If we couldn't swap participants of equal rank, we look to swap
            # the lowest ranking participant in the max_groups.

            for i in max_groups:

                # Find the lowest ranking member of the club in this group.

                min_index = -1
                min_value = 999

                for j in range(len(groups[i])):

                    participants_i = map_to_participants[str(i) + ',' + str(j)]
                    club = participants[participants_i][2]

                    if (club == club_to_swap):

                        rank = participants[participants_i][3] + participants[participants_i][4]

                        if (map_to_integer(rank) < min_value):

                            min_index = participants_i
                            min_value = map_to_integer(rank)

                # Variable min_index now holds the index of the lowest-ranking
                # member of the club in this group.

                participants_i = min_index
                k = min_index

                # While there are participants left, find a partipicant of
                # lower rank to swap with.

                while not swapped and k < len(participants):

                    group_num_of_k = int(map_to_groups[k].partition(',')[0])

                    # Check if we've found a swap candidate.

                    if (group_num_of_k != i and participants[k][2] != club_to_swap):
                        
                        if (group_num_of_k in min_groups):

                            swapped = True

                            # Update clubs dict.

                            clubs[club_to_swap][i] -= 1
                            clubs[club_to_swap][group_num_of_k] += 1

                            if (participants[k][2] != ''):
                                clubs[participants[k][2]][i] += 1
                                clubs[participants[k][2]][group_num_of_k] -= 1

                            # Swap map_to_groups.

                            temp = map_to_groups[k]
                            map_to_groups[k] = map_to_groups[participants_i]
                            map_to_groups[participants_i] = temp

                            # Swap map_to_participants.

                            temp = map_to_participants[map_to_groups[participants_i]]
                            map_to_participants[map_to_groups[participants_i]] = map_to_participants[map_to_groups[k]]
                            map_to_participants[map_to_groups[k]] = temp

                            # Swap groups.

                            i_1 = int(map_to_groups[k].partition(',')[0])
                            j_1 = int(map_to_groups[k].partition(',')[2])
                            i_2 = int(map_to_groups[participants_i].partition(',')[0])
                            j_2 = int(map_to_groups[participants_i].partition(',')[2])

                            temp = groups[i_1][j_1]
                            groups[i_1][j_1] = groups[i_2][j_2]
                            groups[i_2][j_2] = temp             
                        
                    k += 1
                    

    return

#

def write_output(groups):

    print ("\nPool List")
    
    for i in range(len(groups)):
        
        print (
            '--)------- Pool # ' + str(i + 1) + ' -------(--' +
            ' (' + str(len(groups[i])) + ')'
        )
        
        for j in range(len(groups[i])):

            first_name = groups[i][j][0]
            last_name = groups[i][j][1]
            club = groups[i][j][2]
            rank_letter = groups[i][j][3]
            rank_number = groups[i][j][4]

            print (
                f'{first_name:21}' +
                f'{last_name:24}' +
                f'{club:24}' +
                f'{rank_letter:8}' +
                f'{rank_number:2}'
            )

        print ('')

    return

#

def handle_argument_error():

    print ('Usage: python3 FencingTournament.py [filename]')
    return

#

def handle_file_error():

    print ('Unable to open file.')
    return


main()