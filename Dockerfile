FROM python
MAINTAINER Matthew.Crowell@Smoothstack.com
COPY . .
ENTRYPOINT ["python3", "main.py"]