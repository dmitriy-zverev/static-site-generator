import re

from textnode import TextNode, TextType
from leafnode import LeafNode
from consts import CODE_DELIMITER, BOLD_DELIMITER, ITALIC_DELIMITER
from blocktype import BlockType

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Error: unknown text type")
        

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if old_nodes == []:
        raise Exception("Error: cannot split empty nodes")

    if text_type not in TextType:
        raise Exception("Error: text type should be a TextType object")
    
    new_nodes = []
    for old_node in old_nodes:
        new_node = old_node.text.split(delimiter)
        
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        if len(new_node) % 2 == 0:
            raise Exception("Error: cannot split nodes because of invalid syntax")

        for i in range(len(new_node)):
            if i % 2 == 1:
                new_nodes.append(TextNode(new_node[i], text_type))
            else:
                new_nodes.append(TextNode(new_node[i], old_node.text_type))
        
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    if old_nodes == []:
        raise Exception("Error: cannot split empty nodes")
    
    new_nodes = []
    for old_node in old_nodes:
        found_images = extract_markdown_images(old_node.text)
        found_images_str = list(map(lambda tpl: f"![{tpl[0]}]({tpl[1]})", found_images))

        if len(found_images) == 0 or old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        idx = 0
        for i in range(len(found_images_str)):
            cur_idx = idx + old_node.text[idx:].index(found_images_str[i])
            next_idx = cur_idx + len(found_images_str[i])
            
            new_nodes.append(
                TextNode(
                    old_node.text[idx : cur_idx],
                    TextType.TEXT,
                )
            )
            new_nodes.append(
                TextNode(
                    found_images[i][0],
                    TextType.IMAGE,
                    found_images[i][1]
                )
            )

            idx = next_idx

        if idx < len(old_node.text):
            new_nodes.append(
                TextNode(
                    old_node.text[idx : ],
                    TextType.TEXT
                )
            )
    return new_nodes


def split_nodes_link(old_nodes):
    if old_nodes == []:
        raise Exception("Error: cannot split empty nodes")
    
    new_nodes = []
    for old_node in old_nodes:
        found_images = extract_markdown_links(old_node.text)
        found_images_str = list(map(lambda tpl: f"[{tpl[0]}]({tpl[1]})", found_images))

        if len(found_images) == 0 or old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        idx = 0
        for i in range(len(found_images_str)):
            cur_idx = idx + old_node.text[idx:].index(found_images_str[i])
            next_idx = cur_idx + len(found_images_str[i])
            
            new_nodes.append(
                TextNode(
                    old_node.text[idx : cur_idx],
                    TextType.TEXT,
                )
            )
            new_nodes.append(
                TextNode(
                    found_images[i][0],
                    TextType.LINK,
                    found_images[i][1]
                )
            )

            idx = next_idx

        if idx < len(old_node.text):
            new_nodes.append(
                TextNode(
                    old_node.text[idx : ],
                    TextType.TEXT
                )
            )
    return new_nodes

def text_to_textnodes(text):
    text_node = TextNode(text, TextType.TEXT)

    return split_nodes_delimiter(
        split_nodes_delimiter(
            split_nodes_delimiter(
                split_nodes_link(
                    split_nodes_image(
                        [text_node]
                    )
                ),
                BOLD_DELIMITER,
                TextType.BOLD
            ),
            ITALIC_DELIMITER,
            TextType.ITALIC
        ),
        CODE_DELIMITER,
        TextType.CODE
    )

def markdown_to_blocks(markdown):
    return list(
        filter(
            None,
            list(
                map(
                    lambda s: s.strip(),
                    markdown.split("\n\n")
                )
            )
        )
    )
    
def block_to_block_type(block):
    if re.search(r"(?<!#)#{1,6}(?!#) (\w+)", block):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif re.search(r"(>{1}) (\w*)", block):
        return BlockType.QUOTE
    elif re.search(r"(-{1}) (\w*)", block):
        return BlockType.UNORDERED_LIST
    elif re.search(r"(\d{1}\.{1}) (\w*)", block):
        nums = list(
            map(
                lambda num: int(num[:2].replace(".", "")),
                block.split("\n")
            )
        )
        correct_order = [i for i in range(1, len(nums) + 1)]

        if nums == correct_order:
            return BlockType.ORDERED_LIST
        return BlockType.PARAGRAPH
    else:
        return BlockType.PARAGRAPH
