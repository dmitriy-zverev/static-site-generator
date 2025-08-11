from textnode import TextNode, TextType
from htmlnode import HTMLNode
from functions import split_nodes_delimiter


def main():
    node = TextNode("Some plain `with code text` and _italic_ and also **bold**. Ups a `mistake`", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    new_nodes2 = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes3 = split_nodes_delimiter(new_nodes2, "`", TextType.CODE)
    
    for i in range(len(new_nodes3)):
        print(i + 1, new_nodes3[i])

if __name__ == "__main__":
    main()