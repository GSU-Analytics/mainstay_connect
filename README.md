# MainstayConnect

MainstayConnect is a Python package designed to streamline and simplify API interactions with the Mainstay API. It provides robust methods for authenticating and retrieving data, making it easier for developers to integrate Mainstay API features into their applications.

## Features

- Simple and secure token management with keyring.
- Direct API calls to fetch contact information, campaign details, and more.
- Utility functions for converting API responses to Pandas DataFrames and saving them.

## Installation

### Using Conda

To set up a Conda environment with all dependencies pre-installed, use the `remote_install.yaml` file:

```bash
conda env create -f remote_install.yaml
conda activate mainstay_connect
```

This will install all necessary Python packages and prepare your environment to use the MainstayConnect library.

### Using pip and Git

If you prefer using pip, especially in virtual environments, you can install the package directly from GitHub:

```bash
pip install git+https://github.com/GSU-Analytics/mainstay_connect.git
```

Ensure that your environment has Python 3.10 or higher, as specified in the `remote_install.yaml`.

## Usage

Here’s a simple example of how to use MainstayConnect to test your API connection and fetch contact details:

```python
from mainstay_connect import MainstayConnect

# Create a connection instance
connector = MainstayConnect()

# Test API connection
print(connector.test_connection())

# Fetch contact by ID
print(connector.get_contact(id='123456789'))
```
See the `example.py` file for more examples of how to use the MainstayConnect library.

See the [Mainstay API documentation](https://mainstayconnect.com/docs) for more information on the available endpoints and parameters.

## Contributing

We welcome contributions from the community, whether it's improving documentation, bug fixes, or new features! Here’s how you can contribute:

1. **Fork the Repository**
   - Navigate to [GitHub repository](https://github.com/GSU-Analytics/mainstay_connect) and click the 'Fork' button.

2. **Clone the Repository**
   - After forking, clone the repository to your local machine:

     ```bash
     git clone https://github.com/YOUR_USERNAME/mainstay_connect.git
     cd mainstay_connect
     ```

3. **Create a New Branch**
   - Create a new branch for your feature or fix:

     ```bash
     git checkout -b your-branch-name
     ```

4. **Make Your Changes**
   - Make the necessary modifications or additions to the codebase.

5. **Commit Your Changes**
   - Commit your changes with a clear, descriptive message:

     ```bash
     git commit -am "Add a concise commit message describing your change"
     ```

6. **Push to GitHub**
   - Push your changes to your fork on GitHub:

     ```bash
     git push origin your-branch-name
     ```

7. **Submit a Pull Request**
   - Go to your repository on GitHub and click the ‘New pull request’ button. Select your branch and submit the pull request with a clear description of the changes.

## Support

If you encounter any problems or have any suggestions, please open an issue on the [GitHub issues page](https://github.com/GSU-Analytics/mainstay_connect/issues).

## License

The code in this repository is available under the [MIT License](https://opensource.org/licenses/MIT).