# First rename the document to input.pdf
# This scripts extracts a page from that and applies signature


import imageio.v3 as imageio
import matplotlib.pyplot as plt
import my.plot
import argparse
import subprocess
import os

def stamp(input_pdf, input_image, output_filename, left_corner, bottom_corner, 
    desired_width, 
    text=None, text_left=None, text_bottom=None, text_size=12, text_color='k',
    input_pdf_page_number=1, figsize=(8.5, 11)):
    """Stamp the file
    
    Arguments
        input_pdf : string
            Path to input file
        input_image : string
            Path to image
        output_filename : string
            Path to output file
        left_corner, bottom_corner : float
            Where to place image, as fraction of page size
        desired_width : float
            Width of placed image as fraction of page
        input_pdf_page_number : int
            Which page to extract from input_pdf
        figsize : tuple (width, height) of output file
            TODO: Extract this automatically from input file
    
    TODO: allow multi-page output (currently only the stamped page is output)
    TODO: use temporary files
    """
    # Debug input
    if not os.path.exists(input_pdf):
        raise IOError("you provided "
            "{} as an input but it does not exist".format(input_pdf))
    
    # Create a full-size figure
    f = plt.figure(figsize=figsize)

    # Load signature image and calculate its size and aspect ratio
    sig = imageio.imread(input_image)
    sig_height = sig.shape[0]
    sig_width = sig.shape[1]
    sig_aspect = sig_width / float(sig_height)

    # Add an axis to the figure
    # This specifies left and bottom coords
    ax = f.add_axes(
        [left_corner, bottom_corner, 
        desired_width, desired_width / sig_aspect])
    ax.imshow(sig)
    my.plot.despine(ax, which=('left', 'bottom', 'top', 'right'), detick=True)
    ax.set_xticks([])
    ax.set_yticks([])

    # Write text
    if text is not None:
        print("I got {}".format(text))
        f.text(text_left, text_bottom, text, size=text_size, color=text_color)
    else:
        print("no text")

    # Save as a temporary file which will be used as a stamp
    f.savefig('stamp.pdf', transparent=True)
    
    # This extracts the page to sign
    subprocess.check_output([
        'pdftk', input_pdf, 
        'cat', str(input_pdf_page_number), 
        'output', 'page_to_stamp.pdf'
        ])

    # This stamps it
    subprocess.check_output([
        'pdftk', 'page_to_stamp.pdf', 
        'stamp', 'stamp.pdf', 
        'output', output_filename,
        ])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='stamp the pdf with the image')
    parser.add_argument(
        '-i', '--input', required=True,
        help='the filename of the input pdf')
    parser.add_argument(
        '-o', '--output', required=True,
        help='the filename to write as the output pdf',
        )
    parser.add_argument(
        '-s', '--image', required=True,
        help='the filename of the image to stamp',
        )
    parser.add_argument(
        '-l', '--left', required=True, type=float,
        help='the position of the left side of the stamped image (fraction of page width)',
        )
    parser.add_argument(
        '-b', '--bottom', required=True, type=float,
        help='the position of the bottom side of the stamped image (fraction of page height)',
        )
    parser.add_argument(
        '-w', '--width', required=True, type=float,
        help='the width of the stamped image (fraction of page width)',
        )
    parser.add_argument(
        '--text', 
        help='additional text to write',
        )
    parser.add_argument(
        '--text_left', type=float,
        help='left position of additional text (fraction of page width)',
        )
    parser.add_argument(
        '--text_bottom', type=float,
        help='bottom position of additional text (fraction of page height)',
        )
    parser.add_argument(
        '--text_size', type=float, default=12,
        help='font size of additional text',
        )
    parser.add_argument(
        '--text_color', default='black',
        help='color of additional text',
        )
    parser.add_argument(
        '-p', '--page', type=int,
        help='the page number to use from the input pdf',
        default=1,
        )

    args = parser.parse_args()
    stamp(
        input_pdf=args.input, 
        input_image=args.image, 
        output_filename=args.output, 
        left_corner=args.left, 
        bottom_corner=args.bottom, 
        desired_width=args.width, 
        text=args.text,
        text_left=args.text_left,
        text_bottom=args.text_bottom,
        text_size=args.text_size,
        text_color=args.text_color,
        input_pdf_page_number=args.page, 
        figsize=(8.5, 11),
        )    
    
    print("stamped output written to {}".format(args.output))