import speech_recognition as sr

import sys
import json
import os

from kalliope.core import Utils
from kalliope.stt.Utils import SpeechRecognition
from sys import version_info as _swig_python_version_info
if _swig_python_version_info < (2, 7, 0):
    raise RuntimeError("Python 2.7 or later required")
from kalliope.stt.Utils import KaldiRecognizer, Model, SpkModel
from speech_recognition import Microphone


class Vosk(SpeechRecognition, KaldiRecognizer, Model, SpkModel):

    def __init__(self, callback=None, **kwargs):
        """
        Start recording the microphone and analyse audio with Vosk
        :param callback: The callback function to call to send the text
        :param kwargs:
        """

        SpeechRecognition.__init__(self, kwargs.get('audio_file_path', None))


        self.main_controller_callback = callback
        self.language = kwargs.get('language', "model-fr")
        self.grammar_file = kwargs.get('grammar_file', None)

        self.set_callback(self.vosk_callback)
        self.start_processing()


    def vosk_callback(self, recognizer, audio_data):

        model = Model("model-fr")

        rec = KaldiRecognizer(model, 16000)

        upm = sr.Microphone()
        kl = sr.Recognizer()

        if not os.path.exists("model-fr"):
            print("Please download the model from https://github.com/alphacep/kaldi-android-demo/releases and unpack as 'model-fr' in the current folder.")
            exit (1)

        sl_data = audio_data.get_raw_data(convert_rate=16000, convert_width=2)   # the included language models require audio to be 16-bit mono 16 kHz format

        try:

            if len(sl_data) == 0:
                print ("len = 0")

            if rec.AcceptWaveform(sl_data):
               res = json.loads(rec.Result())

            res = json.loads(rec.FinalResult())
            captured_audio = res['text']
            Utils.print_success("Vosk thinks you said %s" % captured_audio)
            self._analyse_audio(captured_audio)


        except sr.UnknownValueError:
            Utils.print_warning("Vosk Speech Recognition could not understand audio")
            self._analyse_audio(audio_to_text=None)

        except sr.RequestError as e:
            Utils.print_danger("Could not request results from Vosk Speech Recognition service; {0}".format(e))
            self._analyse_audio(audio_to_text=None)

        except AssertionError:
            Utils.print_warning("No audio caught from microphone")
            self._analyse_audio(audio_to_text=None)


    def _analyse_audio(self, audio_to_text):
        """
        Confirm the audio exists and run it in a Callback
        :param audio_to_text: the captured audio
        """
        if self.main_controller_callback is not None:
            self.main_controller_callback(audio_to_text)
