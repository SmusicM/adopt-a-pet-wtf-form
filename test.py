from unittest import TestCase

from app import app
from models import db, Pet


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt_test'
app.config['SQLALCHEMY_ECHO'] = False


app.config['TESTING'] = True


app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


app.config['WTF_CSRF_ENABLED'] = False

app_context = app.app_context()
app_context.push()


db.drop_all()
db.create_all()

class TestPet(TestCase):
    """Test for views for pets"""

    def setUp(self):
        """test pet"""
        Pet.query.delete()
        pet = Pet(name="TestPet" , species = "Dog" , age=2, notes = "test notes",available=True)
        db.session.add(pet)
        db.session.commit()
        self.pet_id = pet.id

    def tearDown(self):
        db.session.rollback()
       

    def test_home_page(self):
        with app.test_client() as client:
            resp = client.get('/')
            self.assertEqual(resp.status_code,200)

    def test_add_pet_form(self):
        with app.test_client() as client:
            resp = client.get('/add')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn("<form", html)

    def test_add_pet(self):
        with app.test_client() as client:
            d = {"name":"TestPet","species": "dog","age":"2","notes":"test notes","available":"True"}
            resp = client.get('/add',data=d,follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn("<form",html)

    def test_edit_pet_form(self):
        with app.test_client() as client:
            resp = client.get(f"/{self.pet_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<form", html)

    def test_edit_pet(self):
        with app.test_client() as client:
            d = {"name":"TestPet","species": "dog","age":"2","notes":"test notes2","available":"False"}
            resp = client.get(f"/{self.pet_id}",data=d,follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            pet = Pet(name="TestPet" , species = "Dog" , age=2, notes = "test notes2",available=False)
            self.assertEquals(pet.notes,"test notes2")
            self.assertEquals(pet.available,False)