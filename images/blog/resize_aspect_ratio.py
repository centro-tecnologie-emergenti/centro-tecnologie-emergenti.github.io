#!/usr/bin/env python3
"""
Image aspect ratio resizing script.
Resizes an image to match the aspect ratio of a reference image while maintaining quality.
"""

import argparse
from PIL import Image
import sys
import os

def get_image_info(image_path):
    """Get image dimensions and aspect ratio."""
    try:
        with Image.open(image_path) as img:
            return img.width, img.height, img.width / img.height
    except Exception as e:
        print(f"Error opening {image_path}: {e}")
        sys.exit(1)

def resize_to_aspect_ratio(source_path, reference_path, output_path=None, quality=95):
    """
    Resize source image to match the aspect ratio of reference image.
    
    Args:
        source_path: Path to image to resize
        reference_path: Path to reference image for aspect ratio
        output_path: Output path (optional, defaults to source_resized.jpg)
        quality: JPEG quality (1-100)
    """
    
    # Get dimensions and aspect ratios
    src_width, src_height, src_ratio = get_image_info(source_path)
    ref_width, ref_height, ref_ratio = get_image_info(reference_path)
    
    print(f"Source image: {src_width}x{src_height} (ratio: {src_ratio:.4f})")
    print(f"Reference image: {ref_width}x{ref_height} (ratio: {ref_ratio:.4f})")
    
    if abs(src_ratio - ref_ratio) < 0.001:
        print("Images already have the same aspect ratio!")
        return
    
    # Open source image
    with Image.open(source_path) as img:
        # Calculate new dimensions to match reference aspect ratio
        if ref_ratio > src_ratio:
            # Reference is wider - crop height
            new_height = int(src_width / ref_ratio)
            new_width = src_width
            # Center crop
            crop_top = (src_height - new_height) // 2
            crop_bottom = crop_top + new_height
            cropped = img.crop((0, crop_top, src_width, crop_bottom))
        else:
            # Reference is taller - crop width  
            new_width = int(src_height * ref_ratio)
            new_height = src_height
            # Center crop
            crop_left = (src_width - new_width) // 2
            crop_right = crop_left + new_width
            cropped = img.crop((crop_left, 0, crop_right, src_height))
        
        # Generate output filename if not provided
        if output_path is None:
            name, ext = os.path.splitext(source_path)
            output_path = f"{name}_resized{ext}"
        
        # Save the cropped image
        cropped.save(output_path, quality=quality, optimize=True)
        
        print(f"Resized image saved as: {output_path}")
        print(f"New dimensions: {cropped.width}x{cropped.height} (ratio: {cropped.width/cropped.height:.4f})")

def main():
    parser = argparse.ArgumentParser(description="Resize image to match aspect ratio of reference image")
    parser.add_argument("source", help="Path to image to resize")
    parser.add_argument("reference", help="Path to reference image for aspect ratio")
    parser.add_argument("-o", "--output", help="Output path (optional)")
    parser.add_argument("-q", "--quality", type=int, default=95, help="JPEG quality 1-100 (default: 95)")
    
    args = parser.parse_args()
    
    # Check if files exist
    if not os.path.exists(args.source):
        print(f"Error: Source file '{args.source}' not found")
        sys.exit(1)
    
    if not os.path.exists(args.reference):
        print(f"Error: Reference file '{args.reference}' not found")
        sys.exit(1)
    
    resize_to_aspect_ratio(args.source, args.reference, args.output, args.quality)

if __name__ == "__main__":
    main()