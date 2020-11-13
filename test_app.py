import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db,Movie, Actor
from auth import AuthError, requires_auth



CASTING_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlB1cks3ZlJDZGNyZUlqLVdlaXNyRSJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5MS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZhY2U0MjY5YWIyZDAwMDc2ZjlhZjVlIiwiYXVkIjoiY2FzdGluZ3MiLCJpYXQiOjE2MDUyMTQzMzgsImV4cCI6MTYwNTMwMDczOCwiYXpwIjoiZkM0WFNnUFYzYjF6SDAwblpPY3hWUkhVT0FsT0FYaXkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.G00H8nYhxEbNs2m4IjLSP5_KtA8hX5B87_clpjFGfFKmR6bn6wNyxnRHT0lPa6EhxDD7fV6l6H9RX6f_iFnl1u_2E9gchLvf76AarYNHo3cgxAKKem0iUpp5q8ITvWo_jWtPzYOQau0G0evEcs4-D6nwMA-MGHi7S9o7mIr1RYbX3PugFUtbWGdED-ar09btbNc6dehBnXdDBFpf1zskt8Fb4gCr0B9nrkWkbUbSGT5sDlqS26t9hQAdOcdhubCjmbEQXU6_VGRs5Se-19JaEyrt1gQX_fRhu00Uz-UpB34zMdItfMhON6HJMlqZHyMHR_CR-Pw8ezohnBMYqZOJcA'
CASTING_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlB1cks3ZlJDZGNyZUlqLVdlaXNyRSJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5MS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZhY2U2ZDk5YWIyZDAwMDc2ZjliMTBhIiwiYXVkIjoiY2FzdGluZ3MiLCJpYXQiOjE2MDUyMTQ0MTAsImV4cCI6MTYwNTMwMDgxMCwiYXpwIjoiZkM0WFNnUFYzYjF6SDAwblpPY3hWUkhVT0FsT0FYaXkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.FtvHJFOb6NDbV6bM_rfrCzO0P02WiSa2NB9QNrM4qIl6RTgmEcXk3J0LN3BPyFzPxsDwUm-6FSEM9ij3tH0-BRSnNRzv9YVvcQ_G7BJj9jef2_3rswgakydV5h2eqzFN1kzoIr4iIpTgBHqM3xr8dk8XPIOEELHcDmGBRjJJOwRiabS4cAllC_ZIhNfUvXKNACydlyxTE5-hLVp0KNV1gNhDzLfjmuyaRooigyHVNeQthBvR30YqFwYJJMyd_H1eZbe7P0Tvk-vQpsGuI2m1rKfBuzq-xroxIiiqe84hWPdBBQ2lNyzNEzSecmhYhlWMrdfPpthqI78VdbwKrKocjg'
EXECUTIVE_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlB1cks3ZlJDZGNyZUlqLVdlaXNyRSJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5MS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZhY2U0OGM4MGExZWYwMDZmNDIwMjRhIiwiYXVkIjoiY2FzdGluZ3MiLCJpYXQiOjE2MDUyMTQ0ODksImV4cCI6MTYwNTMwMDg4OSwiYXpwIjoiZkM0WFNnUFYzYjF6SDAwblpPY3hWUkhVT0FsT0FYaXkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.3Rpb5eF1SYy32t5vf6rrwLDz78hI0-3TfS-1c0SfWeg16rl24-P0YAPPcWv7VZuPjYWnISOZkwfmjEQdOf7Yzatdvmz4qF_Z1EDzj0kGGRDTryQOlJMit2W71H7qv8s4SmzJdfZfBybSpU766hm9fAXa42sEeIHe05ny4XBQ6wiix4VSFi8kdwLLuOPVGQP0pxQwxJ6rPKpOM74Ihs0KJoIyaBINbnSloUnsQF5FtG0LWZec0aT7EkKGjj52CiBKbC84Jx4evBEZYrwCyoizxVT6bhJL1TKvx1Np_xLnls7vRpL8ukCjbrrMgE2ZSrGQ3Q08RLOJ-hCGXOJQXq3knQ'


class CastingAgencyTest(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "castingagency"
        self.database_path = "postgres://{}@{}/{}".format('postgres:postgres','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)


        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        self.new_actor = {'name': 'John',
                            'age': '20',
                            'gender': 'male' }
                        
        self.new_movie = {'title': 'Twilight',
                                    'releaseDate' :  '2009-01-01' }
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def get_movies_test(self):
        res = self.client().get('/movies', headers = {'Authorization':  'Bearer ' + CASTING_ASSISTANT}  )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def get_movies_error(self):
        error_movie = Movie( title = None)
        error_movie.insert()
        res = self.client().get('/movies', headers = {'Authorization':  'Bearer ' + CASTING_ASSISTANT} )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')
        error_movie.delete()
        
    def get_actors_test(self):
        res = self.client().get('/actors', headers = {'Authorization':  'Bearer ' + CASTING_ASSISTANT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def get_actors_error(self):
        error_actor = Actor( name = None)
        error_actor.insert()
        res = self.client().get('/actors', headers = {'Authorization':  'Bearer ' + CASTING_ASSISTANT} )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')
        error_actor.delete()





    def test_delete_movie_success(self):
        
        res = self.client().delete('/movies/1' ,  headers = {'Authorization':  'Bearer ' + EXECUTIVE_PRODUCER} )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
     
        
        
    def test_delete_movies_error(self):
        res = self.client().delete('/movies/1000', headers = {'Authorization':  'Bearer ' + EXECUTIVE_PRODUCER} )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable entity')
        
    def test_delete_actor_success(self):
        
        res = self.client().delete('/actors/1' ,  headers = {'Authorization':  'Bearer ' + CASTING_DIRECTOR} )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
        
        
    def test_delete_actor_error(self):
        res = self.client().delete('/actors/1000', headers = {'Authorization':  'Bearer ' + CASTING_DIRECTOR} )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable entity')
        
  

    def test_add_movie(self):
        res = self.client().post('/movies', headers = {'Authorization':  'Bearer ' + EXECUTIVE_PRODUCER}, json= self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_add_movie_error(self):
        self.new_movie['title'] = None
        res = self.client().post('/movies', headers = {'Authorization':  'Bearer ' + EXECUTIVE_PRODUCER}, json= self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable entity')
        
    def test_add_actor(self):
        res = self.client().post('/actors', headers = {'Authorization':  'Bearer ' + EXECUTIVE_PRODUCER}, json= self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_add_actor_error(self):
        self.new_actor['name'] = None
        res = self.client().post('/actors', headers = {'Authorization':  'Bearer ' + EXECUTIVE_PRODUCER}, json= self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable entity')
        
    def test_update_movie(self):
        res = self.client().patch('/movies/1', headers = {'Authorization':  'Bearer ' + EXECUTIVE_PRODUCER}, json={'title' : 'new test title'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated'])

    def test_update_movie_error(self):
        res = self.client().patch('/movies/10000', headers = {'Authorization':  'Bearer ' + EXECUTIVE_PRODUCER} )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')
        
    def test_update_actor(self):
        res = self.client().patch('/actors/1', headers = {'Authorization':  'Bearer ' + EXECUTIVE_PRODUCER}, json={'name' :'new test name'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated'])

    def test_update_actor_error(self):
        res = self.client().patch('/actors/10000', headers = {'Authorization':  'Bearer ' + EXECUTIVE_PRODUCER} )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')
        
    #casting agency success has already been tested with get movies and get actors
    def test_casting_agency_error(self):
        res = self.client().delete('/movies/1', headers = {'Authorization':  'Bearer ' + CASTING_ASSISTANT} )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')
        
    #casting director success tested with delete actor success 
    
    def test_casting_director_error(self):
        res = self.client().delete('/movies/1' ,  headers = {'Authorization':  'Bearer ' + CASTING_DIRECTOR} )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],  'Permission not found.' )
    
    #Executive producer success tested already with add and delete movie
    



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()