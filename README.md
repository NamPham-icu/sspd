# sspd 

### 20250614-MCS8A-plotting.py

This code gets the data from MPANT, analyzes, and plots a graph.
The file from MPANT must be in .txt format. First, from "File", go to "Save Display As...".
Then, select "ASCII File (*M.P)" as file type.

Next, put the saved data file to the same directory as this code. 
Otherwise, you have to explicitly instruct the directory path in this code.

After that, run this code. You will get a graph of times vs counts, with peaks marked as 'x'.
You also obtain the time difference between those peaks.

Other than that, this code stores every parameters in the saved data file in .parameters DataFrame.
You can modify the code to obtain these informations.

You can change the font by un-lining out the plt.rcParams[]. 
There are cases the OS does not have the font.
In that case, you must see the "Import Fonts".

### 20250614-Oscilloscope-plotting.py

This code gets the data from Keysight Oscilloscope, visualize the data, and perform a damping oscillation curve fitting.
This code is meant to analyze the pulse ringing in a pulse waveform, which is caused by unmatching circuit impedance.

First, the file must be in .csv file format. First, on Keysight I/O Interaction, acquire data by giving SCPI commands as below:

```
:WAV:SOUR CHAN1
:WAV:MODE NORM
:WAV:FORM ASCii
:WAV:XINC?
:WAV:YINC?
:WAV:DATA?   
```

Next, copy the response of `:WAV:DATA?` and save into a .csv file.

Then, you can start working on the code.
Save the data file to the same directory as this code.
Otherwise you have to explocitly indicate the directory path in this code.

Then, run the code.
You will get a raw plotted graph.

If you want to proceed to curve fit, first you have to manually extract the analyzing interval.
The code will ask you the starting id and ending id.

Then, it will automatically find the offset, initial values, and do the fitting.
Now, you will obtain the parameters of the fitted curve and the evaluations.

## Appendix
### Import Fonts

**STEP1**: check if the font is installed

```import matplotlib.font_manager as fm

for font in fm.findSystemFonts(fontpaths=None, fontext='ttf'):
    prop = fm.FontProperties(fname=font)
    if "Times New Roman" in prop.get_name():
        print("Found:", font)
```

**STEP2**: Copy the .ttf file in C:/Windows/Fonts

Find the .ttf file online. There must be somewhere.

**STEP3**: Directly refer to it in your code

```
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

font_path = "C:/path/to/your/fontfile.ttf"  # フォントファイルの絶対パス
font_prop = fm.FontProperties(fname=font_path)
```

**STEP4** (if you want to use the font permanently): Install the font into your PC

Right click the .ttf file and click "install".
You might need administrator's previleges. 
