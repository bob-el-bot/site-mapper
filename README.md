# Site-mapper

This is a Python tool designed to generate a sitemap XML file based on HTML files found in a specified directory. It allows customization of priorities, change frequencies, and specific page priorities through a configuration file or command-line arguments.

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd sitemap-tool
   ```

## Usage

### Setup
The first time you run the `generate` command ensure you set the directory. Additionally, it is highly recommended you set the url or else it will default to `https://example.com`.

### Commands

- **Generate Sitemap:**

  Generates a sitemap XML file based on HTML files found in the specified directory.

  ```bash
  python sitemap_tool.py generate -d <directory> -u <base_url> [-v]
  ```

  Optional Arguments:
  - `-v, --verbose`: Enable verbose mode to print detailed output.

- **View Configuration:**

  Displays the current configuration settings from the `config.json` file.

  ```bash
  python sitemap_tool.py view-config
  ```

- **Set Priority:**

  Sets priority for a specific path in the sitemap.

  ```bash
  python sitemap_tool.py set-priority <path> <priority>
  ```

- **Delete Priority:**

  Deletes priority for a specific path from the configuration.

  ```bash
  python sitemap_tool.py delete-priority
  ```

- **Set Change Frequency:**

  Sets the change frequency for all URLs in the sitemap.

  ```bash
  python sitemap_tool.py set-changefreq <changefreq>
  ```

- **Set Specific Page Priority:**

  Sets priority for a specific page identified by its path.

  ```bash
  python sitemap_tool.py set-specific-priority <path> <priority>
  ```

- **Delete Specific Page Priority:**

  Deletes priority for a specific page from the configuration.

  ```bash
  python sitemap_tool.py delete-specific-priority
  ```

- **List Current Settings:**

  Displays all current configuration settings.

  ```bash
  python sitemap_tool.py list-settings
  ```

- **Help:**

  Displays usage instructions and command details.

  ```bash
  python sitemap_tool.py --help
  ```

### Examples

- Generate a sitemap for `https://example.com` using HTML files from `/path/to/directory`:

  ```bash
  python sitemap_tool.py generate -d /path/to/directory -u https://example.com
  ```

- Set priority `0.8` for path `/blog/`:

  ```bash
  python sitemap_tool.py set-priority /blog/ 0.8
  ```

- View current configuration settings:

  ```bash
  python sitemap_tool.py view-config
  ```

## Configuration File (`config.json`)

The `config.json` file contains the following configuration options:

```json
{
  "directory": "/path/to/your/default/directory",
  "base_url": "https://example.com",
  "priorities": {},
  "changefreq": "monthly",
  "specific_pages": {}
}
```

- **directory**: Default directory where HTML files are located.
- **base_url**: Base URL used to construct URLs in the sitemap.
- **priorities**: Custom priority settings for specific paths.
- **changefreq**: Default change frequency for all URLs in the sitemap.
- **specific_pages**: Specific priority settings for individual pages.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.