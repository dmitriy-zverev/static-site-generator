import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_plain_constructor(self):
        node = TextNode("text", TextType.PLAIN)
        self.assertEqual(node.text, "text")
        self.assertEqual(node.text_type, TextType.PLAIN)
        self.assertEqual(node.url, None)

    def test_bold_constructor(self):
        node = TextNode("text", TextType.BOLD)
        self.assertEqual(node.text, "text")
        self.assertEqual(node.text_type, TextType.BOLD)
        self.assertEqual(node.url, None)

    def test_italic_constructor(self):
        node = TextNode("text", TextType.ITALIC)
        self.assertEqual(node.text, "text")
        self.assertEqual(node.text_type, TextType.ITALIC)
        self.assertEqual(node.url, None)

    def test_code_constructor(self):
        node = TextNode("text", TextType.CODE)
        self.assertEqual(node.text, "text")
        self.assertEqual(node.text_type, TextType.CODE)
        self.assertEqual(node.url, None)
    
    def test_link_constructor(self):
        node = TextNode("text", TextType.LINK, "https://boot.dev")
        self.assertEqual(node.text, "text")
        self.assertEqual(node.text_type, TextType.LINK)
        self.assertEqual(node.url, "https://boot.dev")

        node2 = TextNode("text", TextType.LINK)
        self.assertEqual(node2.text, "text")
        self.assertEqual(node2.text_type, TextType.LINK)
        self.assertEqual(node2.url, None)

    def test_image_constructor(self):
        node = TextNode("text", TextType.IMAGE, "https://boot.dev")
        self.assertEqual(node.text, "text")
        self.assertEqual(node.text_type, TextType.IMAGE)
        self.assertEqual(node.url, "https://boot.dev")

        node2 = TextNode("text", TextType.IMAGE)
        self.assertEqual(node2.text, "text")
        self.assertEqual(node2.text_type, TextType.IMAGE)
        self.assertEqual(node2.url, None)

    def test_other_text_type(self):
        try: 
            node = TextNode("text", "some type")
        except Exception as e:
            self.assertEqual(str(e), "Error: text_type should be a TextType object")
    
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()