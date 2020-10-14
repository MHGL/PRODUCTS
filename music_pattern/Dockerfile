FROM python:3.7-slim
MAINTAINER liyang "liyang@deepait.com"

RUN apt-get update && \
    apt-get install -y libsndfile1 ffmpeg && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ --no-cache-dir flask tornado librosa requests tqdm spleeter==1.4.9

COPY . /workspace/music_pattern/
WORKDIR /workspace/music_pattern

EXPOSE 10080

CMD ["sh", "-c", "python server.py"]
