import unittest
import json
from assign_dorms import *
from collections import defaultdict

#black_box
class bandsTest(unittest.TestCase):
    def setUp(self):
        print('setup')
        db = open('./data/dorms.json','r')
        dorms_data = json.loads(db.read())
        db.close()
        db = open('./data/members.json','r')
        self.member = json.loads(db.read())
        ids = []
        ages = []
        for i in range(len(dorms_data)):
            ids_temp = []
            ages_temp = []
            for j in dorms_data[i]['members']:
                item = j.split(' || ')
                ids_temp.append(item[0])
                ages_temp.append(int(item[1]))
            ids.append(ids_temp)
            ages.append(ages_temp)
        self.dorms_data = dorms_data
        self.ids = ids
        self.ages = ages        
 
    def test_length(self):
        dorm = self.dorms_data
        for i in range(len(dorm)):
            mem_sum = len(dorm[i]['members'])
            self.assertEqual(8,mem_sum)
            
    def test_gender(self):
        ids = self.ids
        dorms = self.dorms_data
        gender = []
        for i in range(len(dorms)):
            gender=dorms[i]['gender']
            for j in range(len(dorms[i]['members'])):
                for person in self.member:
                    if person['memberId'] == ids[i][j]:
                        self.assertEqual(gender,person['gender'])
                
    def test_age(self):
        ages = self.ages
        for i in range(len(ages)):
            sum = 0
            k = 0
            for j in ages[i]:
                sum +=j
                k+=1
            ave = sum/k
            if abs(ave - 15.5) < 2:
                s = 1
            else:
                s = 0
            self.assertEqual(1,s)
                
    
        
if __name__ == '__main__':
    unittest.main()
