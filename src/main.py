from textnode import TextNode
from textnode import TextType

def main():
    node = TextNode("some text", TextType.LINK, "https://localhost:8888")
    print(node)

if __name__ == "__main__":
    main()