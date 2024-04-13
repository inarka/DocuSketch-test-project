# Room Corners Deviation Analysis Plotting Tool

## Overview

This project is designed to visualize the deviations of floor vs ceiling corners and degrees of a model against ground truth labels. 

## Features

- Reads JSON data to extract model performance metrics.
- Generates plots (histograms, boxplots, scatter plots, etc) comparing different statistical columns.
- Saves generated plots in a designated directory.
- Provides a Jupyter notebook for an interactive visualization and analysis experience.

## Installation

### Prerequisites

- Python 3.8+
- pip
- Virtual environment 

### Setup

 1. Clone the repository:
 ```bash
 git clone https://github.com/inarka/DocuSketch-test-project.git
 cd DocuSketch-test-project
 ```
   
2. Create and active a virtual environment:
```bash
python -m venv venv
```
- On Windows:
```bash
.\venv\Scripts\activate
```
- On macOS and Linux:
```bash
source venv/bin/activate
```
   
3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Jupyter notebook to interact with the plots and analyze the data:
```bash
jupyter notebook Notebook.ipynb
```
