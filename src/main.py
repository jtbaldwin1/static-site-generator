import os, shutil, sys
from textnode import TextNode
from markdown_blocks import markdown_to_html_node
from inline_markdown import extract_title

path_root = "/Users/justin/self/bootdev/static_site/"
path_public = "/Users/justin/self/bootdev/static_site/public/"
path_public_template = "/Users/justin/self/bootdev/static_site/template.html"
path_public_index = "/Users/justin/self/bootdev/static_site/public/index.html"
path_static = "/Users/justin/self/bootdev/static_site/static/"
path_test2 = "/Users/justin/self/bootdev/static_site/test2"
path_image = "/Users/justin/self/bootdev/static_site/static/images/rivendell.png"
path_css = "/Users/justin/self/bootdev/static_site/static/index.css"
path_content = "/Users/justin/self/bootdev/static_site/content"
path_content_index = "/Users/justin/self/bootdev/static_site/content/index.md"

def main():
    content_dir = "content"
    template_file = "template.html"
    output_dir = "public"
    
    # Verify paths before invoking
    print(os.path.abspath(content_dir))
    print(os.path.abspath(template_file))
    print(os.path.abspath(output_dir))

    copy_static()
    
    # Call recursive page generation function
    #generate_pages_recursive(content_dir, template_file, output_dir)
    print("Page generation complete.")

    # Generates a page from content/index.md using template.html and write it to public/index.html
    #if not os.path.isfile(path_public_index):
        #generate_page(path_content_index, path_public_template, path_public_index)

    if not os.path.isfile(path_public_index):
        #generate_pages_recursive(path_content, path_public_template, path_public_index)
        generate_pages_recursive(path_content, path_public_template, path_public)


def copy_static():
    if os.path.isdir(path_public):
        # removes all dirs and files within the folder, but not the parent folder itself
        for root, dirs, files in os.walk(path_public, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

        # copy all files and subdirectories, nested files, etc. from static dir?
        for root, dirs, files in os.walk(path_static, topdown=False):
            #print(f"root: {root}")
            #print(f"dirs: {dirs}")
            #print(f"files: {files}")

            for name in files:
                source_path = os.path.join(root, name)
                relative_path = os.path.relpath(root, path_static)
                destination_path = os.path.join(path_public, relative_path)

                # Make sure to create the destination directory
                os.makedirs(destination_path, exist_ok=True)

                # Copy the file
                shutil.copyfile(source_path, os.path.join(destination_path, name))
                print(f"Copied file {source_path} to {os.path.join(destination_path, name)}")

            for name in dirs:
                source_dir_path = os.path.join(root, name)
                relative_path = os.path.relpath(root, path_static)
                destination_dir_path = os.path.join(path_public, relative_path)

                # Make sure to create the destination directory
                os.makedirs(destination_dir_path, exist_ok=True)
                print(f"Directory created {destination_dir_path}")                
    else:
        os.mkdir(path_public)
        print(f"Public directory created at {path_public}")

        # Removes all dirs and files within the folder, but not the parent folder itself
        for root, dirs, files in os.walk(path_public, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

        # Copy all files and subdirectories, nested files, etc. from static dir?
        for root, dirs, files in os.walk(path_static, topdown=False):
            for name in files:
                source_path = os.path.join(root, name)
                relative_path = os.path.relpath(root, path_static)
                destination_path = os.path.join(path_public, relative_path)

                # Make sure to create the destination directory
                os.makedirs(destination_path, exist_ok=True)

                # Copy the file
                shutil.copyfile(source_path, os.path.join(destination_path, name))
                print(f"Copied file {source_path} to {os.path.join(destination_path, name)}")

            for name in dirs:
                source_dir_path = os.path.join(root, name)
                relative_path = os.path.relpath(root, path_static)
                destination_dir_path = os.path.join(path_public, relative_path)

                # Make sure to create the destination directory
                os.makedirs(destination_dir_path, exist_ok=True)
                print(f"Directory created {destination_dir_path}")                


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    if not os.path.isfile(from_path):
        raise FileNotFoundError(f"Markdown file not found at path: {from_path}")
    
    if not os.path.isfile(template_path):
        raise FileNotFoundError(f"Template file not found at path: {template_path}")
    
    # Read the markdown file at from_path and store the contents in a variable
    with open(from_path) as f:
        extracted_title = extract_title(from_path)
        from_md = f.read()
        #print(f"from_md: {from_md}")

        # Use markdown_to_html_node function and .to_html() method to convert the markdown file to an HTML string
        from_md_to_html = markdown_to_html_node(from_md).to_html()

    # Read the template file at template_path and store the contents in a variable
    with open(template_path) as f:
        template_content = f.read()
        #print(f"template_content: {template_content}")

    # Replace the {{ Title }} and {{ Content }} placeholders in the template
    adjusted_template = template_content.replace("{{ Title }}", extracted_title).replace("{{ Content }}", from_md_to_html)

    # Ensure the directory for dest_path exists, then write the new full HTML page
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(adjusted_template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.isfile(template_path):
        raise FileNotFoundError(f"Template file not found at path: {template_path}")

    # Read the template content once
    with open(template_path) as f:
        template_content = f.read()

    # Walk through the directory structure
    for root, dirs, files in os.walk(dir_path_content, topdown=True):
        for file in files:
            if file.endswith(".md"):
                # Construct full path to the markdown file
                markdown_path = os.path.join(root, file)
                # Compute path relative to the source root
                relative_path = os.path.relpath(markdown_path, dir_path_content)
                # Construct path for the new HTML file in the destination directory
                new_path = os.path.join(dest_dir_path, relative_path).replace(".md", ".html")

                # Read markdown content
                with open(markdown_path) as f:
                    extracted_title = extract_title(markdown_path)
                    from_md = f.read()

                # Convert markdown to HTML
                from_md_to_html = markdown_to_html_node(from_md).to_html()

                # Replace the placeholders in the template
                adjusted_template = template_content.replace("{{ Title }}", extracted_title).replace("{{ Content }}", from_md_to_html)

                # Ensure the destination directory exists
                os.makedirs(os.path.dirname(new_path), exist_ok=True)

                # Write the new HTML file
                with open(new_path, "w") as f:
                    f.write(adjusted_template)

                print(f"Generated HTML for {markdown_path} at {new_path}")


if __name__ == "__main__":
    main()

