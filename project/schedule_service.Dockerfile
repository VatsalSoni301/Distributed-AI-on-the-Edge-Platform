FROM commondocker

WORKDIR /schedule_service
COPY schedule_service.py .
COPY Logger.py .

ENTRYPOINT ["python3"]
CMD ["schedule_service.py"]