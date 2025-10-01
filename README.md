# myOfflineAi - Privacy-First Ai

<br>

Transparent and auditable offline Ai access for professionals in highly regulated industries who need data privacy and don't want to blindly trust cloud providers and software developers.

- Ai access without an internet connection
- Runs on the desktop.
- Chat with Ollama models
- Create custom multimodal Ai tools - text, images, pdf (Similar to Gemini Gems and OpenAi GPTs)
- Chat histories are not saved
- All user-submitted content, including files and images, are processed ephemerally (in memory). At no time is any data stored on disk.
- Built to be transparent. Single-file flask app - code is easy to audit because html, css, js and python are all in one file.
- Double-click a file to run. No need to use the command line.

<br>

This app runs entirely on your computer and connects directly to Ollama, which is a program that lets you run AI models locally. When you type something into the app, it sends your message to Ollama running on your machine (not over the internet). Ollama then processes the request with the chosen AI model and streams the response back to the app, which displays it in the chat window.

In simple terms: the app is just a friendly interface in your browser, while Ollama does the “thinking” in the background. Everything happens locally, so your data never leaves your computer.

<br>

<img src="https://github.com/vbookshelf/myOfflineAi/blob/main/images/image1.png" alt="App screenshot" height="500">
<p>myOfflineAi App</p>

<br>

<img src="https://github.com/vbookshelf/myOfflineAi-Flask-UI-for-Ollama/blob/main/images/image3.png" alt="Ollama desktop app screenshot" height="500">
<p>Ollama Desktop App</p>

<br>

<img src="https://github.com/vbookshelf/myOfflineAi-Flask-UI-for-Ollama/blob/main/images/image4.png" alt="Ollama desktop app settings" height="500">
<p>Ollama Settings - Airplane mode</p>

## How to Install and Run

<br>

In this section you will do the following:
- Install the Ollama desktop app
- Download a small 250MB text-only Ollama model
- Install the UV python package manager
- Start the myOfflineAi app by double clicking a file

Notes:<br>
- I tested the installation process on Mac OS. Although I've included instructions for Windows, I haven't tested on Windows.
- After setup, you only need to double-click a file to launch the app.

System Requirements:
- Recommended: 16GB RAM
- Minimum: Depends on the model size
- Enough free disk space to store the models you download

<br>

```
1. Download and install the Ollama desktop application

This is the link to download Ollama. After downloading, please install it on your computer.
Then launch it. A white chat window will open.
https://ollama.com/

2. Download an Ollama model

If you have a fast internet connection and at least 8GB RAM then I suggest you download the gemma3:4b model (2.5GB).
This model can handle both text and images.
If you have a slow connection then download the smaller gemma3:270m model (292MB).
This model can handle text only.

To download first open the Ollama desktop app.
Then paste the model name (e.g. gemma3:270m) into the dropdown in the bottom right.
Then type any message e.g. Hi.
The model will start to auto download.

3. Install UV

UV is a new and fast python package manager.
Here you will find the instructions to install uv on Mac and Windows:
https://docs.astral.sh/uv/getting-started/installation

Open your terminal and copy paste this command:

Mac:
wget -qO- https://astral.sh/uv/install.sh | sh

Windows:
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

4. Download the project folder

Download the myOfflineAi project folder from this repo.

5. Open the folder and double-click a file.

Mac:
Double-click start-mac-app.command

Windows:
Double-click start-windows-app.bat

This will install all the python packages.
Then the myOfflineAi web app will open in your browser.
The terminal will also open.

6. Use the app

Click on "AI Assistant"
Type a mesage.

The name of the model you downloaded will appear in the dropdown menu in the top left.
If you downloaded the gemma3:4b model you can submit images and pdf documents in addition to text.

The app does not stop running when you close the browser tab.
To shut down the app: In the terminal type Crl+C on Mac or Alt+F4 on Windows.

7. Future - Simply Double-click a file to launch

Mac:
start-mac-app.command

Windows:
start-windows-app.bat

```

<br>

## Troubleshooting

### 1- The app doesn't auto start when you double-click the file

Solution:<br>
Launch the app manually from the terminal.

Example:<br>
On mac if the project folder is on your desktop type the following commands in the terminal:
```
% cd Desktop
% cd myOfflineAi-v1.0
% uv run python app.py
```

The app will start. A url will appear in the terminal: http://127.0.0.1:5000/<br>
Copy this url and paste it in your browser.<br>
The app will be displayed.<br>

### 2- The app starts when you double-click the file but the browser does not auto open

Solution:<br>
Copy the url, displayed in the terminal (http://127.0.0.1:5000/) and paste it into the browser.

### 3- The app does not work.

Possible causes are that the Ollama Desktop app is not running.<br> 
Or another instance of the app is already running on your computer and using the same port - the app does not stop when you close the browser tab.

Solutions:<br>
Start Ollama. Then retstart the app.<br>
Look for an open terminal on your desktop and see if the app is already running. If it is running then type this url in your broswer: http://127.0.0.1:5000/

<br>

## Selecting and using models

<br>
When you first start myOfflineAi you will only see the model you downloaded in the dropdown menu. To add other models first make sure your computer has enough RAM to run them.  Then download the Ollama model using the same procedure explained above.

You will need to restart the myOfflineAi app to ensure that the model you downloaded is displayed in the dropdown menu.

You can explore Ollama models here:<br>
https://ollama.com/search

My recommended model is: gemma3:12b (8.1GB, Text and image)

It's also possible to add your own model to Ollama locally. This process is explained below.

<br>

## Response times

<br>
When you send your first text message, it may take a few seconds to get your first response. But after that responses are much faster.

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

TEMPERATURE = 0.3<br>
TOP_K = 20<br>
TOP_P = 0.95<br>

Max number of pdf pages allowed per pdf file<br>
MAX_PAGES = 15

Each pdf page is converted into an image.<br>
The image resolution is set here.<br>
1.5x scale provides good readability while reducing file size.<br>
Change this if you need greater resolution when for example, when using medical images.<br>
PDF_IMAGE_RES = 1.5 # 150 dpi

Max pdf upload size<br>
MAX_UPLOAD_FILE_SIZE = 20 * 1024 * 1024 # (20MB)

<br>

## Security and Auditability

<br>

This app is provided without warranties.<br>
I suggest that you do a privacy audit of the code before using the app.<br>
There are no opaque executables. Everything is plain text.

Files to inspect: 
- app.py
- pyproject.toml
- uv.lock
- start-mac-app.command
- start-windows-app.bat

You should also review how myOfflineAi interacts with the Ollama desktop app.<br>
This is a note from Ollama concerning privacy:<br>
[Does Ollama send my prompts and responses back to ollama.com?](https://github.com/ollama/ollama/blob/main/docs/faq.md#does-ollama-send-my-prompts-and-responses-back-to-ollamacom)

For a quick check you can take the app.py file and submit it to an Ai model like Gemini, ChatGPT or Claude. Ask it to review the code for data privacy compliance.

<br>

## FAQ

<br>

### 1- Is it essential to switch off the internet connection?<br>
No it's not essential. By design, no data leaves your device. But I recommend putting Ollama desktop app into Airplane mode. This can be done in the Ollama settings.

### 2- How do I add features, make changes or fix a bug?<br>
This is a single-file app thats designed to be reviewed and modified by Ai. All the code is in one file so the Ai sees the entire design. Simply take the app.py file and upload it to Gemini 2.5 Pro, Claude Sonnet or GPT-5. Tell it what changes or new features you want. Also tell it to output all the code on one page so you can copy and paste it. When the Ai outputs the revised code, copy it and replace all the code in the app.py file. Then put the app.py file back inside the project folder. Launch the app and check if your changes have been made.

### 3- How is pdf conversion handled internally?<br>
The app converts each page of the pdf document into an image. These images are then passed to the model.

### 4- Is it possible to edit a Tool after it is created?<br>
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

- Ollama FAQ<br>
  https://github.com/ollama/ollama/blob/main/docs/faq.md

<br>

## How to load your own models into Ollama locally (not up to the cloud)

<br>

Ollama makes multimodal local CPU inference simple. To take advantage of this you may want to load your own domain specialized models into Ollama, on your computer. Here I will explain how to do that. We will use the MedGemma model as an example.

<br>

The process is slightly different depending on whether the model is text only or multimodal.

### 1- Download the .gguf file for the model.<r>

Download the file and place it on your desktop.

You can create a gguf file. But its simpler to find one on HuggingFace and download it.
For this example I've downloaded the BF16 gguf file from here:<br>
bartowski/google_medgemma-4b-it-GGUF<br>
https://huggingface.co/bartowski/google_medgemma-4b-it-GGUF

The 4b MedGemma version is text only. The 27b version is multimodal i.e. it supports both text and image input.


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
# Type this in the console
olama rm model_name

```

Troubleshooting

If the launcher shows: Ollama is not installed → install from https://ollama.com/download
.

If the launcher shows: 'uv' is not installed → recommended: pipx install uv or python3 -m pip install --user uv.

## Revision History


If browser doesn't open, open http://127.0.0.1:5000 manually.





