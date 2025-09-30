# myOfflineAi - A Flask UI for Ollama

<br>

Transparent and auditable offline Ai access for those who need extreme data privacy and don't want to blindly trust cloud providers and software developers.

- Ai access without an internet connection
- Runs on the desktop.
- Chat with Ollama models
- Create custom multimodal Ai tools - text, images, pdf (Similar to Gemini Gems and OpenAi GPTs)
- Chat histories are not saved
- Built to be transparent. Single-file flask app - code is easy to audit because html, css, js and python are all in one file.
- Double-click a file to run. No need to use the command line.

<br>

<img src="https://github.com/vbookshelf/myOfflineAi/blob/main/images/image1.png" alt="App screenshot" height="500">

<br>


## How to Install and Run

<br>

In this section you will be doing the following:
- Installing the Ollama desktop app
- Downloading a small 250MB text-only Ollama model
- Installing the UV python package manager
- Starting the myOfflineAi app by double clicking a file (The app auto installs the Python packages it needs.)

Notes:<br>
- I tested the installation process on Mac OS. I've included instructions for Windows, but I haven't tested on Windows.<br>
- After setup, you only need to double-click a file to launch the app.

System Requirements:
- Recommended: 16GB RAM
- Minimum: 8GB RAM
- Enough free disk space to store the models you download

<br>

```
1. Download and install the Ollama desktop application
This is the link to download Ollama. After downloading, install it on your computer.
https://ollama.com/

2. Download an Ollama model
If you have a good intenet connection and at least 8GB RAM then download the gemma3:4b model (2.5GB).
This model can handle both text and images.
If you have a slow connection then download the smaller gemma3:270m model (292MB).
This model can handle text only.

Open the Ollama desktop app. Paste the model name (e.g. gemma3:270m) into the dropdown in the bottom right.
Then type any message e.g. Hi.
The model will start to auto download.

3. Install UV
UV is a new and fast python package manager.
Here you will find the instructions to install uv on Mac and Windows:
https://docs.astral.sh/uv/getting-started/installation/#installation-methods

Open your terminal and copy paste this command:

Mac:
wget -qO- https://astral.sh/uv/install.sh | sh

Windows:
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

4. Download the project folder
Download the myOfflineAi project folder from this repo.

5. Open the folder and double-click a file.

Mac:
Double-click start-app.command

Windows:
Double-click start-app.bat

This will install all the python packages.
Then the myOfflineAi web app will open in your browser.
The terminal will also open.

5. Use the app
Click on "AI Assistant"
Type a mesage.

The name of the model you downloaded will appear in the dropdown in the top left.
If you downloaded the gemma3:4b you can also submit images and pdf documents.
To shut down the app: In the terminal type Crl+C on Mac or Alt+F4 on Windows.

6. Future - Simply Double-click a file to launch

Mac:
start-app.command

Windows:
start-app.bat

```

## Selecting and using models

<br>
When you first start the app you will only see the model you downloaded.<br>
To use the other models first make sure your computer has enough RAM to run them. 
Then download the model using the same procedure explained above.<br>
You will need to restart the myOfflineAi app to ensure that the model you downloaded is displayed in the dropdown menu.

You can explore the avaiable Ollama models here:
https://ollama.com/search

Below I will show how to add your own model to Ollama locally. 

<br>

## Response times when using myOfflineAi

<br>
When you send your first message, it may a minute to get your first response. But after that responses are much faster.<br>
Similarly when you submit an image or a pdf, the response time to the first message may take a while. But subsequent responses are faster.

Therefore, please be patient for the first response.

<br>

## myOfflineAi Settings

<br>
These are the app settings. To change them please open the app.py file with a text editor, make the change and then save the file as app.py.

Ollama models have a default context size of 4096 tokens.<br>
4096 is low and will lead to poor quality results when submitting files or when pasting in a large amount of text.<br>
I've set a custom context size.<br>
Note that setting large context sizes will slow down inference.<br>
NUM_CTX = 16000

TEMPERATURE = 0.3
TOP_K = 20
TOP_P = 0.95

Max number of pdf pages allowed per pdf file<
MAX_PAGES = 15

Each pdf page is converted into an image.<br>
The image resolution is set here.<br>
1.5x scale provides good readability while reducing file size.<br>
Change this if you need greater resolution when for example, when using medical images.<br>
PDF_IMAGE_RES = 1.5 # 150 dpi

Max pdf upload size<br>
MAX_UPLOAD_FILE_SIZE = 20 * 1024 * 1024 # (20MB)

<br>

## FAQ

<br>
1- Is it essential to switch off the internet connection?<br>
No it's not essential. By design, no data leaves your device. But I recommend putting Ollama desktop app into Airplane mode. This can be done in the Ollama settings.

2- How do I audit the code for privacy?<br>
There are two options. Either let a programmer review the code or take the app.py file and submit it to an Ai model like Gemini or ChatGPT. Ask it to review the code for data privacy compliance.

3- How do I add features, make changes or fix a bug?<br>
This is a single-file app thats designed to be reviewed and modified by Ai. All the code is in one file so the Ai sees the entire design. Simply take the app.py file and upload it to Gemini 2.5 Pro, Claude Sonnet or GPT-5. Tell it what changes or new features you want. Also tell it to output all the code on one page so you can copy and paste it. When the Ai outputs the revised code, copy it and replace all the code in the app.py file. Then put the app.py file back inside the project folder. Launch the app and check if your changes have been made.

4- How is pdf conversion handled internally?<br>
The app converts each page of the pdf document into an image. These images are then passed to the model.

5- Is it possible to edit a Tool after it is created?<br>
Yes it is. Hover over the tool in the left panel. The edit button will become visible.

<br>

## Lessons learned during this project

- Ollama models have a default context size of 4096. Knowing this will help you get much better results.
- When using Gemma models images come before text.
- The best coding models are Gemini 2.5 Pro and Claude Sonnet.
- Flask apps can be set up to start by double clicking a file.

<br>

## Resources

- Search Ollama models<br>
https://ollama.com/search

- Install UV<br>
https://docs.astral.sh/uv/getting-started/installation/#installation-methods

- How to create a single-file flask app<br>
https://github.com/vbookshelf/Single-File-Flask-Web-App

- 7 Essential AI Prompting Skills That Instantly Make Your Work Stand Out<br>
  Grace Leung<br>
  https://www.youtube.com/watch?v=-era_Orh3TM

<br>

## How to load your own models into Ollama locally (not up to the cloud)

The process is slightly different depending on whether or not the model is text only or multimodal. Here we will use the text-only MedGemma model as an example.

### 1- Download the .gguf file for the model.<r>

Download the file and place it on your desktop.

You can create a gguf file. But its simpler to find one on HuggingFace and download it.
For this example I've downloaded the BF16 gguf file from here:<br>
bartowski/google_medgemma-4b-it-GGUF<br>
https://huggingface.co/bartowski/google_medgemma-4b-it-GGUF

The 4b version is text only. The 27b version is multimodal i.e. it supports both text and image input.


### 2- If the model is multimodal, then also download the mmproj file.

Download the file and also place it on your desktop.

In the repo on Huggingface click 'Files'. Among the list of files, usually at the bottom, you will find files with names that start with mmproj. Choose the mmproj file that matches your chosen model and download it. For example, here we have chose the BF16 model so, if this was a multimodal model, then the following mmproj file needs to be downloaded:<br>
mmproj-google_medgemma-4b-it-bf16.gguf


[ TEXT-ONLY MODEL ]
```
1- Create a Modelfile

# cd to the desktop
% cd Desktop

# (Note that the path to the downloaded file is specified)<br>
# Make sure that you use the actual file name and not the model name from the repo.
% echo 'FROM ./google_medgemma-4b-it-bf16.gguf' > Modelfile

# 2- Insert the model into Ollama

# (You can specify any name. I've used: my-google_medgemma-4b-it-GGUF-bf16)<br>
# The file name you specify must be lower case only.
ollama create my-google_medgemma-4b-it-gguf-bf16 -f Modelfile

```

Thats all.<br>
You can now select the model using myOfflineAi or using the Ollama desktop app.<br>
You can only submit text.

[ MULTIMODAL MODEL ]
```
1- Create a Modelfile

# cd to the desktop
% cd Desktop

# Add the gguf and mmproj file names to this terminal command:
% echo 'FROM ./google_medgemma-4b-it-bf16.gguf
ADAPTER ./mmproj-google_medgemma-4b-it-bf16.gguf' > Modelfile

2- Insert the model into Ollama

# (You can specify any name. I've used: my-google_medgemma-4b-it-bf16)
% ollama create my-google_medgemma-4b-it-bf16 -f Modelfile

```

Thats all.<br>
You can now select the model using myOfflineAi or using the Ollama desktop app.<br>
You can submit both text and images.
Again, please note that the 4b Medgemma model that we downloaded is not multimodal. The 27b version is multimodal.

Test<br>
You can test the model by asking this question:<br>
How do you conduct a patient preclinical interview?

<br>

## How to delete an Ollama model from your computer

```
# Delete model
% olama rm model_name

```




