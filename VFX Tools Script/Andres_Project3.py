''' 
COMP 467 Project 3 VFXML
Alyssa Andres

Goal: Create the script using argparse to run via commandline
Script should be able to do each/all requests from ffmpeg:
-Watermarking (WM) - name of file
-Gif creation (GC)
-Thumbnail creation (TC) - you choose size
-Metadata export (ME)
Rename each new file processed per the request and version the number up or new file are created with v01
Ex: Bath_VFX_v01 -> Bath_VFX_v02
Ex2: gif will probably be GC_VFX_v01

Deliverables:
Run 3 commands:
1. Run individual file "Bath" with watermark only
2. Run individual file "Pirate" with watermark and thumbnail
3. Run folder with "Bath" "Pirate" and "law" in for watermark and gif creation
(3) should export metadata contents to a text file includes:
Metadata of gif
All files included in gif

'''
import argparse
import os
import re
import ffmpeg
from PIL import Image

def extract_original_version(basename): 
    match = re.search(r'_v(\d+)$', basename)
    if match:
        return int(match.group(1))
    return None

def strip_version(basename): #removes version number of file name
    return re.sub(r'_v\d+$', '', basename)

def get_next_version(folder, base_name, ext, original_version=None): #increases version number in file name
    pattern = re.compile(rf"{re.escape(base_name)}_v(\d+)\.{ext}$", re.IGNORECASE)
    versions = [
        int(match.group(1))
        for f in os.listdir(folder)
        if (match := pattern.match(f))
    ]
    if versions:
        next_version = max(versions) + 1
    else:
        if original_version is not None:
            next_version = original_version + 1
        else:
            next_version = 1
    return f"v{next_version:02d}"

#watermark
def add_watermark(input_path, output_dir):
    full_basename = os.path.splitext(os.path.basename(input_path))[0]
    base_stripped = strip_version(full_basename)
    orig_version = extract_original_version(full_basename)
    
    #renaming the file name
    wm_base = f"{base_stripped}_WM"
    version = get_next_version(output_dir, wm_base, "jpg", original_version=orig_version)
    output_path = os.path.join(output_dir, f"{wm_base}_{version}.jpg")

    #making thumbnail
    (
        ffmpeg
        .input(input_path)
        .drawtext(
            text='WATERMARK',
            fontcolor='white',
            fontsize=200,          # Large font size for good visibility
            x='(w-text_w)/2',      # Center horizontally
            y='(h-text_h)/2',      # Center vertically
            alpha=1.0              # Fully opaque watermark
        )
        .output(output_path, vframes=1)
        .overwrite_output()
        .run()
    )
    
    print(f"Watermarked image saved: {output_path}")
    return output_path

#thumbnail
def create_thumbnail(input_path, output_dir, size=(200, 200)):
    full_basename = os.path.splitext(os.path.basename(input_path))[0]
    base_stripped = strip_version(full_basename)
    orig_version = extract_original_version(full_basename)
    
    #renaming the file name
    thumb_base = f"{base_stripped}_TC"
    version = get_next_version(output_dir, thumb_base, "jpg", original_version=orig_version)
    output_path = os.path.join(output_dir, f"{thumb_base}_{version}.jpg")
    
    #open the image, create the thumbnail, and save it.
    img = Image.open(input_path)
    img.thumbnail(size)
    img.save(output_path)
    
    print(f"Thumbnail created: {output_path}")
    return output_path

#combined gif
def create_combined_gif(image_paths, output_dir):
    version = get_next_version(output_dir, "GC_VFX", "gif")
    output_path = os.path.join(output_dir, f"GC_VFX_{version}.gif")
    
    #open each image and convert them to RGB mode
    images = [Image.open(p).convert('RGB') for p in image_paths]
    #save all the images as frames in a GIF
    images[0].save(output_path, save_all=True, append_images=images[1:], duration=500, loop=0)
    
    print(f"GIF created: {output_path}")
    return output_path

#export metadata
def export_metadata(gif_path, image_paths, output_dir):
    base = os.path.splitext(os.path.basename(gif_path))[0]
    output_txt = os.path.join(output_dir, f"{base}_ME_metadata.txt")
    
    #retrieve metadata from the GIF using ffmpeg
    metadata = ffmpeg.probe(gif_path)
    with open(output_txt, "w") as f:
        f.write("GIF Metadata:\n")
        f.write(str(metadata))
        f.write("\n\nImages used in GIF:\n")
        for path in image_paths:
            f.write(f"- {os.path.basename(path)}\n")
    
    print(f"Metadata exported: {output_txt}")

#main function that has argparse functions
def main():
    parser = argparse.ArgumentParser(description="VFX Processing Tool")
    parser.add_argument('--file', help="Path to a single image file to process")
    parser.add_argument('--folder', help="Path to a folder containing multiple image files")
    parser.add_argument('--watermark', action='store_true', help="Apply watermark to the image")
    parser.add_argument('--thumbnail', action='store_true', help="Create a thumbnail of the image")
    parser.add_argument('--gif', action='store_true', help="Create a GIF from images in a folder")
    parser.add_argument('--metadata', action='store_true', help="Export GIF metadata")
    args = parser.parse_args()

    #create the output directory if it doesn't exist.
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    #process a single file if provided.
    if args.file:
        if args.watermark:
            add_watermark(args.file, output_dir)
        if args.thumbnail:
            create_thumbnail(args.file, output_dir)

    #process multiple files from a folder if provided.
    if args.folder:
        #Gather .jpg and .jpeg files from the folder
        image_paths = sorted([
            os.path.join(args.folder, f)
            for f in os.listdir(args.folder)
            if f.lower().endswith(('.jpg', '.jpeg'))
        ])

        gif_path = None
        if args.gif:
            gif_path = create_combined_gif(image_paths, output_dir)
        if args.metadata and gif_path:
            export_metadata(gif_path, image_paths, output_dir)

if __name__ == "__main__":
    main()