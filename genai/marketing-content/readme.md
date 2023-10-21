## Run the content generation

1. [Create Docker file](Dockerfile)
2. Build the docker image. Navigate to the file directory where your python code is saved.
    ```
     docker build -t kukreti12/llm:v2 .
     ```
3. Run the docker image. Pass the env variable i.e OPENAI_API_KEY
    ```
     docker run -d  -p 8501:8501 -e OPENAI_API_KEY="" kukreti12/llm:v2
     ```