import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_create_empty_node(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, None)

    def test_create_node(self):
        node = HTMLNode("p", None, None, None)
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, None)

        node = HTMLNode("p", "text", None, None)
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "text")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, None)

        child_nodes = [HTMLNode("p", "text", None, None), HTMLNode("p", "text", None, None)]
        node = HTMLNode("p", "text", child_nodes, None)
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "text")
        self.assertEqual(node.children, child_nodes)
        self.assertEqual(node.props, None)

        node = HTMLNode("p", "text", child_nodes, {"href": "localhost"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "text")
        self.assertEqual(node.children, child_nodes)
        self.assertEqual(node.props, {"href": "localhost"})

    def test_props_to_html(self):
        node = HTMLNode("p", "text", None, {"href": "localhost", "target": "_blank"})
        props = node.props_to_html()
        expected_props = " href=\"localhost\" target=\"_blank\""
        self.assertEqual(props, expected_props)


if __name__ == "__main__":
    unittest.main()