import unittest

from app import app

class HearlyTest(unittest.TestCase):
    ############################
    #### setup and teardown ####
    ############################

    # execute prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()

        self.assertEquals(app.debug, False)

    # execute after each test
    def tearDown(self):
        pass

    ##############
    #### test ####
    ##############
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertIn(b'Hearly', response.data)
        self.assertIn(b'HOLLYWOOD', response.data)
        self.assertIn(b'Fill in the Blank', response.data)
        self.assertIn(b'Be Hearing', response.data)
        self.assertIn(b'Watch movie without subtitles', response.data)
        self.assertIn(b'Log in', response.data)
        self.assertIn(b'Invite code', response.data)
        self.assertIn(b'beta', response.data)




    if __name__ == '__main__':
        unittest.main()



