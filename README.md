# Tone Assistant

*A letter holds a thousand emotions.*

![Logo](image1) <!-- Replace with actual image link -->

## **Name**: Mohammad Ashraful Huq

## **SI**: 297856

## Table of Contents

1. [Use Case](#1-use-case)
2. [Defining the LLM Models](#2-defining-the-llm-models)
3. [Dataset Preparation](#3-dataset-preparation)
4. [Model Training](#4-model-training)
   - [Fine-Tuning BERT](#41-fine-tuning-bert)
   - [GPT-3.5 Turbo API Usage](#42-gpt-35-turbo-api-usage)
5. [User Guide](#5-user-guide)
   - [Installation](#51-installation)
   - [Usage](#52-usage)
6. [Future Works](#6-future-works)

## 1. Use Case

Professional communication is an essential part of our day-to-day life. However, often emotion gets the best of us. We write messages that are often passive-aggressive, angry, or confused in tone. Such messages can greatly thwart collaboration and goodwill.

We are what we speak. So, it is necessary to keep our tone and words in check. That is why we present our tool, **Tone Assistant**. With this tool, users can write their message and, before sending it, check the tone of the message and rephrase it if necessary.

## 2. Defining the LLM Models

We use two models for our project:

| Use Case                | Model Name         | Parameters   | Comments                                  |
|-------------------------|--------------------|--------------|-------------------------------------------|
| Message tone analysis    | Fine-Tuned BERT    | 343.3 million | Faster and at zero cost                   |
| Rephrasing message       | GPT-3.5-turbo      | 20 billion    | Cheaper alternative to GPT-4              |

The reason for the difference is that the message tone analysis task will be executed frequently when a user is texting. Therefore, it is necessary to make it faster and cheaper. We provide a locally deployed fine-tuned LLM for tone analysis.

Conversely, rephrasing message tasks are expected to be less frequent unless the person is having a very "fake" conversation with someone. Fake conversations are less frequent, and quality matters in those few cases. Thus, we use GPT-3.5 Turbo to ensure high quality while being overall low cost due to low usage.

## 3. Dataset Preparation

We use the airline complaints tweets dataset, which contains 1700 positive and 1700 negative sentiment tweets. The dataset can be found in [this publicly shared drive](https://drive.google.com/uc?export=download&id=1wHt8PsMLsfX5yNSqrt2fSTcb8LEiclcf).

![Dataset Example](image2) <!-- Replace with actual image link -->

To process the data, we remove Twitter account names (e.g., @united) since they have no effect on the sentiment of a tweet. Additionally, we remove any trailing spaces and @ signs.

![Data Cleaning](image3) <!-- Replace with actual image link -->

## 4. Model Training

### 4.1 Fine-Tuning BERT

We take a 30-70 test-train split to train our dataset.

![Training Split](image4) <!-- Replace with actual image link -->

We use the pretrained model **bert-base-uncased**. A corresponding tokenizer is used to tokenize our dataset. The maximum token length is 128 because BERT was trained on 128-token sequences 90% of the time. This provides better generalization and performance on shorter sequences. While a maximum limit of 512 tokens exists, BERT was trained on long sequences only 10% of the time to reduce computational costs and time.

![BERT Tokenization](image5) <!-- Replace with actual image link -->

We define `BertForSequenceClassification` with 2 output neurons since we want either a positive or negative output.

![Model Definition](image6) <!-- Replace with actual image link -->

We use checkpointing to ensure that progress is not lost irrespective of any issues we might encounter.

![Checkpointing](image7) <!-- Replace with actual image link -->

We save progress after each epoch. We were limited to a total of 3 epochs due to time constraints. Our model finally achieved a validation accuracy of 81%, which is quite satisfactory for our task.

![Training Accuracy](image8) <!-- Replace with actual image link -->

We save our model for local use.

### 4.2 GPT-3.5 Turbo API Usage

We access GPT-3.5 Turbo through its API endpoint. We perform prompt engineering using the following command:

```plaintext
TASK = "You are an email message processor. Given an email message and an emotion, you will update the email according to the emotion."
prompt = f"Email: {request.email}\\nEmotion: {request.emotion}"
```

## API Usage

The API returns rephrased email content based on the specified emotion.

## 5. User Guide

### 5.1 Installation

Ideally, it will be a website that users can simply browse. However, if they wish to host it locally, they simply need to download the codebase and execute the following commands:

```bash
pip install -r requirements.txt
uvicorn server:app --reload
```
[Download Model Files](https://drive.google.com/drive/folders/10MQrGYna-QdxuO3P87YuOQBHZhrokAy2?usp=drive_link)

### 5.2 Usage

Since Tone Assistant is just an auxiliary tool in users’ daily workflow, we keep the GUI minimal.

![Usage Scenario](image_link) <!-- Replace with actual image link -->

The above usage scenario can be described as follows:

1. The user writes their email or message in the textbox.
2. They click on “**Analyze Sentiment**.”
3. If the sentiment does not align with their goal, they can choose to rephrase the message.
4. They select any emotion (e.g., Happy) to which the message tone will transform.
5. They click “**Rephrase Message**” to receive a rephrased message with a Happy tone.

### 6. Future Works

This tool can be seamlessly integrated into the user's workflow, much like Grammarly. Additionally, the AI assistant can keep a map of the user's relationships to automatically infer what tone the user should prefer when writing a message. To ensure personalization, the AI should learn the user's writing style and attempt to mimic it as closely as possible.

