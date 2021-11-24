# minimal dockerfile to make the script usable without the hassle of installing sage globally
FROM sagemath/sagemath

WORKDIR /app
COPY . .
CMD ["sage", "graphAssessment.py", "-task", "PLANARITY", "-file", "resources/graph.json"]