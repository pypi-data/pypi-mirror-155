#!/usr/bin/env python3
import random as rand

def rand_id_generator(list_size):
    list_size_arg = list_size
    rand_seed = rand.randint(1,10)
    wordlist = f'words-{rand_seed}.txt'
    with open (wordlist, 'a+') as file:
        for i in range(0, list_size_arg):
            rand_no = rand.randint(10**11, 10**12)
            file.write(str(rand_no)+'\n')
    return wordlist