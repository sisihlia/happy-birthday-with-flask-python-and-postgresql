import unittest
import json
import requests
import app
from datetime import date,datetime
import time


BASE_URL = 'http://127.0.0.1:5000/hello'
HEADERS={"Content-Type": "application/json"}
NAME_NENE="Nene"
NAME_BAD_NENE_1="Nene123"
NAME_NONO="Nono"
NAME_BAD_NENE_2="Nene@"
NAME_BAD_NONO_1="Nono123"
NAME_BAD_NONO_2="Nono@"
NAME_NOT_FOUND="Notfound"
TODAY=datetime.today().strftime('%Y-%m-%d')



class SequentialTestLoader(unittest.TestLoader):
    def getTestCaseNames(self, testCaseClass):
        test_names = super().getTestCaseNames(testCaseClass)
        testcase_methods = list(testCaseClass.__dict__.keys())
        test_names.sort(key=testcase_methods.index)
        return test_names


class TestBirthdates(unittest.TestCase):

   

    def test_a_get_all(self):
        r = requests.get(BASE_URL)
        #print(r.json)
        self.assertEqual(r.status_code, 200)

    #test to create a birthdate (PUT) and check the birthday
    def test_b_create_birthdate_put(self):
        user_payload = json.dumps({
            "birth_date": "2017-12-13"
        })        
        r = requests.put(BASE_URL+"/"+NAME_NENE, headers=HEADERS, data=user_payload)
        self.assertEqual(r.status_code, 204)
        
    #test to create a birthdate (PUT) with invalid name
    def test_c_create_birthdate_put_with_invalid_name(self):
        user_payload = json.dumps({
            "birth_date": "2021-12-13"
        })        
        r = requests.put(BASE_URL+"/"+NAME_BAD_NENE_1, headers=HEADERS, data=user_payload)
        self.assertEqual(r.status_code, 400)
        self.assertIn("invalid argument",r.json['message'])

        c = requests.put(BASE_URL+"/"+NAME_BAD_NENE_2, headers=HEADERS, data=user_payload)
        self.assertEqual(r.status_code, 400)
        self.assertIn("invalid argument",c.json['message'])

    #test to create a birthdate (PUT) with invalid birthdate
    def test_d_create_birthdate_put_with_invalid_birthdate(self):
        user_payload = json.dumps({
            "birth_date": "2021-02-13"
        })        
        r = requests.put(BASE_URL+"/"+NAME_NENE, headers=HEADERS, data=user_payload)
        self.assertEqual(r.status_code, 400)
        self.assertIn("invalid argument",r.json['message'])

    #test to create a birthdate (POST) and check the birthday
    def test_e_create_birthdate_post(self):
        user_payload = json.dumps({
            "name": NAME_NONO,
            "birth_date": TODAY
        })        
        r = requests.post(BASE_URL, headers=HEADERS, data=user_payload)
        self.assertEqual(r.status_code, 204)
        
    #test to create a birthdate (POST) with invalid name
    def test_f_create_birthdate_post_with_invalid_name(self):
        user_payload = json.dumps({
            "name": NAME_BAD_NONO_1,
            "birth_date": "2021-12-13"
        })        
        r = requests.post(BASE_URL, headers=HEADERS, data=user_payload)
        self.assertEqual(r.status_code, 400)
        self.assertIn("invalid argument",r.json['message'])
    
    #test to create a birthdate (POST) with invalid name 2
    def test_g_create_birthdate_post_with_invalid_name_2(self):
        user_payload = json.dumps({
            "name": NAME_BAD_NONO_2,
            "birth_date": "2021-12-13"
        })        
        r = requests.post(BASE_URL, headers=HEADERS, data=user_payload)
        self.assertEqual(r.status_code, 400)
        self.assertIn("invalid argument",r.json['message'])

    #test to creat a birthdate (POST) with invalid birthdate
    def test_h_create_birthdate_post_with_invalid_birthdate(self):
        user_payload = json.dumps({
            "name": NAME_NONO,
            "birth_date": "2018-08-13"
        })        
        r = requests.post(BASE_URL, headers=HEADERS, data=user_payload)
        self.assertEqual(r.status_code, 400)
        self.assertIn("invalid argument",r.json['message'])

    #test to assert the incoming days before birthday
    def test_i_get_birthdate_by_name(self):
        c = requests.get(BASE_URL+"/"+NAME_NENE)
        birthdate=app.Birthdates.get_by_name(NAME_NENE)
        self.assertIn(str(app.count_birthday(birthdate[0].birth_date, date.today())),c.json['message'])

    #test to assert today is the birthday
    def test_j_get_birthdate_by_name_to_birthday(self):
        c = requests.get(BASE_URL+"/"+NAME_NONO)
        self.assertIn("Happy birthday",c.json['message'])

    #test to assert to not found
    def test_k_get_not_exist_by_name(self):
        r = requests.get(BASE_URL+"/"+NAME_NOT_FOUND)
        self.assertEqual(r.status_code, 404)
        self.assertIn("not found",r.json['message'])
    
    #test to update (PUT) the birthdate by name
    def test_l_update_put (self):
        user_payload = json.dumps({
            "birth_date": "2017-12-13"
        })        
        r = requests.put(BASE_URL+"/"+NAME_NONO, headers=HEADERS, data=user_payload)
        self.assertEqual(r.status_code, 204)

        c = requests.get(BASE_URL+"/"+NAME_NONO)
        birthdate=app.Birthdates.get_by_name(NAME_NONO)
        print(c.json['message'])
        self.assertIn(str(app.count_birthday(birthdate[0].birth_date, date.today())),c.json['message'])

 
    #test to update (PUT) the birthdate by name with invalid birthdate
    def test_m_update_put_with_invalid_birthdate (self):
        user_payload = json.dumps({
            "birth_date": "2017-02-13"
        })        
        r = requests.put(BASE_URL+"/"+NAME_NONO, headers=HEADERS, data=user_payload)
        self.assertEqual(r.status_code, 400)

    #test to create (POST) the birthdate by the same name
    def test_n_create_post_resource_with_the_same_name(self):
        user_payload = json.dumps({
            "name": NAME_NENE,
            "birth_date": TODAY
        })        
        r = requests.post(BASE_URL, headers=HEADERS, data=user_payload)
        self.assertEqual(r.status_code, 204)


    #test to get the resource with multiple result
    def test_o_get_multiple_resources(self):      
        r = requests.get(BASE_URL+"/"+NAME_NENE)
        self.assertEqual(r.status_code, 400)
        self.assertIn("More than one resources with the same name found",r.json['message'])

    #test to delete the resource with multiple result
    def test_p_delete_multiple_resources(self):      
        r = requests.delete(BASE_URL+"/"+NAME_NENE)
        self.assertEqual(r.status_code, 400)
        self.assertIn("More than one resources with the same name found",r.json['message'])

    #test to delete the resource
    def test_q_delete_resource(self):   
        r = requests.delete(BASE_URL+"/"+NAME_NONO)
        self.assertEqual(r.status_code, 200)
        self.assertIn("Deleted",r.json['message'])

if __name__ == "__main__":
    unittest.main()