#!/bin/zsh


echo "Booting Docker container..."
docker run -dt --name=ipt mtlynch/ingredient-phrase-tagger

echo "Pre-emptively generating test input..."
python3 test_txt.py

echo "Copying necessary inputs to Docker..."
docker cp data/train.csv ipt:/app/train.csv
docker cp data/test.txt ipt:/app/input.txt

echo "Generating tags..."
docker exec ipt mkdir tmp
docker exec ipt sh -c "bin/generate_data --data-path=train.csv > tmp/train_file"
mkdir data/crf_results
docker exec ipt bin/generate_data --data-path=test.csv > data/crf_results/test.tags

echo "Training CRF++..."
docker exec ipt crf_learn template_file tmp/train_file tmp/model_file

echo "Finished training CRF++, testing..."
docker exec ipt sh -c "python bin/parse-ingredients.py input.txt > results.txt"

echo "Finished testing, copying results back..."
docker cp ipt:/app/results.txt data/crf_results/results.txt

echo "Cleaning up..."
docker kill ipt
docker container rm ipt