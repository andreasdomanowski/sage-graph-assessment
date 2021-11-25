# minimal dockerfile to make the script usable without the hassle of installing sage globally
FROM sagemath/sagemath

WORKDIR /app
COPY . .
RUN sage -pip install bottle
CMD ["sage", "minimalWebserver.py"]