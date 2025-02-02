import unittest
from src.youtube.main import github


class TestMain(unittest.TestCase):
    def test_github(self):
        self.assertEqual(github(), 200)
        self.assertNotEqual(github(), 404)
        self.assertNotEqual(github(), 500)


if __name__ == "__main__":
    unittest.main()
