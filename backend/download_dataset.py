#!/usr/bin/env python3
"""
NBA Dataset Downloader and Processor
Downloads the NBA dataset from Kaggle and prepares it for PostgreSQL import.
"""

import os
import pandas as pd
import kagglehub
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def download_nba_dataset():
    """Download the NBA dataset from Kaggle."""
    try:
        logger.info("Downloading NBA dataset from Kaggle...")
        path = kagglehub.dataset_download("patrickhallila1994/nba-data-from-basketball-reference")
        logger.info(f"Dataset downloaded to: {path}")
        return path
    except Exception as e:
        logger.error(f"Failed to download dataset: {e}")
        raise

def explore_dataset(dataset_path):
    """Explore the dataset structure and return file information."""
    dataset_dir = Path(dataset_path)
    files = list(dataset_dir.glob("**/*"))
    
    logger.info("Dataset structure:")
    for file_path in files:
        if file_path.is_file():
            logger.info(f"  {file_path.relative_to(dataset_dir)}")
    
    return files

def process_csv_files(dataset_path, output_dir="processed_data"):
    """Process CSV files and prepare them for database import."""
    dataset_dir = Path(dataset_path)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    csv_files = list(dataset_dir.glob("**/*.csv"))
    processed_files = []
    
    logger.info(f"Found {len(csv_files)} CSV files to process")
    
    for csv_file in csv_files:
        try:
            logger.info(f"Processing {csv_file.name}...")
            
            # Read the CSV file
            df = pd.read_csv(csv_file)
            
            # Basic data cleaning
            df = df.dropna(how='all')  # Remove completely empty rows
            
            # Clean column names (remove spaces, special characters)
            df.columns = df.columns.str.replace(' ', '_').str.replace('[^a-zA-Z0-9_]', '', regex=True)
            df.columns = df.columns.str.lower()
            
            # Save processed file
            output_file = output_path / f"processed_{csv_file.name}"
            df.to_csv(output_file, index=False)
            processed_files.append(output_file)
            
            logger.info(f"  - Shape: {df.shape}")
            logger.info(f"  - Columns: {list(df.columns)}")
            logger.info(f"  - Saved to: {output_file}")
            
        except Exception as e:
            logger.error(f"Error processing {csv_file.name}: {e}")
            continue
    
    return processed_files

def main():
    """Main function to download and process the NBA dataset."""
    try:
        # Download dataset
        dataset_path = download_nba_dataset()
        
        # Explore dataset structure
        files = explore_dataset(dataset_path)
        
        # Process CSV files
        processed_files = process_csv_files(dataset_path)
        
        logger.info(f"Processing complete! {len(processed_files)} files processed.")
        logger.info("Processed files are ready for database import.")
        
        return dataset_path, processed_files
        
    except Exception as e:
        logger.error(f"Script failed: {e}")
        raise

if __name__ == "__main__":
    main()
