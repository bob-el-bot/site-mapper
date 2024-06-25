import os
import sys
import json
import xml.etree.ElementTree as ET
from urllib.parse import urljoin
from datetime import datetime

CONFIG_FILE = 'config.json'

def load_config(config_file):
    if not os.path.exists(config_file):
        # Create a default configuration if the file doesn't exist
        default_config = {
            "directory": "/path/to/your/default/directory",
            "base_url": "https://example.com",
            "priorities": {},
            "changefreq": "monthly",
            "specific_pages": {}
        }
        save_config(default_config, config_file)
        return default_config
    with open(config_file, 'r') as file:
        return json.load(file)

def save_config(config, config_file):
    with open(config_file, 'w') as file:
        json.dump(config, file, indent=4)

def generate_sitemap(directory=None, base_url=None, verbose=False):
    try:
        config = load_config(CONFIG_FILE)

        if directory is None:
            directory = config.get('directory', None)
        if base_url is None:
            base_url = config.get('base_url', None)

        if directory is None or base_url is None:
            print("Please provide both -d <directory> and -u <base_url> arguments or ensure they are set in the config file.")
            sys.exit(1)

        urlset = ET.Element(
            "urlset", 
            xmlns="http://www.sitemaps.org/schemas/sitemap/0.9",
            attrib={
                "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                "xsi:schemaLocation": "http://www.sitemaps.org/schemas/sitemap/0.9 "
                                      "http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd"
            }
        )

        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(('.html', '.htm')):
                    filepath = os.path.join(root, file)
                    rel_path = os.path.relpath(filepath, directory).replace(os.sep, '/')
                    url = urljoin(base_url, rel_path)
                    
                    url_element = ET.Element("url")
                    loc = ET.SubElement(url_element, "loc")
                    loc.text = url

                    lastmod = ET.SubElement(url_element, "lastmod")
                    lastmod.text = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d')

                    urlset.append(url_element)
                    
                    if verbose:
                        print(f"Added {url}")

        # Determine where to write the sitemap.xml file
        output_dir = config.get('directory', None)
        if output_dir:
            output_path = os.path.join(output_dir, 'sitemap.xml')
        else:
            output_path = 'sitemap.xml'

        tree = ET.ElementTree(urlset)
        tree.write(output_path, xml_declaration=True, encoding='utf-8', method="xml")
        print(f"Sitemap generated successfully at {output_path}")

    except FileNotFoundError as e:
        print(f"Configuration file {CONFIG_FILE} not found: {e}")
    except Exception as e:
        print(f"Error generating sitemap: {e}")


    except FileNotFoundError as e:
        print(f"Configuration file {CONFIG_FILE} not found: {e}")
    except Exception as e:
        print(f"Error generating sitemap: {e}")

def view_config(config_file):
    try:
        config = load_config(config_file)
        print(json.dumps(config, indent=4))
    except Exception as e:
        print(f"Error viewing config: {e}")

def add_priority(path, priority, config_file):
    try:
        config = load_config(config_file)
        if path in config['priorities']:
            print(f"Priority for path '{path}' already exists. Updating priority to {priority}.")
        config['priorities'][path] = priority
        save_config(config, config_file)
        print(f"Added priority {priority} for path {path}.")
    except Exception as e:
        print(f"Error adding priority: {e}")

def delete_priority(path_index, config_file):
    try:
        config = load_config(config_file)
        priorities = config['priorities']
        if path_index >= 0 and path_index < len(priorities):
            path = list(priorities.keys())[path_index]
            del priorities[path]
            save_config(config, config_file)
            print(f"Deleted priority for path '{path}'.")
        else:
            print("Invalid path index.")
    except Exception as e:
        print(f"Error deleting priority: {e}")

def edit_changefreq(changefreq, config_file):
    try:
        config = load_config(config_file)
        config['changefreq'] = changefreq
        save_config(config, config_file)
        print(f"Set changefreq to {changefreq}.")
    except Exception as e:
        print(f"Error editing changefreq: {e}")

def add_specific_page(path, priority, config_file):
    try:
        config = load_config(config_file)
        if 'specific_pages' not in config:
            config['specific_pages'] = {}

        if path in config['specific_pages']:
            print(f"Specific priority for page '{path}' already exists. Updating priority to {priority}.")
        config['specific_pages'][path] = priority
        save_config(config, config_file)
        print(f"Added specific priority {priority} for page {path}.")
    except Exception as e:
        print(f"Error adding specific page priority: {e}")

def delete_specific_page(path_index, config_file):
    try:
        config = load_config(config_file)
        specific_pages = config.get('specific_pages', {})
        if path_index >= 0 and path_index < len(specific_pages):
            path = list(specific_pages.keys())[path_index]
            del specific_pages[path]
            save_config(config, config_file)
            print(f"Deleted specific page priority for path '{path}'.")
        else:
            print("Invalid path index or no specific page priorities.")
    except Exception as e:
        print(f"Error deleting specific page priority: {e}")

def list_settings(config_file):
    try:
        config = load_config(config_file)
        print("Current settings:")
        print(f"Priorities: {config['priorities']}")
        print(f"Change Frequency: {config['changefreq']}")
        print(f"Specific Page Priorities: {config['specific_pages']}")
    except Exception as e:
        print(f"Error listing settings: {e}")

def print_help():
    print("Usage: sitemap_tool.py <command> [<args>]")
    print("\nCommands:")
    print("  generate             Generate sitemap")
    print("    -d, --directory <directory>   Specify the directory to scan for HTML files")
    print("    -u, --url <base_url>          Specify the base URL for the sitemap")
    print("    -v, --verbose        Verbose mode")
    print("  view-config          View current configuration")
    print("  set-priority <path> <priority> Set priority for a specific path")
    print("  delete-priority      Delete priority for a specific path")
    print("  set-changefreq <changefreq>   Set change frequency")
    print("  set-specific-priority <path> <priority> Set priority for a specific page")
    print("  delete-specific-priority      Delete priority for a specific page")
    print("  list-settings        List current settings")

def main():
    if len(sys.argv) < 2 or sys.argv[1] == '--help':
        print_help()
        sys.exit(1)

    command = sys.argv[1]

    if command == 'generate':
        try:
            config = load_config(CONFIG_FILE)
            
            directory = config.get('directory', None)
            base_url = config.get('base_url', None)

            # Check for optional arguments to set directory and base_url
            if '-d' in sys.argv:
                directory_index = sys.argv.index('-d')
                directory = sys.argv[directory_index + 1]
                config['directory'] = directory
            if '--directory' in sys.argv:
                directory_index = sys.argv.index('--directory')
                directory = sys.argv[directory_index + 1]
                config['directory'] = directory
            if '-u' in sys.argv:
                base_url_index = sys.argv.index('-u')
                base_url = sys.argv[base_url_index + 1]
                config['base_url'] = base_url
            if '--url' in sys.argv:
                base_url_index = sys.argv.index('--url')
                base_url = sys.argv[base_url_index + 1]
                config['base_url'] = base_url

            verbose = '-v' in sys.argv or '--verbose' in sys.argv

            # Save updated configuration back to file
            save_config(config, CONFIG_FILE)

            generate_sitemap(directory, base_url, verbose)
        except Exception as e:
            print(f"An error occurred during generation: {e}")

    elif command == 'view-config':
        view_config(CONFIG_FILE)

    elif command == 'set-priority':
        try:
            if len(sys.argv) != 4:
                print("Usage: sitemap_tool.py set-priority <path> <priority>")
                sys.exit(1)
            path = sys.argv[2]
            priority = sys.argv[3]
            add_priority(path, priority, CONFIG_FILE)
        except Exception as e:
            print(f"Error setting priority: {e}")

    elif command == 'delete-priority':
        try:
            config = load_config(CONFIG_FILE)
            priorities = config['priorities']
            print("Current priorities:")
            for i, path in enumerate(priorities.keys()):
                print(f"{i}: {path}")
            if len(priorities) > 0:
                path_index = int(input(f"Enter the number corresponding to the path to delete (0-{len(priorities)-1}): "))
                delete_priority(path_index, CONFIG_FILE)
            else:
                print("No priorities to delete.")
        except Exception as e:
            print(f"Error deleting priority: {e}")

    elif command == 'set-changefreq':
        try:
            if len(sys.argv) != 3:
                print("Usage: sitemap_tool.py set-changefreq <changefreq>")
                sys.exit(1)
            changefreq = sys.argv[2]
            edit_changefreq(changefreq, CONFIG_FILE)
        except Exception as e:
            print(f"Error setting changefreq: {e}")

    elif command == 'set-specific-priority':
        try:
            if len(sys.argv) != 4:
                print("Usage: sitemap_tool.py set-specific-priority <path> <priority>")
                sys.exit(1)
            path = sys.argv[2]
            priority = sys.argv[3]
            add_specific_page(path, priority, CONFIG_FILE)
        except Exception as e:
            print(f"Error setting specific page priority: {e}")

    elif command == 'delete-specific-priority':
        try:
            config = load_config(CONFIG_FILE)
            specific_pages = config.get('specific_pages', {})
            print("Current specific page priorities:")
            for i, path in enumerate(specific_pages.keys()):
                print(f"{i}: {path}")
            if len(specific_pages) > 0:
                path_index = int(input(f"Enter the number corresponding to the specific page path to delete (0-{len(specific_pages)-1}): "))
                delete_specific_page(path_index, CONFIG_FILE)
            else:
                print("No specific page priorities to delete.")
        except Exception as e:
            print(f"Error deleting specific page priority: {e}")

    elif command == 'list-settings':
        try:
            list_settings(CONFIG_FILE)
        except Exception as e:
            print(f"Error listing settings: {e}")

    else:
        print("Invalid command. Use 'sitemap_tool.py --help' for usage.")

if __name__ == "__main__":
    main()
