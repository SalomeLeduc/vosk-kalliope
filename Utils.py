from threading import Thread

import logging
import speech_recognition as sr

from kalliope import Utils, SettingLoader

from sys import version_info as _swig_python_version_info
if _swig_python_version_info < (2, 7, 0):
    raise RuntimeError("Python 2.7 or later required")

# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _vosk
else:
    import _vosk

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

logging.basicConfig()
logger = logging.getLogger("kalliope")


class SpeechRecognition(Thread):

    def __init__(self, audio_file=None):
        """
        Thread used to caught n audio from the microphone and pass it to a callback method
        """
        super(SpeechRecognition, self).__init__()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.callback = None
        self.stop_thread = None
        self.kill_yourself = False
        self.audio_stream = None

        # get global configuration
        sl = SettingLoader()
        self.settings = sl.settings

        if audio_file is None:
            # audio file not set, we need to capture a sample from the microphone
            with self.microphone as source:
                if self.settings.options.adjust_for_ambient_noise_second > 0:
                    # threshold is calculated from capturing ambient sound
                    logger.debug("[SpeechRecognition] threshold calculated by "
                                 "capturing ambient noise during %s seconds" %
                                 self.settings.options.adjust_for_ambient_noise_second)
                    Utils.print_info("[SpeechRecognition] capturing ambient sound during %s seconds" %
                                     self.settings.options.adjust_for_ambient_noise_second)
                    self.recognizer.adjust_for_ambient_noise(source,
                                                             duration=self.settings.
                                                             options.adjust_for_ambient_noise_second)
                else:
                    # threshold is defined manually
                    logger.debug("[SpeechRecognition] threshold defined by settings: %s" %
                                 self.settings.options.energy_threshold)
                    self.recognizer.energy_threshold = self.settings.options.energy_threshold

                Utils.print_info("[SpeechRecognition] Threshold set to: %s" % self.recognizer.energy_threshold)
        else:
            # audio file provided
            with sr.AudioFile(audio_file) as source:
                self.audio_stream = self.recognizer.record(source)  # read the entire audio file

    def run(self):
        """
        Start the thread that listen the microphone and then give the audio to the callback method
        """
        if self.audio_stream is None:
            Utils.print_info("Say something!")
            try:
                with self.microphone as source:
                    logger.debug("[SpeechRecognition] STT timeout: %s" % self.settings.options.stt_timeout)
                    self.audio_stream = self.recognizer.listen(source, timeout=self.settings.options.stt_timeout)
            except sr.WaitTimeoutError:
                logger.debug("[SpeechRecognition] timeout reached while waiting for audio input")
                self.audio_stream = None
            logger.debug("[SpeechRecognition] end of speech recognition process")

        self.callback(self.recognizer, self.audio_stream)

    def start_processing(self):
        """
        A method to start the thread
        """
        self.start()

    def set_callback(self, callback):
        """
        set the callback method that will receive the audio stream caught by the microphone
        :param callback: callback method
        :return:
        """
        self.callback = callback

def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)


def _swig_setattr_nondynamic_instance_variable(set):
    def set_instance_attr(self, name, value):
        if name == "thisown":
            self.this.own(value)
        elif name == "this":
            set(self, name, value)
        elif hasattr(self, name) and isinstance(getattr(type(self), name), property):
            set(self, name, value)
        else:
            raise AttributeError("You cannot add instance attributes to %s" % self)
    return set_instance_attr


def _swig_setattr_nondynamic_class_variable(set):
    def set_class_attr(cls, name, value):
        if hasattr(cls, name) and not isinstance(getattr(cls, name), property):
            set(cls, name, value)
        else:
            raise AttributeError("You cannot add class attributes to %s" % cls)
    return set_class_attr


def _swig_add_metaclass(metaclass):
    """Class decorator for adding a metaclass to a SWIG wrapped class - a slimmed down version of six.add_metaclass"""
    def wrapper(cls):
        return metaclass(cls.__name__, cls.__bases__, cls.__dict__.copy())
    return wrapper


class _SwigNonDynamicMeta(type):
    """Meta class to enforce nondynamic attributes (no new attributes) for a class"""
    __setattr__ = _swig_setattr_nondynamic_class_variable(type.__setattr__)


class KaldiRecognizer(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        _vosk.KaldiRecognizer_swiginit(self, _vosk.new_KaldiRecognizer(*args))
    __swig_destroy__ = _vosk.delete_KaldiRecognizer

    def AcceptWaveform(self, data):
        return _vosk.KaldiRecognizer_AcceptWaveform(self, data)

    def Result(self):
        return _vosk.KaldiRecognizer_Result(self)

    def FinalResult(self):
        return _vosk.KaldiRecognizer_FinalResult(self)

    def PartialResult(self):
        return _vosk.KaldiRecognizer_PartialResult(self)

# Register KaldiRecognizer in _vosk:
_vosk.KaldiRecognizer_swigregister(KaldiRecognizer)

class Model(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, model_path):
        _vosk.Model_swiginit(self, _vosk.new_Model(model_path))
    __swig_destroy__ = _vosk.delete_Model

# Register Model in _vosk:
_vosk.Model_swigregister(Model)

class SpkModel(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, spk_path):
        _vosk.SpkModel_swiginit(self, _vosk.new_SpkModel(spk_path))
    __swig_destroy__ = _vosk.delete_SpkModel

# Register SpkModel in _vosk:
_vosk.SpkModel_swigregister(SpkModel)
