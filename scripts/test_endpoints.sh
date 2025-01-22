
# Test basic factorial endpoint
echo "Testing factorial endpoint with input 5..."
curl -s http://localhost:8080/factorial/5 | jq
# Sample output: {"result": 120}

# Test history endpoint with no filters
echo -e "\nGetting full history..."
curl -s http://localhost:8080/history | jq
# Sample output: [
#   {
#     "id": 2,
#     "input_number": 5,
#     "result": 120,
#     "created_at": "2024-01-21T15:30:25.123456"
#   },
#   {
#     "id": 1,
#     "input_number": 3,
#     "result": 6,
#     "created_at": "2024-01-21T15:30:20.123456"
#   }
# ]

# Test history with specific input number
echo -e "\nGetting history for input_number=5..."
curl -s "http://localhost:8080/history?input_number=5" | jq
# Sample output: [
#   {
#     "id": 2,
#     "input_number": 5,
#     "result": 120,
#     "created_at": "2024-01-21T15:30:25.123456"
#   }
# ]

# Test history with min_input filter
echo -e "\nGetting history for min_input=3..."
curl -s "http://localhost:8080/history?min_input=3" | jq
# Sample output: [
#   {
#     "id": 2,
#     "input_number": 5,
#     "result": 120,
#     "created_at": "2024-01-21T15:30:25.123456"
#   },
#   {
#     "id": 1,
#     "input_number": 3,
#     "result": 6,
#     "created_at": "2024-01-21T15:30:20.123456"
#   }
# ]

# Test history with max_input filter
echo -e "\nGetting history for max_input=5..."
curl -s "http://localhost:8080/history?max_input=5" | jq
# Sample output: [
#   {
#     "id": 2,
#     "input_number": 5,
#     "result": 120,
#     "created_at": "2024-01-21T15:30:25.123456"
#   },
#   {
#     "id": 1,
#     "input_number": 3,
#     "result": 6,
#     "created_at": "2024-01-21T15:30:20.123456"
#   }
# ]

# Test history with both min and max filters
echo -e "\nGetting history for min_input=3 and max_input=5..."
curl -s "http://localhost:8080/history?min_input=3&max_input=5" | jq
# Sample output: [
#   {
#     "id": 2,
#     "input_number": 5,
#     "result": 120,
#     "created_at": "2024-01-21T15:30:25.123456"
#   },
#   {
#     "id": 1,
#     "input_number": 3,
#     "result": 6,
#     "created_at": "2024-01-21T15:30:20.123456"
#   }
# ]

# Example error case
echo -e "\nTesting invalid input..."
curl -s http://localhost:8080/factorial/-1 | jq
# Sample output: {
#   "detail": "Input must be non-negative"
# }

# Test recursion limit error
echo -e "\nTesting very large input..."
curl -s http://localhost:8080/factorial/1000 | jq
# Sample output: {
#   "detail": "Input too large"
# }
