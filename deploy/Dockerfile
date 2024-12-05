FROM public.ecr.aws/lambda/python:3.10

# Set up workspace
RUN mkdir -p /workspace
WORKDIR /workspace

# Install Python packages from requirements.txt and konlpy
COPY requirements.txt .
RUN pip install -r requirements.txt


# Set the working directory for the model
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy model code and entry point
COPY lambda_function.py .
COPY cosine_sim.pkl .
COPY video_df.pkl .

# Set the entry point to use the virtual environment's Python
CMD [ "lambda_function.handler" ]