vosk-kalliope


This project goal is to be able to integrete the offline Speech-to-text tool VOSK to the vocal assistant Kalliope.


To use Vosk with kalliope, install VOSK, download the acoustic model corresponding to the language you want to use and then, clone vosk.py and _init_.py in ../python3.7/dist-packages/kalliope-0.6.1-py3.7.egg/kalliope/stt/vosk 
And finally, go to settings.yml of Kalliope and set the stt to vosk.
You may have to add 
  - vosk:
      language: "model-xx"
after cmusphinx line. Model-xx is the name of the model you use. If Kalliope can't find your model, go to vosk.py and specify the name and/or hard path to the model.

The link towards VOSK-API : https://github.com/alphacep/vosk-api
For more information about it or if you have any question, you can visit my web page : https://quotech-23.webself.net/accueil
