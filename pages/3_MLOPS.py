import streamlit as st
import reveal_slides as rs

sample_markdown = r"""
# MLOPS
---
## What is MLOps?
MLOps, or Machine Learning Operations, is a pivotal component within the realm of Machine Learning engineering. It is dedicated to streamlining the entire lifecycle of deploying machine learning models into production and managing them thereafter. This multifaceted function relies on collaboration among diverse roles, such as data scientists, devops engineers, and IT professionals, to ensure a cohesive and efficient approach to deploying and maintaining machine learning models.
---
## Why MLOPS?
- Efficiency and Automation. <!-- .element: class="fragment" data-fragment-index="0" -->
- Reproducibility and Collaboration. <!-- .element: class="fragment" data-fragment-index="1" -->
- Scalability and Deployment. <!-- .element: class="fragment" data-fragment-index="2" -->
-  Continuous Improvement.<!-- .element: class="fragment" data-fragment-index="3" -->
---
## Kubeflow :
\[[KubeFlow](https://www.kubeflow.org/)\] is an end-to-end Machine Learning (ML) platform for Kubernetes, it provides components for each stage in the ML lifecycle, from exploration through to training and deployment. Operators can choose what is best for their users, there is no requirement to deploy every componen

---
## Kubeflow componants: :
- Kubeflow Piplines: it is a platform for building then deploying portable and scalable machine learning workflows using Kubernetes.<!-- .element: class="fragment" data-fragment-index="0" -->
- Kubeflow Notebooks: lets you run web-based development environments on your Kubernetes cluster by running them inside Pods.<!-- .element: class="fragment" data-fragment-index="1" -->
- Kubeflow Central Dashboard :a hub which connects the authenticated web interfaces of Kubeflow and other ecosystem components. <!-- .element: class="fragment" data-fragment-index="2" -->
---
## Adventages:
- **End-to-End Orchestration.** <!-- .element: class="fragment" data-fragment-index="0" -->
- **Integration with TensorFlow and Other Frameworks.**<!-- .element: class="fragment" data-fragment-index="1" -->
- **Modular Components.** <!-- .element: class="fragment" data-fragment-index="2" -->
---

## Disadventages:
- **Resource Intensive.**  <!-- .element: class="fragment" data-fragment-index="0" -->
- **Dependency on Kubernetes.**<!-- .element: class="fragment" data-fragment-index="1" -->
- **Initial Setup Complexity**<!-- .element: class="fragment" data-fragment-index="2" -->
---
##  Apache Airflow:
\[[Apache Airflow](https://airflow.apache.org/)\] is an open-source platform for orchestrating complex workflows, including data preparation, model training, and deployment.it is a platform to programmatically author, schedule, and monitor workflows.
---
## Adventages:
- **Pure Python.** <!-- .element: class="fragment" data-fragment-index="0" -->
- **Open Source.**<!-- .element: class="fragment" data-fragment-index="1" -->
- **Extensibility.** <!-- .element: class="fragment" data-fragment-index="2" -->
---

## Disadventages:
- **Learning Curve.**  <!-- .element: class="fragment" data-fragment-index="0" -->
- **Web UI Limitations.**<!-- .element: class="fragment" data-fragment-index="1" -->
---
## DVC  (Data Version Control):
\[[DVC](https://dvc.org/)\] iData version control is a method of working with data sets. It is similar to the version control systems used in traditional software development, but is optimized to allow better processing of data and collaboration in the context of data analytics, research, and any other form of data analysis.
---
## DVC componants: :
- GenAI data chain: To Explore and enrich annotated datasets with custom embeddings, auto-labeling, and bias removal at billion-file scale — without modifying your data..<!-- .element: class="fragment" data-fragment-index="0" -->
- Data and Model versioning: ToConnect to versioned data sources and code with pipelines, track experiments, register models — all based on GitOps principles.<!-- .element: class="fragment" data-fragment-index="1" -->

---
## Adventages:
- **FREE.** <!-- .element: class="fragment" data-fragment-index="0" -->
- **Integration with Existing Tools.**<!-- .element: class="fragment" data-fragment-index="1" -->
- **Modular Components.** <!-- .element: class="fragment" data-fragment-index="2" -->
---
## Disadventages:
- **Community Size.**  <!-- .element: class="fragment" data-fragment-index="0" -->
- **Smaller Ecosystem.**<!-- .element: class="fragment" data-fragment-index="1" -->
---
## La fin
"""
st.markdown("## Presentation about MLOPS")
with st.sidebar:
    st.header("Component Parameters")
    theme = st.selectbox("Theme", ["black", "black-contrast", "blood", "dracula", "moon", "white", "white-contrast", "league", "beige", "sky", "night", "serif", "simple", "solarized"])
    height = st.number_input("Height", value=500)
    scale_range = st.slider("Scale Range", min_value=0.0, max_value=5.0, value=[0.1, 3.0], step=0.1)
    margin = st.slider("Margin", min_value=0.0, max_value=0.8, value=0.1, step=0.05)
    transition = st.selectbox("Transition", ["slide", "convex", "concave", "zoom", "none"])
    plugins = st.multiselect("Plugins", ["highlight", "katex", "mathjax2", "mathjax3", "notes", "search", "zoom"], [])
    st.subheader("Initial State")
    hslidePos = st.number_input("Horizontal Slide Position", value=0)
    vslidePos = st.number_input("Vertical Slide Position", value=0)
    fragPos = st.number_input("Fragment Position", value=-1)
    overview = st.checkbox("Show Overview", value=False)
    paused = st.checkbox("Pause", value=False)

# Add the streamlit-reveal-slide component to the Streamlit app.                    
currState = rs.slides(sample_markdown, 
                    height=height, 
                    theme=theme, 
                    config={
                            "transition": transition, 
                            "minScale": scale_range[0], 
                            "center": True, 
                            "maxScale": scale_range[1], 
                            "margin": margin, 
                            "plugins": plugins
                            }, 
                    initial_state={
                                    "indexh": hslidePos, 
                                    "indexv": vslidePos, 
                                    "indexf": fragPos, 
                                    "paused": paused, 
                                    "overview": overview 
                                    }, 
                    markdown_props={"data-separator-vertical":"^--$"}, 
                    key="foo")

