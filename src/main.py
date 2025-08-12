from textnode import TextNode, TextType
from htmlnode import HTMLNode
from functions import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes


def main():
    text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    text_nodes = text_to_textnodes(text)
    
    for n in text_nodes:
        print(f"|{n}|")

if __name__ == "__main__":
    main()