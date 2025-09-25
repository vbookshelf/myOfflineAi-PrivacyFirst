# myOfflineAi - A Flask UI for Ollama

Transparent offline Ai access for those who need extreme data privacy, but don't want to blindly trust the software developer.

- Chat with Ollama models
- Create multimodal Ai tools
- Local. Transparent. Free.
- Users don't need to trust, because they have complete control.

myOfflineAi is a single-file Flask app - HTML, CSS, JS and Python code are all in one file (app.py). This makes the code easy to audit. 

It also makes it easy for Ai models like Gemini, ChatGPT and Claude to modify the code to add new features to the app. Simply give the Ai model the app.py file and tell it what changes or what new feature you want. In the AI age, software no longer has to be one-size-fits-all.


<br>

<img src="https://github.com/vbookshelf/myOfflineAi/blob/main/images/image1.png" alt="App screenshot" height="500">

<br>

## What problem does this solve?

<img src="https://github.com/vbookshelf/myOfflineAi/blob/main/images/image2.png" alt="Grandmother using a laptop" height="300">

Most of us take it for granted that we can drop a document into Google Translate or ChatGPT without a second thought. But what if that document is your grandmother’s secret recipe? Or a client’s legal brief? Or a patient’s medical chart? For many people, uploading such things to the cloud is a a risk. A single upload could expose sensitive data, waive attorney–client privilege, or violate medical privacy laws. That fear prevents many from benefiting from the power of AI to help them be more productive and to serve more people.

Large firms can buy their way out of this problem with costly, enterprise-grade privacy systems. But the solo lawyer, the therapist in private practice, the small nonprofit cannot.
Open source, offline, privacy-first AI solves this problem. The data never leaves the user’s computer. And there's full transparency - all the underlying code for the app can be audited for data privacy compliance. Also, the user's internet connection can be disconnected while the app is being used - creating trust and peace of mind.

## What is myOfflineAi?

myOfflineAi is a privacy-first Flask UI for Ollama AI models. The user has complete control and there's total transparency. The app runs offline. CSS and JS code is stored locally. Therefore, the internet connection can be switched off. Additionally, the Ollama app that serves the model can be put in Airplane mode. This ensures data privacy.

## Features

- Single-File app: Html, CSS, JS and Python code are all in one file named app.py
- Full transparency: No black box. Users can inspect the code themselves or give the app.py file to an LLM and ask it to explain exactly what the code does. For example: When you submit an image to a Gemma model and ask it what's on the image - does the code put your text question first or the image first? That order affects the quality of the Gemma model's response. (It should be image first.)
- Customizable: Because its a single-file app, it's easy to use ChatGPT, Gemini or Claude to make code changes and add features.
- Data privacy: Uses on-device Ollama models. Runs offline. Does not save anything.
- Multimodal: Supports image and pdf input. Processes pdf pages as images, for greater accuracy.
- Custom tools: The user can create custom Ai tools - similar to Gemini Gems and OpenAi GPTs.

<br>

## Limitations

## How to Install

## FAQ

## Lessons learned

## Resources


