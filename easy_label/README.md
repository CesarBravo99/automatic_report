# Tri-Chile Automated Report Generation

## Project Description

This repository hosts the automated report generation project for Tri-Chile, utilizing LaTeX for typesetting documents. Our goal is to streamline the daily report creation process for R.O.V. pilots, significantly reducing time and effort. The project leverages EasyLabel, a specialized web platform for precise labeling of R.O.V. images.

## Usage

Below are the instructions for using the Auto-Report and EasyLabel tools.

### EasyLabel

To launch EasyLabel, run:

```bash
./easylabel.sh
```

Then, access EasyLabel at http://127.0.0.1:8687/.

#### EasyLabel Workflow

- **Upload Images:** Navigate to the website and upload images for tagging. Images must pass a quality check for non-repetition and clarity.
- **Label Images:** Individually label each image, specifying spatial location, observations, and mark type.
- **Download Labeled Images:** Export all labeled images in .zip format.

After downloading the .zip file, upload it to the designated form for further processing.

