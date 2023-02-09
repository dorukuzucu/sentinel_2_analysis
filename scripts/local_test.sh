curl -X GET -H "Content-Type: application/json" http://127.0.0.1:8000/operations
echo "\n"
curl -X POST -H "Content-Type: application/json" -d '{"name": "MEAN_VALUE"}' http://127.0.0.1:8000/analyze
echo "\n"
