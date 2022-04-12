# Thai-Sentence-Correction

<div id="top"></div>
A spelling correction application that can correct misspell Thai compound words by using a Symmetric Delete Spelling Correction (SymSpell) approach. 

<br />




<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->
Some fields in Thai Natural Language Processing are an emerging field due to the complexity of Thai language. However, Thai spelling correction is similar to English since we not only look a single word, but also a language model and the context around it. Hence, considering n-grams around each specific word can be used to find the misspell compound word. Some libraries already proposed a solution for spelling correction by using Norvig's approach, brute force all possible edits, such as delete, insert, transpose, replace and split which have tremendous possibilities and inordinately expensive for searching.

A Symmetric Delete Spelling Correction (SymSpell) generate a dictionary with edit distance using only deletes instead of delete + insert + transpose + replace. With these, it also covers every single case as the same as Norvig's approach, and it is much faster and tends to be more language independent. For more details, the table shown below indicates that all cases are covered using SymSpell (only delete) approach.  

COMPARISION                                     |   RESULT
----------------------------------------------- | -------------
Dictionary Entry         == Input Entry         |   Correct
delete(Dictionary Entry) == Input Entry         |   Type 1 character less than usual (Delete)
Dictionary Entry         == delete(Input Entry) |   Type 1 more exceed (Insert)
delete(Dictionary Entry) == delete(Input Entry) |   (Replace) + (Transpose)

In this repository, we will use a Symmetric Delete Spelling Correction (SymSpell) approach to do the Thai Spelling Correction.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Setup

1. Clone the repo
   ```sh
   git clone https://github.com/Mickzaa/Thai-sentence-correction.git
   ```
2. Install packages 
    ```
    pip install -r requirements.txt
    ```

### Usage
1. Edit Text in input_text.txt

2. Run Programme
    ```sh
    python th_correction.py
    ```

### Option
#### For Argsparse

--file: Text_File_Path

--engine: Engine for word segmentation e.g. attacut, deepcut (default as attacut)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- Result -->
## Result
![Capture](https://user-images.githubusercontent.com/62434159/162964854-21f3de10-8fae-48c8-a905-803fa36c6ff2.PNG)
<p>Input: Thai sentences within one line needed to be written in input_text.txt</p>
<p>Recommend: Each sentence should be seperated with a spacebar.</p>
</br>
<p>Output: The start index, the end index of the old word, old_word and new_word will be returned.</p>

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- Feature -->
## Features

- ✅    Word Suggestion using corpus unigrame, bigrame, trigrame
- ✅    Start and end index are provided
- ✅    Word Suggestion with highest frequency 
- ❌    Auto Correction 

See the [open issues](https://github.com/Mickzaa/Thai-sentence-correction/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Krit Apornwirat - [Linkedin](https://www.linkedin.com/in/krit-apornwirat-0440b120b/)

Project Link: [https://github.com/Mickzaa/Thai-sentence-correction](https://github.com/Mickzaa/Thai-sentence-correction)

<p align="right">(<a href="#top">back to top</a>)</p>
