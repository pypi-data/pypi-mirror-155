from argparse import ArgumentParser
from . import main
import json
import sys


def get_option():
    argparser = ArgumentParser()
    argparser.add_argument('-i', '--input_file',help='Path of input json file')
    argparser.add_argument('--input_json',default="[]",help='Input json text')
    argparser.add_argument('-os', '--output_svg_file',help='Path of output svg file')
    argparser.add_argument('-op', '--output_png_file',help='Path of output svg file')

    argparser.add_argument('-cp','--config_path',help='Configuration file path')
    argparser.add_argument('--picture_box',type=float,default=500,help='Size of output image (length of one side of a square)')
    argparser.add_argument('-r','--radius',type=float,default=180,\
                            help='Plasmid radius, which automatically determines the size of the image.')
    argparser.add_argument('-pw','--plasmid_width',type=float,default=2.5,\
                            help='Width of plasmid line')
    argparser.add_argument('-th','--tag_height',type=float,default=20,\
                            help='Height of tag(an annular sector)')
    argparser.add_argument('-tl','--tag_line_width',type=float,default=1,\
                            help='Tag(an annular sector) outline thickness')
    argparser.add_argument('-cll','--cut_line_length',type=float,default=20,\
                            help='Length of a cut line')
    argparser.add_argument('-clt','--cut_line_thickness',type=float,default=2.5,\
                            help='Thickness of a cut line')
    argparser.add_argument('--arrow_size',type=float,default=10,\
                            help='Size of an arrow')
    argparser.add_argument('--arrow_radius',type=float,default=200,\
                            help='Arrow radius')
    argparser.add_argument('--arrow_thickness',type=float,default=2,\
                            help='Arrow line thickness')
    argparser.add_argument('--font',help='Font name')
    argparser.add_argument('--font_size',type=float,default=16,help='Font size')
    argparser.add_argument('--rotation_angle',type=float,default=-90,\
                            help='Angle of rotation')


    return argparser.parse_args()

def option_json(json_path):
    with open(json_path,mode="r") as f:
        config_dic = json.load(f)
    for key in config_dic.keys():
        if key=="input_file":
            if not("--input_file" in sys.argv) and not("-i" in sys.argv):
                arguments.input_file=config_dic[key]
        elif key=="input_json":
            if not("--input_json" in sys.argv):
                arguments.input_file=config_dic[key]
        elif key=="output_svg_file":
            if not("--output_svg_file" in sys.argv) and not("-os" in sys.argv):
                arguments.output_svg_file=config_dic[key]
        elif key=="output_png_file":
            if not("--output_png_file" in sys.argv) and not("-op" in sys.argv):
                arguments.output_png_file=config_dic[key]
        elif key=="config_path":
            if not("--config_path" in sys.argv) and not("-cp" in sys.argv):
                arguments.config_path=config_dic[key]
        elif key=="margin":
            if not("--margin" in sys.argv):
                arguments.margin=float(config_dic[key])
        elif key=="radius":
            if not("--radius" in sys.argv):
                arguments.radius=float(config_dic[key])
        elif key=="plasmid_width":
            if not("--plasmid_width" in sys.argv) and not("-pw" in sys.argv):
                arguments.plasmid_width=float(config_dic[key])
        elif key=="tag_height":
            if not("--tag_height" in sys.argv) and not("-th" in sys.argv):
                arguments.tag_height=float(config_dic[key])
        elif key=="tag_line_width":
            if not("--tag_line_width" in sys.argv) and not("-tl" in sys.argv):
                arguments.tag_line_width=float(config_dic[key])
        elif key=="font":
            if not("--font" in sys.argv):
                arguments.font=config_dic[key]
        elif key=="font_size":
            if not("--font_size" in sys.argv):
                arguments.font_size=float(config_dic[key])



class arguments(object):
    """docstring forarguments."""
    input_file=None
    input_json=None
    output_svg_file=None
    output_png_file=None
    config_path=None
    picture_box=500.0
    radius=180.0
    plasmid_width=2.5
    tag_height=20
    tag_line_width=1.0
    cut_line_length=20.0
    cut_line_thickness=2.5
    arrow_size=10.0
    arrow_radius=200.0
    arrow_thickness=2.0
    font=None
    font_size=16.0
    rotation_angle=-90.0
