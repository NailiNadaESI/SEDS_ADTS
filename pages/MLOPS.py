import streamlit as st
from streamlit_reveal_slides import st_reveal_slides 

st_reveal_slides(
        {
            "title": "MLOPS: Deploying and Monitoring ML Projects",
            "slides": [
                {
                    "content": "# MLOPS: Deploying and Monitoring ML Projects",
                },
                {
                    "content": "## Introduction",
                },
                {
                    "content": "### What is MLOPS?",
                    "subcontent": "MLOPS (Machine Learning Operations) is a set of practices that combines machine learning (ML) system development and machine learning system operations to deliver and manage ML applications efficiently.",
                },
                {
                    "content": "### Why MLOPS?",
                    "subcontent": "Ensures collaboration and communication between data scientists and operations teams. Enables automated and streamlined ML workflows from development to deployment.",
                },
                {
                    "content": "## Available Frameworks",
                },
                {
                    "content": "### 1. TensorFlow Extended (TFX)",
                    "subcontent": "TFX is an end-to-end platform for deploying production-ready ML models. It provides components for every step in the ML lifecycle, including data validation, model training, and serving.",
                },
                {
                    "content": "### 2. MLflow",
                    "subcontent": "MLflow is an open-source platform for managing the end-to-end ML lifecycle. It includes tools for tracking experiments, packaging code into reproducible runs, and sharing and deploying models.",
                },
                {
                    "content": "### 3. Kubeflow",
                    "subcontent": "Kubeflow is an open-source platform for deploying, monitoring, and managing ML models on Kubernetes. It provides components for building scalable, portable ML workflows.",
                },
                {
                    "content": "## Demo: Deploying a Model with TFX",
                },
                {
                    "content": "### Walkthrough of deploying a TensorFlow model using TFX.",
                    "subcontent": "Showcasing the steps involved in the deployment process using TFX.",
                },
                {
                    "content": "## Challenges in MLOPS",
                },
                {
                    "content": "### Model Versioning",
                    "subcontent": "Managing and tracking different versions of ML models.",
                },
                {
                    "content": "### Continuous Integration/Continuous Deployment (CI/CD)",
                    "subcontent": "Ensuring smooth and automated deployment pipelines for ML models.",
                },
                {
                    "content": "## Best Practices",
                },
                {
                    "content": "### Documentation and Monitoring",
                    "subcontent": "Importance of thorough documentation and continuous monitoring for ML systems.",
                },
                {
                    "content": "# Conclusion",
                },
                {
                    "content": "## Choose the Right Framework for Your ML Project",
                },
            ],
        }
)