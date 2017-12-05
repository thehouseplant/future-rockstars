import json
import unittest
from app import app
from assign_bands import *
from assign_dorms import *
from collections import defaultdict


class BandsTestCase(unittest.TestCase):
    @classmethod
    def setupClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass
    
    def setUp(self):
        #print('Setting up bands test case')
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
        talent_type = ['Singer','Guitarist','Drummer',
                        'Bassist','Keyboardist','Instrumentalist']
        for i in range(len(result)):
            k = 0
            t_sum = []
            for j in talent_type:
                item = result[i][j].split(' || ')
                if item[1] == 'male':
                    k+=1
                t_sum.append(int(item[-1]))
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

    def tearDown(self):
        pass


class DormsTestCase(unittest.TestCase):
    @classmethod
    def setupClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass
    
    def setUp(self):
        #print('Setting up dorms test case')
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
    
    def tearDown(self):
        pass


class ViewsTestCase(unittest.TestCase):
    @classmethod
    def setupClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        #print('Setting up views test case')
        self.app = app.test_client()
        self.app.testing = True

    def test_404(self):
        response = self.app.get('/wrong/url')
        self.assertEqual(response.status_code, 404)

    def test_index_view(self):
        response = self.app.get('/index', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_bands_view(self):
        response = self.app.get('/bands', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_dorms_view(self):
        response = self.app.get('/dorms', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_members_view(self):
        response = self.app.get('/members', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_members_add_view(self):
        response = self.app.get('/members/add', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_members_add(self):
        response = self.app.post('/members/submit', data={
            'memberId': '99999',
            'type': 'member',
            'firstName': 'James',
            'lastName': 'Testman',
            'gender': 'male',
            'age': 15,
            'street': '123 Fake St',
            'city': 'Testville',
            'state': 'CA',
            'zipCode': 91000,
            'phone': '000-000-0000',
            'talent': 'Guitarist',
            'cohort': 'first',
            'status': 'Pending',
            'checkin': False,
            'forms': False,
            'payment': False
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_members_delete(self):
        response = self.app.post('/members/delete', data={
            'memberId': '99999'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_members_checkout(self):
        response = self.app.post('/members/checkout', data={
            'memberId': '99999'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_members_checkin(self):
        response = self.app.post('/members/checkin', data={
            'memberId': '99999'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    '''def test_members_edit(self):
        response = self.app.post('/members/edit', data={
            'memberId': '99999'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_members_update(self):
        response = self.app.post(
            '/members/update',
            data=dict(
                memberId=99999,
                type="member", 
                firstName="James",
                lastName="Testman", 
                gender="Male", 
                age=15, 
                street="123 Fake St", 
                city="Faketown",
                state="CA",
                zipCode=91000,
                talent="Guitarist",
                status="Pending",
                checkin=False,
                forms=False,
                payment=False
            ),
            follow_redirects=True
        )
        self.assertIn(b"Testing Member update", response.data)

    def test_email_send(self):
        response = self.app.post(
            '/email/send',
            data=dict(
                memberId=99999,
                type="Rejected"
            ),
            follow_redirects=True
        )
        self.assertIn(b"Testing Email send", response.data)'''

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
