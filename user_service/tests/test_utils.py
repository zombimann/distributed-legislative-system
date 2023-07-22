# tests/test_utils.py

from tests import BaseTestCase
from app.utils import generate_password_hash, check_password_hash

class UtilsTestCase(BaseTestCase):
    def test_password_hashing(self):
        password = "test_password"
        password_hash = generate_password_hash(password)
        self.assertTrue(check_password_hash(password_hash, password))

if __name__ == '__main__':
    unittest.main()
