```markdown
# MediaBash

MediaBash is a cross-platform application built using Python's BeeWare framework. The app allows users to search for videos on VidBinge, view the results, and download videos directly to their device.

## Features

- Search for videos by entering keywords.
- Browse and view video results from VidBinge.
- Watch videos directly within the app.
- Download videos for offline viewing.

## Requirements

- Python 3.6 or higher
- [BeeWare](https://beeware.org/) (for application packaging)
- [Selenium](https://www.selenium.dev/) (for web automation)
- [WebDriver Manager](https://github.com/SergeyPirogov/webdriver_manager) (for managing browser drivers)
- [Requests](https://docs.python-requests.org/en/master/) (for downloading videos)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/mediabash.git
   cd mediabash
   ```

2. Set up a virtual environment:

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

4. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

5. Run the application in development mode using Briefcase:

   ```bash
   briefcase dev
   ```

   Alternatively, follow [BeeWare's tutorial](https://beeware.org/getting-started/) for packaging and updating your application.

## How It Works

- The application has a main window where users can initiate a search for videos.
- When a search term is entered, the app fetches results from VidBinge using Selenium.
- Users can watch videos in-app or download them for later use.
- Downloaded videos are saved in a designated `saved_videos` directory.

## Contributing

If you would like to contribute to MediaBash, please fork the repository and submit a pull request. Any contributions are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [BeeWare](https://beeware.org/) for providing the tools to build cross-platform applications.
- [Selenium](https://www.selenium.dev/) for web scraping capabilities.

## Contact

For any questions or feedback, feel free to reach out:
