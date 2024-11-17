import unittest
from backpack import Backpack, ITEMS, Item

class BackpackTest(unittest.TestCase):

    def setUp(self):
        self.backpack = Backpack()

    def test_add_item(self):
        # Test adding an item that exists
        self.assertTrue(self.backpack.add_item('sandwich'))
        self.assertEqual(self.backpack.items['sandwich'], ITEMS['sandwich'])

        # Test adding an item that doesn't exist
        self.assertFalse(self.backpack.add_item('nonexistent_item')[0])

        # Test adding an item when the backpack is full
        self.backpack.add_item('water bottle')
        self.backpack.add_item('flashlight')
        self.backpack.add_item('map')
        self.backpack.add_item('rope')  # Backpack is now full
        #print("Weight is now: " + str(self.backpack.current_weight()))
        #confirm backpack is full
        self.assertEqual(self.backpack.current_weight(), 10)

        #fail at attempting to add one more item
        self.assertFalse(self.backpack.add_item('first aid kit')[0])

    def test_use_item(self):
        # Test using an item that exists
        self.backpack.add_item('sandwich')
        self.assertTrue(self.backpack.use_item('sandwich')[0])
        self.assertEqual(self.backpack.items['sandwich'].uses, ITEMS['sandwich'].uses - 1)

        # Test using an item that doesn't exist
        self.assertFalse(self.backpack.use_item('nonexistent_item')[0])

        # Test using an item with no uses left
        self.backpack.add_item('water bottle')
        for _ in range(ITEMS['water bottle'].uses):
            self.backpack.use_item('water bottle')
        self.assertFalse(self.backpack.use_item('water bottle')[0])

    def test_current_weight(self):
        self.assertEqual(self.backpack.current_weight(), 0)
        self.backpack.add_item('sandwich')
        self.assertEqual(self.backpack.current_weight(), ITEMS['sandwich'].weight)

    def test_list_items(self):
        self.assertEqual(self.backpack.list_items(), "Your backpack is empty!")
        self.backpack.add_item('sandwich')
        self.backpack.add_item('water bottle')
        expected_output = "\nYour Backpack Contents:\n- sandwich (Uses left: 2)\n- water bottle (Uses left: 3)\nTotal Weight: 3/10"
        self.assertEqual(self.backpack.list_items(), expected_output)


if __name__ == '__main__':
    unittest.main()