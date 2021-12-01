unzip submission.zip -d ./ >/dev/null

rm submission.zip

for FILE in submission/*; do
    mv $FILE eval/
done


cd eval/
python3 ./evaluate.py instance1
cd ../
