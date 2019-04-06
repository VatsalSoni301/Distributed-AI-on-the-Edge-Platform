FROM commondocker

WORKDIR /deploy_service
COPY deploy_service.py .
COPY Logger.py .

ENTRYPOINT ["python3"]
CMD ["deploy_service.py"]