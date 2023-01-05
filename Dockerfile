FROM public.ecr.aws/lambda/python:3.9
COPY /file1.py ${LAMBDA_TASK_ROOT}
COPY /app.py ${LAMBDA_TASK_ROOT}
# COPY ./config.py ${LAMBDA_TASK_ROOT}

# COPY . ${LAMBDA_TASK_ROOT}

COPY requirements.txt  .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

CMD ["/app.handler"]