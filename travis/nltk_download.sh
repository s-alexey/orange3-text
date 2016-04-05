#!/usr/bin/env bash
data=( "wordnet" "stopwords" "snowball_data" )

for d in "${data[@]}"
do
    python -m nltk.downloader $d;
done

echo "Contents of NLTK data folder:"
ls $HOME/nltk_data;
