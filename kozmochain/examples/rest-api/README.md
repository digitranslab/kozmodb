## Single command to rule them all,

```bash
docker run -d --name kozmochain -p 8080:8080 kozmochain/rest-api:latest
```

### To run the app locally,

```bash
# will help reload on changes
DEVELOPMENT=True && python -m main
```

Using docker (locally),

```bash
docker build -t kozmochain/rest-api:latest .
docker run -d --name kozmochain -p 8080:8080 kozmochain/rest-api:latest
docker image push kozmochain/rest-api:latest
```

