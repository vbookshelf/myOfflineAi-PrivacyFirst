# myOfflineAi - A Flask UI for Ollama

Transparent offline Ai access for those who need extreme data privacy and don't want to blindly trust cloud providers and software developers.

- Chat with Ollama models
- Create multimodal Ai tools
- Local. Transparent. Free.
- Users don't need to trust, because they have complete control.

myOfflineAi is a single-file Flask app - HTML, CSS, JS and Python code are all in one file (app.py). This makes the code easy to audit. 

It also makes it easy for Ai models like Gemini, ChatGPT and Claude to modify the code to add new features to the app. Simply give the Ai model the app.py file and tell it what changes or what new feature you want. If you find a bug you can use Ai to immediately fix it.

## Designed for where technology is going, not where it currently is

Currently, if you want to run AI models locally you are restricted to using small models. The bottom line is that these models are not trustworthy. They are okay for non-crtical work like translation, summarization and brainstorming. But their ability to hallucinate makes them unsuitable for high precision work like extracting patient data from medical records.

That said, the most recent small models, like Gemma3, have very good qualities: They are multilimgual. They are multimodal meaning that they can handle both text and images. And they run quite fast on a CPU. Some, like the Qwen3 models, also have the ability to reason internally i.e. they are thinking models.

Trustworthy local Ai is not a reality yet, but the day when it will be is coming fast. myOfflineAi is designed so that when that day comes you can load up the model and hit the ground running.


<br>

<img src="https://github.com/vbookshelf/myOfflineAi/blob/main/images/image1.png" alt="App screenshot" height="500">

<br>

## What problem does this solve?

Most of us take it for granted that we can drop a document into Google Translate or ChatGPT without a second thought. But what if that document is your grandmother’s secret recipe? Or a client’s legal brief? Or a patient’s medical chart? For many people, uploading such things to the cloud is a risk. A single upload could expose sensitive data, waive attorney–client privilege, or violate medical privacy laws. That fear prevents many from benefiting from the power of AI to help them be more productive and to serve more people.

Large firms can buy their way out of this problem with costly, enterprise-grade privacy systems. But the solo lawyer, the therapist in private practice, the small nonprofit cannot.
Open source, offline, privacy-first AI solves this problem. The data never leaves the user’s computer. And there's full transparency - all the underlying code for the app can be audited for data privacy compliance. Also, the user's internet connection can be disconnected while the app is being used - creating peace of mind.

## What is myOfflineAi?

myOfflineAi is a privacy-first Flask UI for Ollama AI models. The user has complete control and there's total transparency. The app runs offline. CSS and JS code is stored locally. Therefore, the internet connection can be switched off. Additionally, the Ollama app that serves the model can be put in Airplane mode. This ensures data privacy. The user has complete control and does not need to blindly trust the software developer's privacy assurances.

## Features

- Single-File app: Html, CSS, JS and Python code are all in one file named app.py
- Full transparency: No black box. Users can inspect the code themselves or give the app.py file to an LLM and ask it to explain exactly what the code does. For example: When you submit an image to a Gemma model and ask it what's on the image - does the code put your text question first or the image first? That order affects the quality of the Gemma model's response. (It should be image first.)
- Customizable: Because its a single-file app, it's easy to use ChatGPT, Gemini or Claude to make code changes and add features.
- Data privacy: Uses on-device Ollama models. Runs offline. Does not save anything.
- Multimodal: Supports image and pdf input. Processes pdf pages as images, for greater accuracy.
- Custom tools: The user can create custom Ai tools - similar to Gemini Gems and OpenAi GPTs.

<br>

## Build it. Release it. Forget it.

## Limitations
- Hallucinations
- Slow response time to first message when processing pdf documents and images
- Limited to using small models


## How to Install and Run the app

There's a few steps that you need to follow when first installing. Normally you only need to make sure Ollama is running, and then double-click a file to launch the app.

System Requirements

The app has the following models that you can select:
- gemma3:270m - Text only, 32K context, 292MB
- gemma3:4b - Text and Images, 128k context, 3.3GB
- gemma3:12b - Text and Images, 128k context, 8.1GB (Recommended)
- qwen3:4b - Text only, Thinking, 256k context, 2.5GB

Other Ollama models can be easily added.

The amount of RAM that your machine has needs to exceed the sizes shown above.
For example, if your computer has 8GB of RAM then you should select the gemma3:4b because
its size is 3.3GB. On an M series Mac with 16GB RAM, models with a size of approx. 10 GB tend to run well.

The models run on the CPU. The speed at which the models run will depend on how fast your computer is. 

```
1. Download and install Ollama
For the app to work Ollama needs to be installed and running.
This is the link to download Ollama. After downloading it install in on your computer.
https://ollama.com/

2. Download an Ollama model
The models used in the app need to be downloaded using Ollama.
If you have a good intenet connection download the gemma3:4b model (2.5GB). This model can handle both text and images.
If you have a slow connection then download the smaller gemma3:270m model (292MB). This model can handle text only.

There are two ways to downoad:
Method 1- Open your terminal and type this:
ollama pull gemma3:270m
Method 2- Open the Ollama app. Paste the model name into the dropdown in the bottom right. Then type any message e.g. Hi.
The model will start to auto download.

3. Install UV
UV is a new and fast python package manager.
Here you will find the instructions to install uv on Mac and Windows:
https://docs.astral.sh/uv/getting-started/installation/#installation-methods

Open your terminal and type this command:

Mac:
wget -qO- https://astral.sh/uv/install.sh | sh

Windows:
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

4. Download the project folder

5. Open the folder and double-click a file.
This will install all the python packages (first time only).
Then it will start the app.
The app will open in your browser.

Mac:
start-app.command

Windows:
start-app.bat

The app will open in your browser. The terminal will also open.

5. Use the app
Select the model that you downloaded from the dropdown in the top left.
Click the AI Assistant.
Type a mesage.
If you downloaded the gemma3:4b you can also submit images and pdf documents.<br>
The app converts pdf docs into images before processing.


5. Future

This set up process above only needs to be done once.
In future to start the app do the following:

1- Launch Ollama
2- Double-click this file that's in the project folder:
Mac:
start-app.command
Windows:
start-app.bat

The app will open in your browser. The terminal will also open.
To shut down the app from the terminal, type Crl+C on Mac or Alt+F4 on Windows.

5. Notes on selecting and using models.
When you first start the app you will only be able to use the gemma3:4b model because you've downloaded it already.
To use the other models first make sure your computer has enough RAM to run them. Then download the model using the same procedure explained above.

The app can run all Ollama models, but not all models are included in the dropdown.
To run a model that not included in the dropdown, to need to manually add model name to the dropdown.
To do this open the app.py file with a text editor and change one line of code. Then save the file.
model_list = ['gemma3:270m', 'gemma3:4b', 'gemma3:12b']

For example if you wanted to add the OpenAi gpt-oss:20b model this is the change you should make:
model_list = ['gemma3:270m', 'gemma3:4b', 'gemma3:12b', 'gpt-oss:20b]

Now, it will appear in the dropdown.
If you have downloaded gpt-oss:20b you will be able to use it in the app.

A full list of Ollama models and their details can be found here:
https://ollama.com/search

6. How to set a default model

The default model is the one that displays, in the dropdown, when you load the app.
To make a model your default, open the app.py file.
Change the number (model_list[0]) to match your models poition in the list e.g. 0 for gemma3:270m', 1 for gemma3:4b etc.
model_list = ['gemma3:270m', 'gemma3:4b', 'gemma3:12b', 'qwen3:4b']
MODEL_NAME = model_list[0]  # Set the Default model

All the Ai Tools use the same model that's selected in the dropdown.

```

## How does the app work?
- Ai Models
- Inference process
- How does pdf conversion work
- Adding new tools
- Click to run

## FAQ

## Lessons learned

## Resources

- Search Ollama models<br>
https://ollama.com/search

- Install UV<br>
https://docs.astral.sh/uv/getting-started/installation/#installation-methods

- How to create a single-file flask app<br>
https://github.com/vbookshelf/Single-File-Flask-Web-App


