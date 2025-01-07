# LibGen Books Downloader

A Python tool for automated batch downloading of books from Library Genesis. This tool streamlines the process of searching and downloading multiple books by automating link generation and parallel downloads.

## Features

- **Automated Search**: Search books by keyword across multiple pages
- **Batch Processing**: Generate download links for hundreds of books in one go
- **Parallel Downloads**: Download multiple books simultaneously 
- **Resume Support**: Continue interrupted downloads from where they left off
- **Progress Tracking**: Visual progress bars and detailed logging
- **Error Handling**: Robust error handling and retry mechanisms

## How It Works

The tool operates as a two-stage process designed for efficient book downloading at scale.

### Stage 1: Link Generation

In the first stage, the tool searches Library Genesis and generates download links. Here's what happens under the hood:

1. The script takes your search term and converts it into a URL-friendly format
2. It then systematically scrapes the search results pages on Library Genesis
3. For each book found, it:
   - Extracts the initial book link
   - Follows that link to find the actual download URL
   - Validates the URL to ensure it's a valid download link
4. All valid download URLs are saved to a text file for the next stage

This stage is handled by `link_generator.py`, which creates a structured collection of direct download links.

### Stage 2: Downloading

The second stage handles the actual downloading of books, managed by `downloader.py`:

1. The script reads your previously generated list of download URLs
2. It creates a download directory if it doesn't exist
3. For each URL, the downloader:
   - Sets up proper headers to mimic browser behavior
   - Creates a connection with error handling and retries
   - Downloads the book in chunks to handle large files
   - Saves the book with its proper filename
4. The process includes:
   - Parallel downloading using multiple threads
   - Progress bars showing download status
   - Logging of successful and failed downloads
   - Error handling for network issues

## Installation

```bash
git clone https://github.com/tenlhak/libgen-downloader
cd libgen-downloader
pip install -r requirements.txt
