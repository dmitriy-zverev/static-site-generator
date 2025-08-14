import re
import os
import shutil

from textnode import TextNode, TextType
from leafnode import LeafNode
from htmlnode import HTMLNode
from blocktype import BlockType
from consts import (
    CODE_DELIMITER, 
    BOLD_DELIMITER, 
    ITALIC_DELIMITER,
    TITLE_PLACEHOLDER,
    CONTENT_PLACEHOLDER,
)

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
            if i % 2 == 1 and new_node[i] != "":
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
    elif block.startswith("```") and block.endswith("```") and len(block) >= 6:
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


def markdown_to_html_node(markdown):
    if markdown == "":
        raise Exception("Error: cannot convert empty .md file")
    
    blocks = markdown_to_blocks(markdown)

    html_blocks = HTMLNode("div", "")

    for block in blocks:
        html_block = block_to_html_node(block)
        html_blocks.children.append(html_block)
    
    return html_blocks


def text_nodes_to_html_children(text_nodes):
    return list(
        map(
            lambda node: text_node_to_html_node(node),
            text_nodes
        )
    )

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    html_block = None

    match block_type:
            case BlockType.PARAGRAPH:
                html_block = HTMLNode("p", "")
                html_block.children = text_nodes_to_html_children(text_to_textnodes(" ".join(block.split("\n"))))

            case BlockType.HEADING:
                first_space = block.index(" ")
                hashtags_count = block[:first_space].count("#")
                
                node = HTMLNode(None, "", text_nodes_to_html_children(text_to_textnodes(block.strip("#").strip(" "))))
                h_node = LeafNode(None, node.with_children())

                html_block = HTMLNode("h" + str(hashtags_count), "")
                html_block.children.append(h_node)

            case BlockType.CODE:
                html_block = HTMLNode("pre", "")
                html_block.children.append(LeafNode("code", block.strip(CODE_DELIMITER).strip("\n")))

            case BlockType.UNORDERED_LIST:
                html_block = HTMLNode("ul", "")

                ul_items = list(
                    map(
                        lambda item: item.strip("- "),
                        block.split("\n")
                    )
                )

                for ul_item in ul_items:
                    node = HTMLNode(None, "", text_nodes_to_html_children(text_to_textnodes(ul_item)))
                    li_node = LeafNode("li", node.with_children())
                    html_block.children.append(li_node)

            case BlockType.ORDERED_LIST:
                html_block = HTMLNode("ol", "")
                ol_items = list(
                    map(
                        lambda item: item[item.index(".") + 1 : ].strip(" "),
                        block.split("\n")
                    )
                )
                for ol_item in ol_items:
                    node = HTMLNode(None, "", text_nodes_to_html_children(text_to_textnodes(ol_item)))
                    li_node = LeafNode("li", node.with_children())
                    html_block.children.append(li_node)

            case BlockType.QUOTE:
                leaf_nodes = list(
                    map(
                        lambda b: LeafNode(None, b.strip(">").strip(" ") + "\n"),
                        block.split("\n")
                    )
                )

                html_block = HTMLNode("blockquote", "")
                html_block.children.extend(leaf_nodes)

            case _:
                raise Exception("Error: unknown block type in .md file")
        
    html_block.value = html_block.with_children()

    return html_block


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        if block.startswith("# "):
            return block[1 : ].strip()
    
    raise Exception("Error: there is no title in .md file")


def copy_from_public_to_static(from_dir, to_dir):
    static_dir = os.path.abspath(from_dir)

    if os.path.exists(os.path.abspath(to_dir)):
        shutil.rmtree(os.path.abspath(to_dir))

    os.mkdir(os.path.abspath(to_dir))

    public_dir = os.path.abspath(to_dir)
    static_content = os.listdir(static_dir)

    for content in static_content:
        static_file_path = os.path.join(static_dir, content)
        if os.path.isfile(static_file_path):
            public_file_path = os.path.join(public_dir, content)
            shutil.copy(static_file_path, public_file_path)
        else:
            copy_from_public_to_static(
                static_file_path,
                os.path.join(public_dir, content)
            )


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        file_content = f.read()
    
    with open(template_path) as f:
        template_content = f.read()

    html_content = markdown_to_html_node(file_content).to_html()
    html_title = extract_title(file_content)

    template_content = template_content.replace(
        TITLE_PLACEHOLDER,
        html_title
    )

    template_content = template_content.replace(
        CONTENT_PLACEHOLDER,
        html_content
    )

    template_content = template_content.replace(
        "href=\"/",
        f"href=\"{basepath}"
    )

    template_content = template_content.replace(
        "src=\"/",
        f"src=\"{basepath}"
    )

    if not os.path.exists(os.path.abspath(dest_path)):
        dest_dirs = dest_path.split("/")

        if len(dest_dirs) > 1:
            dest_dirs = os.path.abspath("/".join(dest_dirs[ : -1]))

            if not os.path.exists(dest_dirs):
                os.makedirs(dest_dirs)
    
    abs_path_to_page = os.path.abspath(dest_path)

    with open(abs_path_to_page, "a") as f:
        f.write(template_content)


def generate_pages_recursively(dir_path_content, template_path, dest_dir_path, basepath):
    abs_content_path = os.path.abspath(dir_path_content)
    abs_template_path = os.path.abspath(template_path)
    abs_dir_path = os.path.abspath(dest_dir_path)

    content_list = os.listdir(abs_content_path)

    for content in content_list:
        new_content_path = os.path.join(abs_content_path, content)
        new_dest_content_path = os.path.join(abs_dir_path, content)
        
        if os.path.isdir(new_content_path):
            generate_pages_recursively(new_content_path, abs_template_path, new_dest_content_path, basepath)
        
        if os.path.isfile(new_content_path):
            generate_page(new_content_path, abs_template_path, new_dest_content_path.replace(".md", ".html"), basepath)