# Insert
# if new TE is inside an existing TE disable the latter
        # look if pos is between pos and length of an active TE
        # if pos     te:
        #     self.TEs[] = [pos, length, 'D']

        # The TEs are numbered by insertion order so in __str__ the genome is constructed by inserting the TEs one at a time


        # for te in self.active_TEs:
        #     if te[0]
        
        # for i in range(pos, pos+length+1):
        #     if self.genome[i] != '-':
        #         # overwrite TE with '' in genome
        #         dis_TE = self.active_TEs[self.genome[i]]
        #         for nuc in range(dis_TE[0],dis_TE[0]+dis_TE[1]+1):  # if I know where the TE starts I can overwrite without looking
        #             self.genome[nuc] = '-'
        #         # remove existing TE from dict
        #         self.active_TEs.pop(self.genome[i])
        
        #     # insert new TE
        #     self.genome[i] = 'TE_ID'


   # if te in active_TEs:    
        # # change pos in dictionary
        #     self.active_TEs[te][0] += offset
        #     return



      # if te in active_TEs:
        #     # overwrite TE with '' in genome
        #     dis_TE = self.active_TEs[self.genome[i]]
        #     for nuc in range(dis_TE[0],dis_TE[0]+dis_TE[1]+1):
        #         self.genome[nuc] = '-'
        #     # remove existing TE from dict
        #     self.active_TEs.pop(self.genome[i])




# test_genome = ['-']*25

# test_TE_dict = {}
# test_TE_dict[1] = [2, 8, 'D']
# test_TE_dict[2] = [5, 9, 'A']
# test_TE_dict[3] = [29, 5, 'A']

# print(test_TE_dict)
# print(test_TE_dict[1][0])

# print(test_genome)
# print(test_genome[:test_TE_dict[1][0]])

# print(test_TE_dict[1][1])


# for te in test_TE_dict:

#     if test_TE_dict[te][2] == 'A':
#         test_genome = test_genome[:test_TE_dict[te][0]] + ['A']*test_TE_dict[te][1] + test_genome[test_TE_dict[te][0]:]
#     else:
#         test_genome = test_genome[:test_TE_dict[te][0]] + ['x']*test_TE_dict[te][1] + test_genome[test_TE_dict[te][0]:]

# print(test_genome)
# print(''.join(test_genome))

# __str__
 # maybe sorted(my_dict.items())
        # it should iterate in order of insertion, that is from 1 and upwards
        # for te in self.TEs:
        #     if self.TEs[te][2] == 'A':
        #         self.genome = self.genome[:self.TEs[te][0]] + ['A']*self.TEs[te][1] + self.genome[self.TEs[te][0]:]
        #     else:
        #         self.genome = self.genome[:self.TEs[te][0]] + ['x']*self.TEs[te][1] + self.genome[self.TEs[te][0]:]


# Look at lengt. I could move upwards trough As until meeting - or x, but there could be another active TE right next to this one, so i wouldnt know when to stop.


#Linkedlist

#  def __iter__(self):
#         current = self.head.next
#         while current is not self.head:
#             yield current.val
#             current = current.next

        # for l in self.head:
        #     # skips dummy link in __iter__ by going to self.head.next
        #     if count == pos:
        #         # insert 'A'*length at pos
        #         for _ in range(length):
        #             insert_after(l, 'A')    # or insert before? no
        #     count += 1