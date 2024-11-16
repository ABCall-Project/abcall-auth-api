import unittest
from flaskr.domain.models import Role

class RoleTestCase(unittest.TestCase):
        def setUp(self):
            self.auth = Role(
                id="a257ee3b-c1c6-4139-84bc-f70595a1c780",
                name="admin"
            )
        
        def test_init(self):
            self.assertEqual(self.auth.id, "a257ee3b-c1c6-4139-84bc-f70595a1c780")
            self.assertEqual(self.auth.name, "admin")

        def test_to_dict(self):
            result = self.auth.to_dict()
            expected_dict = {
                'id': "a257ee3b-c1c6-4139-84bc-f70595a1c780",
                'name': "admin"
            }
            self.assertEqual(result, expected_dict)