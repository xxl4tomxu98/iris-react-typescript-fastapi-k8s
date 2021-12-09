# FastAPI Server

The API was created with FastAPI ([FastAPI website](https://fastapi.tiangolo.com/)), a modern web framework which allows build APIs, in this case to deploy machine learning models. The key FastAPI features are:

- Fast: Very high performance, on par with Node.js and Go, so it is one of the fastest Python frameworks available.
- Intuitive: Great editor support.
- Easy: Designed to be easy and learn.
- Robust: Get production-ready code with automatic interactive documentation.
- Standard-based: Based on (and fully compatible with) the open standards for APIs: OpenAPI and JSON Schema.

To run our API we need to use uvicorn (in this specific case) to serve our API, the command is shown below:

```shell
uvicorn main:app
```

However, since this command is already in main.py, run main.py should be sufficient. Details of the implementation please refer to [How to use Python and FastAPI to Deploy Machine Learning Models on Heroku](https://python.plainenglish.io/how-to-use-python-and-fastapi-to-deploy-machine-learning-models-on-heroku-61b96271d5b3)
