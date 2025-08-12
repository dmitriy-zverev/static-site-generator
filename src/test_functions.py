import unittest

from functions import (
    text_node_to_html_node, 
    split_nodes_delimiter, 
    extract_markdown_images, 
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
)
from textnode import TextNode, TextType
from consts import CODE_DELIMITER, ITALIC_DELIMITER, BOLD_DELIMITER

class TestFunctions(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://localhost:8888")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props["href"], "https://localhost:8888")

    def test_link_no_url(self):
        node = TextNode("This is a link node", TextType.LINK)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props["href"], None)
    
    def test_img(self):
        node = TextNode(
            "This is an image node", 
            TextType.IMAGE, 
            "https://localhost:8888"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "https://localhost:8888")
        self.assertEqual(html_node.props["alt"], "This is an image node")
    
    def test_img_no_url(self):
        node = TextNode(
            "This is an image node", 
            TextType.IMAGE
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], None)
        self.assertEqual(html_node.props["alt"], "This is an image node")

    def test_split_bolds(self):
        node = TextNode("Text **bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], BOLD_DELIMITER, TextType.BOLD)
        expected_nodes = [
            TextNode("Text ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_italic(self):
        node = TextNode("Text _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], ITALIC_DELIMITER, TextType.ITALIC)
        expected_nodes = [
            TextNode("Text ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode("", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_code(self):
        node = TextNode("Text `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], CODE_DELIMITER, TextType.CODE)
        expected_nodes = [
            TextNode("Text ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_multiple_types(self):
        node = TextNode("Text `code` and _italic_ and **some bold**", TextType.TEXT)

        new_nodes = split_nodes_delimiter([node], CODE_DELIMITER, TextType.CODE)
        new_nodes2 = split_nodes_delimiter(new_nodes, ITALIC_DELIMITER, TextType.ITALIC)
        new_nodes3 = split_nodes_delimiter(new_nodes2, BOLD_DELIMITER, TextType.BOLD)

        expected_nodes = [
            TextNode("Text ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("some bold", TextType.BOLD),
            TextNode("", TextType.TEXT),
        ]
        self.assertEqual(new_nodes3, expected_nodes)

    def test_split_error_syntax(self):
        node = TextNode("Text **with some", TextType.TEXT)
        try:
            split_nodes_delimiter([node], BOLD_DELIMITER, TextType.BOLD)
        except Exception as e:
            self.assertEqual(str(e), "Error: cannot split nodes because of invalid syntax")

    def test_split_error_empty_nodes(self):
        try:
            split_nodes_delimiter([], BOLD_DELIMITER, TextType.BOLD)
        except Exception as e:
            self.assertEqual(str(e), "Error: cannot split empty nodes")
        
    def test_split_error_other_text_type(self):
        node = TextNode("Text **with** some", TextType.TEXT)
        try:
            split_nodes_delimiter([node], BOLD_DELIMITER, "not known text type")
        except Exception as e:
            self.assertEqual(str(e), "Error: text type should be a TextType object")

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_nothing(self):
        matches = extract_markdown_images(
            "This is text without images"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link text](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link text", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links_nothing(self):
        matches = extract_markdown_links(
            "This is text without links"
        )
        self.assertListEqual([], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_multiple_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_with_nothing(self):
        node = TextNode(
            "This is text without images",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_multiple_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links_with_nothing(self):
        node = TextNode(
            "This is text without images",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_multiple_links_and_images(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png). Also here's an ![image](https://i.imgur.com/zjjcdfa.png) with second ![second image](https://i.imgur.com/zjfaaKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link(split_nodes_image([node]))
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(". Also here's an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcdfa.png"),
                TextNode(" with second ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/zjfaaKZ.png"
                ),
            ],
            new_nodes,
        )

    def test_text_to_textnode(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text_nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            text_nodes
        )
    
    def test_text_to_textnode_with_nothing(self):
        text = "This is text with an italic word and a code block"
        text_nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("This is text with an italic word and a code block", TextType.TEXT),
            ],
            text_nodes
        )