FROM python:3.6
RUN mkdir -p app
RUN mkdir -p app/data
WORKDIR ./app
COPY read-write-mjpg-display.py .
RUN pip install matplotlib
RUN pip install numpy
RUN pip install opencv-python
CMD ["python", "read-write-mjpg-display.py"]
