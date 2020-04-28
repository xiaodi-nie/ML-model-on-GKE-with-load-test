#!/usr/bin/env bash

PORT=8080
echo "Port: $PORT"

# POST method predict
curl -d '{
          "Pclass": {
            "0": 1
          },
          "Sex": {
            "0": 1
          },
          "Age": {
            "0": 5
          },
          "Fare": {
            "0": 3
          },
          "Embarked": {
            "0": 1
          },
          "relatives": {
            "0": 1
          },
          "Deck": {
            "0": 3
          },
          "Title": {
            "0": 3
          }
        }'\
     -H "Content-Type: application/json" \
     -X POST http://localhost:$PORT/predict
