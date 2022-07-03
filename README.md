# What is Browsable Web Directory?

Web servers may register to list the contents of directories that do not have an index page. In this case, threat actors can quickly obtain data about the target. These files can be sensitive files, important information about the company, and password information.


## How Does BrowsableFinder Work?

BrowsableFinder tries to extract the paths in the "link", "script" and "img" tags from the websites given by the user, one by one, and prints the result to the screen.

## Installation

First you need to install the libraries in the requirements file.

```pip install -r requirements```

Then BrowsableFinder is ready to use.

## Usage

```python3 BrowsableFinder.py -f url.txt```

Note: The urls in url.txt must start with http or https.


> Thanks to Faruk and Kaan for their help.
