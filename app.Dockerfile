FROM python:3.9

WORKDIR /code
ENV PYTHONPATH /code/app
COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN python -c 'from keras.applications import VGG16; VGG16(weights="imagenet", include_top=True)'
#
COPY ./app /code/app

#
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]