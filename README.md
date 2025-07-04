# 🎙️ Personal Task Voice Assistant

[![LangGraph](https://img.shields.io/badge/Built%20With-LangGraph-blue?logo=python)](https://github.com/langchain-ai/langgraph)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-brightgreen?logo=openai)](https://platform.openai.com/docs/guides/gpt)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-success.svg)](#)

Your **AI-powered personal assistant** that helps you create, manage, and organize your to-do list using **natural voice commands**. This voice-enabled task manager leverages **LangGraph**, **OpenAI**, and **TrustCall extractors** to make intelligent updates to your task memory and provide conversational task assistance.

---

## 📂 Project Structure

```
TASK_MAISTRO/
│
├── .langgraph_api/            # LangGraph local dev cache
├── Assistant/                 # Main assistant logic and components
│   ├── prompts/              # Prompt templates for LLM
│   └── utils/                # Utility modules
│       ├── configuration.py  # Configuration schema (user ID, category, role)
│       ├── nodes.py          # LangGraph node logic for updates
│       ├── schema.py         # Pydantic schemas for messages and memory
│       ├── tools.py          # TrustCall tools (Profile, ToDo, etc.)
│       ├── utils.py          # Helper utilities
│       └── __init__.py
│
├── agent.py                  # Entry point for the voice assistant
├── langgraph.json            # LangGraph configuration
├── requirements.txt          # Python dependencies
├── LICENSE
└── README.md
```

---

## ✨ Features

* 🎤 **Voice Interaction** — Speak your tasks naturally using a microphone.
* 🤖 **Memory-aware Assistant** — Remembers your profile, tasks, and instructions.
* 🧠 **LLM + Tools** — Integrates OpenAI + TrustCall extractors to keep your memory updated.
* 🔄 **Auto-updates Profile & ToDos** — Reflects on conversation and updates memory store.
* 🗂️ **Organized by Category** — Tasks and memories are scoped per user and category.

---

## 🚀 Quick Start

1. **Clone the repository**

```bash
git clone https://github.com/<your-username>/Personal_Task_Voice_Assistant.git
cd Personal_Task_Voice_Assistant
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Set environment variables**
   Create a `.env` file in the root directory:

```
OPENAI_API_KEY=your-api-key
```

4. **Run the assistant**

```bash
python Assistant/agent.py
```

> 🎙️ Speak into your mic — your assistant will transcribe, respond, and update your to-do list in real-time.

---

## 🧩 LangGraph Flow

Your LangGraph is composed of the following nodes:

* **`audio_input`**: Records your voice and transcribes it.
* **`task_maistro`**: Analyzes memory and prompts the LLM for task understanding.
* **`update_profile`, `update_todos`, `update_instructions`**: Update memory based on extracted tool calls.
* **`audio_output`**: Converts LLM response to voice and plays it.

Decision routing is handled by:

```python
route_message() → returns one of: END, update_profile, update_todos, update_instructions
```

---

## 🛠️ Built With

* [LangGraph](https://github.com/langchain-ai/langgraph)
* [OpenAI GPT-4o](https://platform.openai.com/docs/guides/gpt)
* [TrustCall Extractors](https://docs.langchain.com/docs/components/extractors/)
* [SoundDevice](https://python-sounddevice.readthedocs.io/) for audio input
* [Scipy.io.wavfile](https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.write.html) for handling WAV files

---

## 🧪 Example Conversation

> **You**: “Hey, can you help me with some of the tasks I need to complete tomorrow?”
>
> **Assistant**: “Sure! What tasks would you like me to note?”
>
> **You**: “Read about MCP servers and finish my NLP assignment.”
>
> ✅ To-do list updated.

---

## 🧠 Memory System

All memories are stored using a tuple key:

```python
namespace = (type, category, user_id)
```

Types include:

* `"profile"` – stores user preferences and bio.
* `"todo"` – tasks and notes.
* `"instructions"` – fine-tuning how the assistant should behave.

---

## 🧑‍💻 Contributing

Pull requests are welcome! Please fork the repo and submit a PR. For major changes, open an issue first to discuss your proposal.

---

## 📄 License

This project is licensed under the terms of the [MIT License](LICENSE).

---

## 🙌 Acknowledgments

Special thanks to:

* The LangChain team for LangGraph
* OpenAI for providing the Whisper and GPT-4o APIs
