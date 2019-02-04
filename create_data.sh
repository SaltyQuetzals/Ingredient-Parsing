#!/bin/zsh

echo "Booting Docker container..."
docker run -d -t --name=ipt mtlynch/ingredient-phrase-tagger
python3 split_data.py

echo "Copying CSV files..."
docker cp data/train.csv ipt:/app/train.csv
docker cp data/valid.csv ipt:/app/valid.csv
docker cp data/test.csv ipt:/app/test.csv

echo "Generating tags..."
docker exec ipt bin/generate_data --data-path=train.csv > data/train.tags
docker exec ipt bin/generate_data --data-path=valid.csv > data/valid.tags
docker exec ipt bin/generate_data --data-path=test.csv > data/test.tags

echo "Converting tagfiles to sequence tagging files..."
python3 convert_to_seqtag_file.py data/train.tags data/train.seqtags
python3 convert_to_seqtag_file.py data/valid.tags data/valid.seqtags
python3 convert_to_seqtag_file.py data/test.tags data/test.seqtags

echo "Cleaning up..."
docker stop ipt
docker container rm ipt
rm -rf data/*.tags