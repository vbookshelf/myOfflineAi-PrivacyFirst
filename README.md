<img src="https://github.com/vbookshelf/myOfflineAi-Privacy-First-Flask-Desktop-UI-for-Ollama/blob/main/myOfflineAi-v1.0/static/icon.png" alt="App screenshot" height="100">

# myOfflineAi - Privacy-First Ai

<br>

Transparent offline Ai access for professionals in highly regulated industries who need data privacy and don't want to blindly trust cloud providers.

- Ai access without an internet connection
- Runs on the desktop.
- Chat with Ollama models
- Create custom multimodal Ai tools - text, images, pdf (Specialized assistants - similar to Gemini Gems and OpenAi GPTs)
- Chat histories are not saved
- All user-submitted content, including files and images, is processed ephemerally (in memory). At no time is any data stored on disk.
- Built to be simple and transparent. Single-file flask app architecture - code is easy to audit because html, css, js and python are all in one file.
- Double-click a file to run. No need to use the command line.

<br>

myOfflineAi is an app that runs entirely on your computer and connects directly to Ollama - a program that lets you run AI models locally. Ollama is the engine that downloads, manages and runs the models. When you type something into the app, it sends your message to Ollama running on your machine (not over the internet). Ollama processes the request with the chosen AI model and streams the response back to the app.

In other words, myOfflineAi is a helpful interface running in your browser. Ollama models do the thinking in the background. Everything happens locally - your sensitive data never leaves your machine. Compliance thinking is built into the software.

<br>

<img src="https://github.com/vbookshelf/myOfflineAi/blob/main/images/image1.png" alt="App screenshot" height="500">
<p>myOfflineAi App</p>

<br>

<img src="https://github.com/vbookshelf/myOfflineAi-Flask-UI-for-Ollama/blob/main/images/image3.png" alt="Ollama desktop app screenshot" height="500">
<p>Ollama Desktop App</p>

<br>

<img src="https://github.com/vbookshelf/myOfflineAi-Flask-UI-for-Ollama/blob/main/images/image4.png" alt="Ollama desktop app settings" height="500">
<p>Ollama Settings - Airplane mode</p>

<br>

## What is Ephemeral data processing?

<br>

When you enter some text or you give the app a document, it reads the data straight into your computers temporary memory. It processes the data and then uses it to get the Ai answer. At no point is your sensitive data ever written down or stored on your hard drive. When you close the Assistant/Tool tab in the app or close your browser tab - any data in temporary memory is deleted. So even if someone got into your computer later - there would be no unencrypted data in your chat history or in an obscure file waiting to be found.

You trade the convenience of being able to look back through old chats for the certainty that your data is private and secure.

<br>

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

Normally, Ollama will launch automatically when you start your computer.

2. Download an Ollama model

If you have a fast internet connection and at least 8GB RAM then I suggest you download the gemma3:4b model (3.3GB).
This model can handle both text and images.
If you have a slow connection then download the smaller gemma3:270m model (292MB).
This model can handle text only.

How to download a model:
Open the Ollama desktop app.
Paste the model name (e.g. gemma3:270m) into the dropdown in the bottom right.
Type any message e.g. Hi.
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
Type a message.

The name of the model you downloaded will appear in the dropdown menu in the top left.
If you downloaded the gemma3:4b model you can submit images and pdf documents in addition to text.

The app does not stop running when you close the browser tab.
To shut down the app: In the terminal type Crl+C on Mac or Alt+F4 on Windows.

7. Future startup

Now that the setup is complete, in future simply Double-click a file to launch the app.

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
On Mac if the project folder is on your desktop type the following commands in the terminal:
```
% cd Desktop
% cd myOfflineAi-v1.0
% uv run python app.py
```

The app will start. A url will appear in the terminal: http://127.0.0.1:5000/<br>
Copy this url and paste it in your browser, then press Enter.

### 2- The app starts when you double-click the file but the browser does not auto open

Solution:<br>
Copy the url, displayed in the terminal (http://127.0.0.1:5000/) and paste it into the browser. Then press Enter.

### 3- The app does not work.

Possible causes are that the Ollama Desktop app is not running.<br> 
Or another instance of the app is already running on your computer and using the same port - because the app does not stop when you close the browser tab.

Solutions:<br>
- Start Ollama. Then retstart the app or<br>
- Look for an open terminal on your desktop and see if the app is already running. If it is running then type this url in your broswer: http://127.0.0.1:5000/

### 4- The model responses have become very poor

Not many people know that the context size of all Ollama models is set to 4096 tokens. There is no warning when the context is exceeded, but the quality of the responses becomes very poor.

This happens because Ollama will automatically drop the oldest messages/tokens from the history to make space for the new input. You don’t see an error, but earlier conversation context is silently lost.

Solution:<br>
Increase the context size by changing the NUM_CTX setting in the app.py file (currently NUM_CTX = 16000).<br>
Please note that large context sizes will slow down the model.

The app has a context warning system that will alert you when the context size has been exceeded or is close to being exceeded. Also, the total number of tokens in the message history is continuously printed in the terminal. This will help you monitor the context size. Ensure that this value stays below the value that you set for NUM_CTX.

### 5- Performance has suddenly slowed down

This can happen if you've submitted a large file. Even when you change the model to a smaller model the performance can still be slow. On Mac, if you look at the Activity Monitor you will see that the memory use is still high.

To manage memory, Ollama uses a caching mechanism controlled by a parameter called keep_alive. When you make a request with a model the Ollama server loads that entire model into RAM. When you then make a new request with a different, smaller model, Ollama loads this second model. The first, larger model is now considered inactive but remains in memory. The inactive model stays loaded for the duration specified by keep_alive. The default value is 5 minutes. If you don't use the large model again within that 5-minute window, Ollama will automatically unload it, and only then will the memory be freed.

This behavior is designed for performance, preventing the slow reloading a model if you need to use it again soon.

Solution:<br>
To free up memory immediately, Ollama needs to be shut down and restarted. You can do this by using "Quit Ollama" in the desktop app. When you click the "Quit Ollama" option from the menu bar icon (on macOS) or the system tray icon (on Windows), it does more than just close a window. It terminates the Ollama background server.

This action has several important effects:
- Stops the Server: The core Ollama process that listens for API requests is stopped.
- Frees All Memory: Any models currently loaded into your VRAM or system RAM are immediately unloaded.
- Ends Connectivity: You will no longer be able to interact with Ollama. Any attempt to connect will result in an error.

Simply closing a terminal window  does not stop the background server. The server is designed to run persistently. Using "Quit Ollama" is the correct way to ensure the application is fully turned off and all system resources are released.

### 6- Everything freezes even tho the model you are trying to use is small

This can happen if you have LM Studio running while you are trying to use Ollama and myOfflineAi.

Solution:<br>
Eject any model that you have loaded into LM Studio.<br>
Quit LM Studio.


<br>

## Selecting and using models

<br>
When you first start myOfflineAi you will see only one model in the dropdown menu - the model that you downloaded. To add other models first make sure your computer has enough RAM to run them. Then download the Ollama model using the same procedure explained above. You can check model sizes by searching models on the Ollama website.

You will need to restart the myOfflineAi app to ensure that the model you downloaded is displayed in the dropdown menu.

You can explore Ollama models here:<br>
https://ollama.com/search

It's also possible to add your own model to Ollama locally. This process is explained below.

<br>

## Response times

<br>
When you send your first text message, it may take a few seconds to get your first response. But after that responses are much faster.

This is because, by default models are kept in memory for 5 minutes before being unloaded. This allows for quicker response times when you are making multiple requests during a chat.

Similarly, when you submit an image or a pdf, the response time to the first message may take a while. But subsequent responses are faster. 

Therefore, please be patient for the first response.

<br>

## myOfflineAi Settings

<br>

These are the app settings.<br>
To change them please open the app.py file with a text editor, make the change and then save the file as app.py.<br>
Some systems may add a .txt extension. Please double check that the file has not been saved as: app.py.txt

<br>

```
Context size
NUM_CTX = 16000

TEMPERATURE = 0.6
TOP_K = 60
TOP_P = 0.95
FREQUENCY_PENALTY = 1.0
REPEAT_PENALTY = 1.0

Max number of pdf pages allowed per pdf file
MAX_PAGES = 15

Each pdf page is converted into an image.
The image resolution is set here.
1.5x scale provides good readability while reducing file size.
1.5 is 150 dpi, 2.5 is 250 dpi etc.
Change this if you need greater resolution. For example, when reviewing medical images.
PDF_IMAGE_RES = 1.5 

Max pdf upload size is set to 20MB
MAX_UPLOAD_FILE_SIZE = 20 * 1024 * 1024

```
<br>

## Security and Auditability

<br>

This app is provided without warranties.<br>
I suggest that you do a privacy audit of the code before using the app.

There are no opaque executables. Everything is plain text.

The single-file Flask app architecture places all the necessary code — HTML, CSS, JavaScript, and Python — into a single app.py file. This makes the code easy to audit because a compliance professional can review the entire application design and logic in one place without needing to navigate a complex file structure.

Files to inspect: 
- app.py
- pyproject.toml
- uv.lock
- start-mac-app.command
- start-windows-app.bat

This is a note from Ollama concerning privacy:<br>
[Does Ollama send my prompts and responses back to ollama.com?](https://github.com/ollama/ollama/blob/main/docs/faq.md#does-ollama-send-my-prompts-and-responses-back-to-ollamacom)

#### Use Ai to do a quick privacy audit

To do a quick check, you can take the app.py file and submit it to an enterprise grade Ai model like Gemini 2.5 Pro or Claude Sonnet. Ask it to review the code for data privacy compliance. Because GPT-5 sets it's thinking budget dynamically, there's no guarantee that it will apply the highest level of thinking to this code review.

You can ask the following questions:

- Does this code send any data out?
- Are there any privacy risks here?
- What happens if I forget to turn off my internet connection?
- The app creates files named agents.json and last_model.txt. What are those files for?

By using Ai to check the code, even if you don't know anything about programming, you can get a sophisticated privacy compliance report within minutes. But it's important to use the enterprise grade pro level models and not the faster consumer models.

<br>

## FAQ

<br>

### 1- Is it essential to switch off the internet connection?<br>
No it's not essential. By design, no data leaves your computer. But I recommend putting the Ollama desktop app into Airplane mode. This can be done in the Ollama settings. A picture of the settings menu is shown above.

### 2- How do I add features, make changes or fix a bug?<br>
This is a single-file app. It's designed to be reviewed and modified by Ai. All the code is in one file so the Ai sees the entire design. Simply take the app.py file and upload it to Gemini 2.5 Pro, Claude Sonnet or GPT-5. Tell it what bug to fix or what changes or new feature you want. Also tell it to output all the code on one page so you can copy and paste it. When the Ai outputs the revised code, copy it and replace all the code in the app.py file. Then put the app.py file back inside the project folder. Launch the app and check if your changes have been made.

### 3- How is pdf conversion handled internally?<br>
The app converts each page of the pdf document into an image. These images are then passed to the model. This ensures that the model sees all relevant details including graphs and hand written comments.

### 4- Is it possible to edit a Tool?<br>
Yes it is. Hover over the tool in the left panel. The edit button will become visible.

<br>

## How to load your own models into Ollama locally (not up to the cloud)

<br>

Ollama makes multimodal local CPU inference simple. To take advantage of this you may want to load your own domain specialized models into Ollama, on your computer. Here I will explain how to do that. We will use the MedGemma model (4b version) as an example. 

4b means 4 billion parameters. It's a refelection of the size and capability of the model. For reference, a top end model like GPT-5 may have more the 500 billion parameters.

<br>

The process to add the model to Ollama is slightly different depending on whether the model is text only or multimodal.

### 1- Download the .gguf file for the model.

To add a model to Ollama it the file has to be in gguf format. You can convert a model to gguf. But it's simpler to find one on HuggingFace and download it.

For this example I've downloaded the BF16 gguf file from here (7.77GB):<br>
bartowski/google_medgemma-4b-it-GGUF<br>
https://huggingface.co/bartowski/google_medgemma-4b-it-GGUF

We are using the BF16 model. BF16 means that the model is in it's original form, without any quantization (smart compression). Quantization reduces the size of a model but it can also affect the model's performance in unexpected ways. This uncertainty is not acceptable for medical applications. BF16 models can be very large. But in this case the BF16 size is only 7.7 GB.

The 4b MedGemma version is text only. The 27b version is multimodal. Multimodal means that it supports both text and image input. Some multimodal models also support video and audio input.


### 2- If the model is multimodal, then also download the mmproj file.

In the repo on Huggingface click 'Files'. Among the list of files, usually at the bottom, you will find files with names that start with mmproj. Choose the mmproj file that matches your chosen model and download it. Here we have chosen the text only BF16 model. But if this was a multimodal model, then the following mmproj file needs to be downloaded:<br>
mmproj-google_medgemma-4b-it-bf16.gguf

The terminal commands below are for Mac. Windows will be similar.
You don't need to type the % symbol.


### [ TEXT-ONLY MODEL ]
```
1- Create a Modelfile

These terminal commands assume the file is on your desktop.

# cd to the desktop
% cd Desktop

# (Note that the path to the downloaded file is specified)<br>
# Make sure that you use the actual file name and not the model name from the repo.
% echo 'FROM ./google_medgemma-4b-it-bf16.gguf' > Modelfile

2- Insert the model into Ollama

# (You can specify any name. I've used: my-google_medgemma-4b-it-GGUF-bf16)<br>
# The file name you specify must be lower case only.
% ollama create my-google_medgemma-4b-it-gguf-bf16 -f Modelfile

```

The model has now been inserted into your local Ollama models folder.<br>
The medGemma model will now appear in the myOfflineAi dropdown menu and in the Ollama desktop app dropdown menu.<br>
As this is a text only model, you can only submit text.

You can test the model by asking this question:<br>
How do you conduct a patient preclinical interview?

<br>

### [ MULTIMODAL MODEL ]

This is for example only because the 4b MedGemma model is not multimodal.

```
1- Create a Modelfile

These terminal commands assume the file is on your desktop.

# cd to the desktop
% cd Desktop

# Add the gguf and mmproj file names to this terminal command:
% echo 'FROM ./google_medgemma-4b-it-bf16.gguf
ADAPTER ./mmproj-google_medgemma-4b-it-bf16.gguf' > Modelfile

2- Insert the model into Ollama

# (You can specify any name. I've used: my-google_medgemma-4b-it-bf16)
% ollama create my-google_medgemma-4b-it-bf16 -f Modelfile

```


<br>

## How to delete an Ollama model from your computer

This command is for Mac.

```
# Type this in the terminal
% olama rm model_name

```

<br>

## Lessons learned during this project

<br>

1- All Ollama models are set to context size of 4096 tokens. I didn't know this. At first I just assumed that small local models were just bad. This small size allows the models to work faster. However, when your inputs (or the chat history) exceeds this size there's no warning message. The quality of the model's responses just becomes very poor. In this app I've set a context size of 16000. You can change the context size if needed. But take note that this will affect the speed of the model's responses. Also, I've built in a context warning system that will alert you when the context size has been exceeded or is close to being exceeded. Additionally, the total size of the context is continously printed in the terminal.
  
2- When using Gemma models - images must be placed before text when coding the model input<br>e.g. [<my_image>, "What's on this image?"].<br>This gives much better results.

3- Ai models are now capable of coding up entire apps. I used Ai models like Gemini 2.5 Pro, Claude Sonnet, GPT-5 and Qwen-235B extensivley during this project. The secret is the single-file flask app architecture. All the code - html, css, js, python - is in one file. Therefore, the Ai can see the entire app design. This makes it easy for Ai to make changes and fix bugs.<br> See: https://github.com/vbookshelf/Single-File-Flask-Web-App<br>
I got better results by using top-end models e.g. Gemini 2.5 Pro and not Gemini 2.5 Flash. Each Ai has it's own quirks and strengths. For example, Gemini 2.5 Pro produces beautiful UI designs but it struggled to add comments to Html code.

4- Using Flask together with the UV Python package manager creates a powerful setup for desktop applications. Flask was originally designed as a lightweight framework for building web applications to be deployed on servers. But Flask is also well-suited for running locally on the desktop. Its simplicity makes it ideal for creating fast, elegant, and functional Python apps.

In my earlier Flask projects, one major limitation for desktop use was that users needed to rely on the command line to install dependencies and to start the app. This was a barrier beacuse non-programmers are not comfortable using terminal commands.

On this project, I discovered a way to remove that friction. With UV, the entire process can be streamlined so that the user only needs to double-click a file: dependencies are installed automatically, and the app launches without any extra steps. Each time the user only needs to double-click a file to run the app.

This approach makes desktop Flask apps far more accessible to everyday users. It also makes the app easier to share - non-programmers can simply send the zipped file by email. There's no need to use GitHub or Docker.

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

## Conclusion

MyOfflineAi solves the privacy problem through isolation and local ephemeral processing. 

But this project is about more than just privacy. It's a shift in mindset. It's about owning and controlling your own tools. It's about changing your role from being a passive consumer of Ai services to an active and accountable owner of your Ai capability.

<br>

## Revision History

Version 1.0<br>
1-Oct-2025<br>
First release






