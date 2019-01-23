### Build image

```
$ docker build --no-cache -t mmlu_test_cv2:v0.1 .
```

### Run container
```
$ docker run -d -e http_proxy=$http_proxy -e https_proxy=$https_proxy -v ~/Workspace:/app/data mmlu_test_cv2:v0.1
```
