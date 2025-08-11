import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_div(self):
        node = LeafNode("div", "This is div")
        self.assertEqual(node.to_html(), "<div>This is div</div>")

    def test_leaf_with_props(self):
        node = LeafNode("div", "This is div", {"href": "localhost"})
        self.assertEqual(node.to_html(), "<div href=\"localhost\">This is div</div>")
    
    def test_no_children(self):
        node = LeafNode("div", "This is div")
        self.assertEqual(node.children, [])

    def test_no_value(self):
        try: 
            node = LeafNode("div", None)
        except ValueError as e:
            self.assertEqual(str(e), "Error: LeafNode must have a value")
    
    def test_no_tag(self):
        node = LeafNode(None, "Some text without tags")
        self.assertEqual(node.to_html(), "Some text without tags")
        