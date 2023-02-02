# Hinglish

## Setup
To set up the backend do the following :
1. Make a virtual enviornment
```
python3 venv -m env
```
2. Download all the required packages
```
pip install -r requirements.txt
```
3. Clone the indicTrans repository in the same folder
```
git clone https://github.com/DataGov-SamagraX/indicTrans.git
```
4. Download the model weights using
```
!wget "https://ai4b-my.sharepoint.com/:u:/g/personal/sumanthdoddapaneni_ai4bharat_org/ETnq-z4aHXFAjDF1Te3AZ20BaZ59PwlKlzSemEHhrmYJ3w?e=fg3s9y&download=1" --output-document=en-indic.zip
```
```
!wget "https://ai4b-my.sharepoint.com/:u:/g/personal/sumanthdoddapaneni_ai4bharat_org/EUOJ3irrwzFGnEnlPWHgaYkBugAQz25bPFgRvCPW8k7qtg?e=vvCP3u&download=1" --output-document=indic-en.zip
```
5. Unzip the downloaded folders
```
mkdir en-indic
cd en-indic
unzip "../en-indic.zip"
mkdir ../indic-en
cd ../indic-en
unzip "../indic-en.zip"
cd ..
```
6. Start the Flask development server using
```
export FLASK_APP=app.py
flask run
```