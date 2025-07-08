# 💵 Fake Indian Currency Detection using Xception Model

This project leverages deep learning and the **Xception** architecture to detect **fake Indian currency notes** using image classification. It aims to provide a reliable, fast, and accurate method for identifying counterfeit currency — a growing concern in the financial ecosystem.

---

## 📌 Features

- Detects **fake vs. real currency notes** using high-resolution image data.
- Utilizes **Xception**, a deep convolutional neural network pre-trained on ImageNet.
- Implements **transfer learning** for faster convergence and better accuracy.
- Achieves **high classification accuracy** (>90%) with minimal overfitting.
- Includes **image preprocessing**, **data augmentation**, and **evaluation metrics**.

---

## 🧠 Model Architecture

- **Base Model**: Xception (Extreme Inception) from Keras Applications.
- **Transfer Learning**: Used with pre-trained weights; top layers fine-tuned.
- **Custom Classifier Head**:
  - Global Average Pooling
  - Dropout
  - Dense layers with ReLU
  - Output layer with Softmax/Sigmoid

---

## 🗂️ Dataset

- Real & Fake Indian currency note images.
- Classes: `Real`, `Fake`
- Images preprocessed (resized, normalized).
- Augmented for robustness (rotation, zoom, flip, etc.).

> *Dataset source: Manually curated / Public datasets or Kaggle*

---

## ⚙️ Requirements

```bash
tensorflow
keras
numpy
matplotlib
opencv-python
scikit-learn
