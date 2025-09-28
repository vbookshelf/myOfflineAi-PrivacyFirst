# myOfflineAi - A Flask UI for Ollama

Transparent offline Ai access for those who need extreme data privacy and don't want to blindly trust cloud providers and software developers.

- Ai access without an internet connection
- Runs on the desktop.
- Chat with Ollama models
- Create custom multimodal Ai tools - text, images, pdf (Similar to Gemini Gems and OpenAi GPTs)
- Chat histories are not saved
- Built to be transparent. Single-file flask app. Therefore, it's easy to audit the code.
- No need to use the command line. Simply double click a file to launch the app in your browser.

<br>

<img src="https://github.com/vbookshelf/myOfflineAi/blob/main/images/image1.png" alt="App screenshot" height="500">

<br>

## What problem does this solve?

Most of us take it for granted that we can drop a document into Google Translate or ChatGPT without a second thought. But what if that document is your grandmother’s secret recipe? Or a client’s legal brief? Or a patient’s medical chart? For many people, uploading such things to the cloud is a risk. A single upload could expose sensitive data, waive attorney–client privilege, or violate medical privacy laws. That fear prevents many from benefiting from the power of AI to help them be more productive and to serve more people.

Large firms can buy their way out of this problem with costly, enterprise-grade privacy systems. But the solo lawyer, the therapist in private practice, the small nonprofit cannot.
Open source, offline, privacy-first AI solves this problem. The data never leaves the user’s computer. And there's full transparency - all the underlying code for the app can be audited for data privacy compliance. Also, the user's internet connection can be disconnected while the app is being used - creating peace of mind.

<br>


## Current state of small local Ai models

Currently, if you want to run AI models locally, say on a machine with 16GB RAM, you are restricted to using small models. The bottom line is that these models are not trustworthy. They are okay for non-crtical work like translation, summarization and brainstorming. But their ability to hallucinate makes them unsuitable for high precision work.

That said, the most recent small models, like Gemma3, have very good qualities: They are multilingual. They are multimodal meaning that they can handle both text and images. And they run quite fast on a CPU. Some, like the Qwen3 models, also have the ability to reason internally i.e. they are thinking models.

Trustworthy local Ai is not a reality yet, but the day when it will be is coming fast. myOfflineAi is designed so that when that day comes you can hit the ground running.

<br>

## Limitations
- Hallucinations
- Slow response time to first message when processing pdf documents and images
- Limited to using small models


## How to Install and Run the app

I tested the installation process on Mac OS. Please note that although I've included instructions for Windows, I haven't tested on Windows.

In this section you will be installing the requirements. You will also be downloading a model thats 3.3GB. You'll need to have a computer with approx. 8GB of RAM. You will also need to have a good internet connection. If you have one of the newer M series Macs with 16GB RAM, you will be fine.

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
1. Download and install the Ollama desktop application
This is the link to download Ollama. After downloading it install in on your computer.
https://ollama.com/

2. Download an Ollama model
If you have a good intenet connection and at least 8GB RAM then download the gemma3:4b model (2.5GB). This model can handle both text and images.
If you have a slow connection then download the smaller gemma3:270m model (292MB). This model can handle text only.

Open the Ollama desktop app. Paste the model name (e.g. gemma3:270m) into the dropdown in the bottom right. Then type any message e.g. Hi.
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

4. Download the project folder<br>
Download the project folder from this repo.

5. Open the folder and double-click a file.
This will install all the python packages (first time only).
Then it will auto open the myOfflineAi web app in your browser.
The terminal will also open.

Mac:
Double-click start-app.command

Windows:
Double-click start-app.bat

5. Use the app
The name of the model you download will appear in the dropdown in the top left.
Click on "AI Assistant"
Type a mesage.
If you downloaded the gemma3:4b you can also submit images and pdf documents.<br>
The app converts pdf docs into images before processing.


5. Future

This set up process above only needs to be done once.
In future to start the app do the following:

1- The Ollama desktop app auto launches when you start your computer.
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

1- Is it essential to switch off the internet connection?<br>
No it's not essential. By design, no data leaves your device. But I recommend putting Ollama into Airplane mode. This can be done in the Ollama settings.

2- How do I audit the code for privacy?

3- How do I add features, make changes or fix a bug?
This is a single-file app thats designed to be reviewed and modified by Ai. All the code is in one file so the Ai sees the entire design. Simply take the app.py file and upload it to Gemini 2.5 Pro, Claude Sonnet or GPT-5. Tell it what changes or new features you want. Also tell it to output all the code on one page so you can copy and paste it. When the Ai outputs the revised code, copy it and replace all the code in the app.py file. Then put the app.py file back inside the project folder. Launch the app and check if your changes have been made.

## Lessons learned
- Ollama models have a default context size of 4096. Knowing this will help you get much better results.
- When using Gemma models images come before text.
- The best coding models are Gemini 2.5 Pro and Claude Sonnet.

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

## Appendix

1- How to load your own models into Ollama

bartowski/google_medgemma-4b-it-GGUF<br>
https://huggingface.co/bartowski/google_medgemma-4b-it-GGUF

