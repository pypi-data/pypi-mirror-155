# Plasmid_render
CLI tool to illustrate plasmids with a structure described by json.

![Example Image](/test/SVG.svg)

This program is a CLI tool that can describe the plasmid structure in json and output it as an image in SVG format.  

The output is in vector format, so there is no possibility of poor quality images being output.

## Usage

### Prerequisites
- Python3

### Download
Download the code with git clone.

```
git clone https://github.com/strelka145/Plasmid_render.git
cd Plasmid_render
```

### Json file notation

![Example Image](/test/SVG.svg)

If you want to draw a plasmid like the one shown in the figure, you can write a json like this.

```json
[
  {"type":"arrow","angle":"10","label":"primer","color":"black"},
  {"type":"space","angle":"10"},
  {"type":"tag","angle":"45","label":"EGFP","color":"green"},
  {"type":"space","angle":"10"},
  {"type":"arrow","angle":"-10","label":"primer","color":"black"},
  {"type":"space","angle":"20"},
  {"type":"tag","angle":"60","label":"RFP","color":"red"},
  {"type":"tag","angle":"60","label":"BFP","color":"#1E90FF"},
  {"type":"space","angle":"30"},
  {"type":"line","angle":"45","label":"BamHI","color":"black"}
]
```

`type`  
If the value of `type` is "tag", a annular sector is drawn; if it is "space", nothing is drawn and a space is opened at the angle specified by `angle`.  
If `space` is not described between `tag` as shown between RFP and BFP in the example of json, `{"type":"space","angle":"5"}` is automatically inserted. If you do not want gaps between the annular sectors, write `{"type": "space", "angle": "0"}`.  

`angle`  
Central angle of an annular sector or a gap. Specify the value using the degree method, NOT the radian method.

`label`  
Text of an annular sector.

`color`  
Color of an annular sector.

### SVG output from json files

```
python3 main.py -i (Path of input json file) --output_svg_file (Path of output svg file)
```

### SVG output from json string

```
python3 main.py --input_json (json code) --output_svg_file (Path of output svg file)
```

### Output as png format

```
python3 main.py -i (Path of input json file) --output_png_file (Path of output png file)
```


### Future
- To be able to change the text style
- Allow the hight of a annular sector to be changed
- Allow adjustable line thickness

### More future
- Restriction Enzyme Indication
- Show primer
- Show translation direction
