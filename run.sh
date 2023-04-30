python3 to_be_download_files.py
echo "to_be_download_files DONE"
python3 extract.py
echo "extract DONE"

while read line
do
echo "Line:" $line

  for file in ./data/source_text/*
  do
      # commands to execute for each file
      echo "Processing file: $file"
      python3 nlp.py $file
      rm $file
  done
done < ./data/file_list.text

echo "nlp DONE"
python3 dedup_and_export.py
echo "DONE ALL"