from config import SPEECH_KEY, SERVICE_REGION
import azure.cognitiveservices.speech as speechsdk

# Create a Speech config
speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SERVICE_REGION)
speech_config.speech_synthesis_voice_name = "en-US-AriaNeural"
speech_config.speech_synthesis_language = "en-US"

# Set output format to MP3
speech_config.set_speech_synthesis_output_format(
    speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
)

# Create a speech synthesizer
# No audio output config, since we are capturing audio data directly
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

# Result Reasons
audio_completed = speechsdk.ResultReason.SynthesizingAudioCompleted
audio_canceled = speechsdk.ResultReason.Canceled
audio_canceled_reason = speechsdk.CancellationReason.Error