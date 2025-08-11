from textnode import TextNode, TextType
from htmlnode import HTMLNode


def main():
    node = HTMLNode("p", "some text", props={"href": "https://www.google.com", "target": "_blank",})
    # node = HTMLNode("p", "some text")
    print(node)

if __name__ == "__main__":
    main()