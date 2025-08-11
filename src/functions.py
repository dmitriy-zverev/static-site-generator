from textnode import TextNode, TextType
from leafnode import LeafNode

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