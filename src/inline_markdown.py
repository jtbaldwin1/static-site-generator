import re
from textnode import TextNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_img = "image"

content_test_path = "/Users/justin/self/bootdev/static_site/content/test.md"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

''' my attempt. what is different between this and the code above that works?
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = []
    for node in old_nodes:
        # Ensure we're dealing only with text type
        if node.text_type == text_type_text:
            parts = node.text.split(delimiter)
            # Iterate over parts and use alternating logic to assign types
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    new_node = TextNode(part, text_type_text)
                else:
                    new_node = TextNode(part, text_type)
                nodes.append(new_node)
        else: # Simply append non-text type nodes as-is
            nodes.append(node)
    return nodes
'''


def extract_markdown_images(text):
    #test = re.split(r"!\[(.*?)\]\((.*?)\)", text)
    pattern = r"!\[(.*?)\]\((.*?)\)"
    markdown_images = re.findall(pattern, text)
    #print(f"markdown_images is type: {type(markdown_images)}")
    #print(markdown_images)
    #for i, line in enumerate(testall):
        #print(f"index: {i}, line: {line}")
    return markdown_images 

def extract_markdown_links(text):
    pattern = r"\[(.*?)\]\((.*?)\)"
    markdown_links = re.findall(pattern, text)
    #print(f"markdown_links is type: {type(markdown_links)}")
    #print(markdown_links)
    return markdown_links

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(
                TextNode(
                    image[0],
                    text_type_img,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(link[0], text_type_link, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def extract_title(markdown):
    with open(markdown) as f:
        first_line = f.readline().strip('\n').strip()
        #print(f"first line: {first_line}")
        return first_line

