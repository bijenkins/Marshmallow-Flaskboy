# Marshmallow-Flaskboy

Create a simple RESTful API in flask with database access and seriaization validation.

### Prerequisites

Python 3+
sqllite

```
pip install -r requirements.txt
```
Currently set up to create a sqlite at /tmp/test.db


## Examples
First Terminal
```
python todo.py
 * Serving Flask app "todo" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
```

Second Terminal 
```
# Check our todo's
curl http://127.0.0.1:5000/todos
[]

# Add a Task
curl -d '{"description":"First Task!"}' -H "Content-Type: application/json" -X POST http://localhost:5000/todos
{
    "description": "First Task!",
    "id": 1
}

# Get all Tasks
curl http://127.0.0.1:5000/todos
[
    {
        "description": "First Task!",
        "id": 1
    }
]
```

## Authors

* **Billy Jenkins**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
