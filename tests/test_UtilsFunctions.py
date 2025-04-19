import unittest

from UtilsFunctions import check_yeld, generator_univ


class TestCheckYeld(unittest.TestCase):

    def test_all_true(self):
        # Test when all elements in the list are truthy
        self.assertTrue(check_yeld([1, 2, 3, True, "text"]))

    def test_all_false(self):
        # Test when all elements in the list are falsy
        self.assertFalse(check_yeld([0, None, False, ""]))

    def test_mixed_values(self):
        # Test when the list has a mix of truthy and falsy elements
        self.assertTrue(check_yeld([0, False, None, 1, "", True]))

    def test_empty_list(self):
        # Test when the list is empty
        self.assertFalse(check_yeld([]))

    def test_single_truthy_element(self):
        # Test when the list contains only one truthy element
        self.assertTrue(check_yeld([1]))

    def test_single_falsy_element(self):
        # Test when the list contains only one falsy element
        self.assertFalse(check_yeld([0]))


class TestGeneratorUniv(unittest.TestCase):

    def test_generator_with_list(self):
        # Ensure generator_univ yields all elements from a list
        self.assertEqual(list(generator_univ([1, 2, 3])), [1, 2, 3])

    def test_generator_with_string(self):
        # Ensure generator_univ yields the string as a single element
        self.assertEqual(list(generator_univ("text")), ["text"])

    def test_generator_with_empty_string(self):
        # Ensure generator_univ raises StopIteration for an empty string
        with self.assertRaises(StopIteration):
            next(generator_univ(""))

    def test_generator_with_single_item(self):
        # Ensure generator_univ yields the single item correctly
        self.assertEqual(list(generator_univ(42)), [42])

    def test_generator_with_nested_list(self):
        # Ensure generator_univ yields nested lists correctly
        self.assertEqual(list(generator_univ([[1, 2], 3])), [[1, 2], 3])


if __name__ == "__main__":
    unittest.main()
