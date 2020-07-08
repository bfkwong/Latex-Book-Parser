# Markdown Parser Documentation 

### Python Dependencies
- [Mistletoe](https://github.com/miyuchina/mistletoe)
- [Requests](https://requests.readthedocs.io/en/master/)
- [Pandas](https://pandas.pydata.org/)

## I. BOOK LAYOUT 

### Chapter Layout

Markdown header tags gets translated into chapter, section, and subsection tags in HTML. The `\label{...}` tag is the first word of a space delimited string. 

Consider the example string of `"Ch.1 A Dream and a Song"`. The parser will split this string into two parts base on the first space encountered in the string (`"Ch.1"` and `"A Dream and a Song"`). The first part will become the label name and the second part will be the title name. So for this example, the translated version is `\chapter{A Dream and a Song} \label{Ch.1}`. Here are some extra examples of how the label tag is derived. 

**MARKDOWN**

```
# Ch.1 Hong Kong 
## 1.1 History
### 1.1.1 British Occupation

## Weird Format
```

**LATEX TRANSLATION**

```
\chapter{Hong Kong} \label{Ch.1}
\section{History} \label{1.1}
\subsection{British Occupation} \label{1.1.1}

\section{Format} \label{Weird}
```

It is recommended that each chapter only has one `#` tag and each section has a `##` tag and each subsection has a `###` tag. A markdown example is shown below with its latex translation 

**MARKDOWN**

```
# Ch.1 Hong Kong

Hong Kong is a metropolitan area and special administrative region of the People's Republic of China in the eastern Pearl River Delta by the South China Sea. 

## 1.1 History

The region is first known to have been occupied by humans during the Neolithic period, about 6,000 years ago.

### 1.1.1 British 

Hong Kong Island was formally ceded to the United Kingdom in the 1842 Treaty of Nanking. The colony was further expanded in 1898, when Britain obtained a 99-year lease of the New Territories.

```

**LATEX TRANSLATION**

```
\chapter{Hong Kong} \label{Ch.1}

Hong Kong is a metropolitan area and special administrative region of the People's Republic of China in the eastern Pearl River Delta by the South China Sea. 

\section{History} \label{1.1}

The region is first known to have been occupied by humans during the Neolithic period, about 6,000 years ago.

\subsection{British} \label{1.1.1}

Hong Kong Island was formally ceded to the United Kingdom in the 1842 Treaty of Nanking. The colony was further expanded in 1898, when Britain obtained a 99-year lease of the New Territories.
```

### Posting Images

Images must have an alternative title for the parser to function properly. The parser will rely on the alt-title to name the files that will be generated. The image source can either be an HTTP link or a local file. The alt-titles should have unique titles. 

**EXAMPLE**

```
![title1](www.linktoimage.com/image1)
![title2](www.linktoimage.com/image2)
```

## II. EQUATIONS 

Equations in Markdown should be done with `\begin{align} ... \end{align}`. The parser is setup to recognize `align` but not `equation`. Additionally, equations should be wrapped in `$$` tags touching the `\begin{align}` and `\end{align}` tags. 

**EXAMPLE: Correct way to use align**

```
$$\begin{align}
y = mx + b
\end{align}$$
```

**EXAMPLE: WRONG way to use align**

```
$$
\begin{align}
y = mx + b
\end{align}
$$
```

###  Equation Number 

Equation number in markdown should be down with the `label{name}\tag{1}` tag within `align`. The parser will automatically remove the `tag{1}` so that Latex can do the proper numbering. When referencing the equation, the `eqref` tag should be wrapped in `$`.

**EXAMPLE**

```
$$\begin{align}
y = mx + b
\label{slope_int_form}\tag{1}
\end{align}$$

The slope intercept form $\eqref{1}$ defines a line using the slope of the line and the y intercept of the line
```

*Note: Colab Notebooks won't work perfectly with this equation numbering. You will have to refresh the page to make the equation numbering to work correctly. However, if you use Jupiter Lab or Jupiter Notebook, this equation numbering feature will work fine with out refresh.*

## III. CODE AND OUTPUT

### Code Blocks

The code blocks should be limited to 65 lines long. Anything longer will cause the Latex files to overflow. This applies for comments as well.

### Output Blocks 

#### IMAGES 

The parser is trained to output images encoded as PNGs. Any other format is not supported. Matplotlib already supports PNG images by default. This means that `Altair` graphs must use an HTML renderer. On Colab notebook, it will require the following code to be run to set up the environment. On any local environment, consult the Altair guide on how to set up Selenium. 

```
# SETUP : Allow Altair to Display Charts as PNG
!pip install selenium
!apt-get update 
!apt install chromium-chromedriver

from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
wd = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
driver =webdriver.Chrome('chromedriver',chrome_options=chrome_options)

import altair as alt
alt.renderers.enable('png')
# END SETUP
```

#### TABLE OUTPUT

It is recommended to use `print(...)` for pandas table output instead of `display(...)` because `print(...)` limits the number of rows that it will display. Unfortunately, there is no way to limit the number of lines the pandas data frame will print, however, this behavior can be simulated by how many columns to print and how many lines per column to print with the following code 

```
pd.set_option("display.max_columns", 4)
pd.set_option("display.max_colwidth", 15)
```

## IV. LINK FORMATTING

Whenever you are writing a link, it can be represented two ways: inline or as a footnote. 

### Footnote 
To make your link a footnote use the markdown link formatter 

**MARKDOWN**

```
Check out [google](www.google.com)!
```

**LATEX**

```
Check out google\footnote{www.google.com}!
```

### Inline
To make your link inline with the text, use inline code block quotation (\` \`). This is a general rule with this parser, ALWAYS put underscores in inline code block quotations (consult section 5 for more information about what else to put in inline block code quotations). 

## V. FORMAT REQUIREMENTS OF `Mistletoe` 

`Mistletoe` is the package that the parser use to translate markdown to raw latex before the parser does further processing. Here are a few do's and don't's when writing Markdown. 

**DO**

* DO put all text with an underscore in inline code block quotations (i.e. links)

```
Check out this link at `www.somelink.com/sub_link`.
```

* DO put all percentages in \` \` quotations

```
According to a study, `100%` of bald people have no hair.
```

* DO put all weird characters like ~ as `$\verb|~|$`

```
$\verb|~|$ character means negative in the SML language.
```

**DON'T** 

* DON'T nest `$...$` within `$$...$$`

```
$$ y = mx + b \text{$m$ is the slope} $$
```

* DON'T nest formatting (i.e. don't put `*...*` within `**...**`)

```
Don't **do *this* please** 
```

* DON'T bold/italicize/verbatim texts within a markdown table

```
Markdown | Less | Pretty
--- | --- | ---
*Still* | `renders` | **nicely**
1 | 2 | 3
```

* DON'T bold/italicize/verbatim texts within #/##/### (ok to use `$...$`)

```
# This **chapter** is broken
```

* DON'T use the character `#` within `$...$`

```
$\text{# of things to break}$
```

* DON'T use HTML formatting

## VI. USAGE

Example usage of the PynbParser would be as follows 

```
$ python ./PynbParser.py ./config.json
```

To ensure everything gets rendered to Latex, make sure to run all the cells in each Markdown file so that any output and output images are in the file. 

### Config File

The python file takes in one config file as input. The config file is a JSON file that is formatted as follows 

```
{
	"resources": {
		"/main.tex": "http link to the file", 
		"/krantz.cls": "http link to the file", 
	},
	"book_directory": "TestBook",
	"glossary_word_csv": "./glossary.csv"
}
```

#### Resources

##### main.tex
The JSON file resources section must include a `main.tex` section. This is the main launching point for the latex notebook. Within `main.tex`, there must exists the string `"@@@SPLIT@@@"` that signifies where you want the compiled latex files to be put. For example. 

**source main.tex**

```
...
\usepackage{makeidx}
\usepackage{multicol}
\usepackage{graphicx}
\usepackage{csquotes}
\makeindex

\begin{document}
@@@SPLIT@@@
\printindex
\end{document}
...
```

**compiled main.tex**

```
...
\usepackage{makeidx}
\usepackage{multicol}
\usepackage{graphicx}
\usepackage{csquotes}
\makeindex

\begin{document}
\include{01_Data_Ecosystem/out}
\include{02_Categorical_Data/out}
\include{03_Quantitative_Data/out}
\include{05_Regression_Models/out}
\printindex
\end{document}
...
```

##### Other Resources 

The other resources that could be put into the config files include things like format files (`klantz.cls`) or tex files that `main.tex` will use. Just provide the name of the file and the http link to it. All resources file will be put at the surface directory of `./LatexBook`. 

#### Book Directory

The config file also takes in a key called `"book_directory"`. This is the directory that the parser will go to to look for the  books. This parameter accepts a relative path to the folder. Do not use `.` or `..` in your path, this is important because this directory will help create the final project structure of the LatexBook directory.

#### Glossary Word CSV

This is a CSV file that contains all glossary words that you would like the parser to create an index for. In Latex, glossary words marked by `\index{pandas}`. Thus any words in the glossary CSV will be parsed to be put inside an index tag. The Format of this File should be as follows: 

words| 
---|
Quantative Variable|
Dataframes| 
Jupyter| 
Tabular Data|

The CSV file would be displayed as 

```
words
Quantative Variable
Dataframes
Jupyter
Tabular Data
```

### Output

Once the parser is done running, it will dump all of its compiled output in `./LatexBook` directory path. In order for overleaf to accept this, you will have to zip all the contents INSIDE of `./LatexBook/`. Do not include the `./LatexBook` folder itself, only its content goes into the zip file. This zip file can now be uploaded into overleaf. 
