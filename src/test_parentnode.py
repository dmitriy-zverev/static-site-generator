import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_no_children(self):
        try:
            parent_node = ParentNode("div", None)
        except ValueError as e:
            self.assertEqual(str(e), "Error: ParentNode object must have children")

    def test_to_html_multiple_children(self):
        child_node1 = LeafNode("span", "child 1")
        child_node2 = LeafNode("p", "child 2")
        child_node3 = LeafNode(None, "child 3 raw")
        parent_node = ParentNode("div", [child_node1, child_node2, child_node3])
        self.assertEqual(
            parent_node.to_html(), 
            "<div><span>child 1</span><p>child 2</p>child 3 raw</div>"
        )

    def test_to_html_multiple_nested_parents(self):
        grandchild_node1 = LeafNode("b", "grandchild 1")
        grandchild_node2 = LeafNode("div", "grandchild 2")

        child_node1 = ParentNode("span", [grandchild_node1])
        child_node2 = ParentNode("p", [grandchild_node2])

        parent_node = ParentNode("div", [child_node1, child_node2])

        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild 1</b></span><p><div>grandchild 2</div></p></div>",
        )


if __name__ == "__main__":
    unittest.main()