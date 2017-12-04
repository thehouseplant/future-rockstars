import unittest
import json
from assign_bands import *
from collections import defaultdict

class bandsTest(unittest.TestCase):
    def setUp(self):
        print('setup')
        db = open('./data/members_test.json', 'r')
        self.test_data = json.loads(db.read())
        db.close()
        re_tem = open('./data/bands.json', 'r')
        self.result = json.loads(re_tem.read())
        re_tem.close()
        db = open('./data/bands2.json','r')
        self.backup_data = json.loads(db.read())
        db.close()
    
    #gray_box
    def test_gendergrade(self):
        test_data_input = self.test_data['gender_test'][0]
        test_data_output = self.test_data['gender_test'][1]
        temp_test = male_female_grade(test_data_input)
        self.assertEqual(test_data_output, temp_test)
    
    def test_average_variance(self):
        test_data_input = self.test_data['trank_test_ave'][0]
        test_data_output = self.test_data['trank_test_ave'][1]
        test_data_input_var = self.test_data['trank_test_var'][0]
        test_data_output_var = self.test_data['trank_test_var'][1]
        for i in range(len(test_data_input)):
            temp_test_ave = average(test_data_input[i])
            self.assertEqual(test_data_output[i],temp_test_ave)
            temp_test = variance(test_data_input_var[i],temp_test_ave)
            self.assertEqual(test_data_output_var[i],temp_test)

    #black_box: assign_bands
    def test_assign_bands(self):
        result = self.result
        gender_list = []
        trank_list = []
        talent_type = ['singer','guitarist','drummer',
                        'bassist','keyboardist','instrumentalist']
        for i in range(len(result)):
            k = 0
            t_sum = []
            for j in talent_type:
                item = result[i][j].split(' || ')
                if item[1] == 'male':
                    k+=1
                t_sum.append(int(item[3]))
            if abs(k-3) < 3:
                gender_list.append(1)
            else:
                gender_list.append(0)
            t_ave = average(t_sum)
            t_var = variance(t_sum,t_ave)
            if abs(t_var - 1.25) < 1.25:
                trank_list.append(1)
            else:
                trank_list.append(0)
            
            self.assertEqual(1,gender_list[i])
            self.assertEqual(1,trank_list[i])
        
if __name__ == '__main__':
    unittest.main()
