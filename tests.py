import json
import unittest
from app import app


class ViewsTestCase(unittest.TestCase):
    @classmethod
    def setupClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
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
