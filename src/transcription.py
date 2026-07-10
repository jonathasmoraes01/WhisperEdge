import io
import os
import numpy as np
import soundfile as sf
from faster_whisper import WhisperModel
from openai import OpenAI

from utils import ConfigManager

def _add_nvidia_dll_dirs():
    """Registra as DLLs CUDA (cuBLAS/cuDNN) instaladas via pip
    (pacotes nvidia-cublas-cu12 / nvidia-cudnn-cu12) no caminho de busca,
    para a GPU funcionar sem instalar o CUDA Toolkit."""
    try:
        import glob
        import nvidia  # namespace package: usar __path__ (nao tem __file__)
        for base in list(getattr(nvidia, '__path__', [])):
            for bin_dir in glob.glob(os.path.join(base, '*', 'bin')):
                try:
                    os.add_dll_directory(bin_dir)
                except Exception:
                    pass
                os.environ['PATH'] = bin_dir + os.pathsep + os.environ.get('PATH', '')
    except Exception:
        pass


def _cuda_available():
    """True se o ctranslate2 enxerga uma GPU NVIDIA utilizavel."""
    try:
        import ctranslate2
        return ctranslate2.get_cuda_device_count() > 0
    except Exception:
        return False


def create_local_model():
    """
    Create a local model using the faster-whisper library.

    device 'auto': tenta GPU NVIDIA (CUDA) e cai para CPU com int8 se a GPU
    nao estiver disponivel ou falhar ao carregar (ex.: cuDNN ausente).
    """
    ConfigManager.console_print('Creating local model...')
    local_model_options = ConfigManager.get_config_section('model_options')['local']
    compute_type = local_model_options['compute_type'] or 'default'
    model_path = local_model_options.get('model_path')
    device = local_model_options['device'] or 'auto'
    model_name = model_path or local_model_options['model']

    if device == 'auto':
        device = 'cuda' if _cuda_available() else 'cpu'
    if device == 'cuda':
        _add_nvidia_dll_dirs()

    # Ajusta o compute_type ao dispositivo quando o usuario deixou 'default'.
    if compute_type == 'default':
        compute_type = 'float16' if device == 'cuda' else 'int8'
    if device == 'cpu' and compute_type == 'float16':
        compute_type = 'int8'  # float16 nao roda em CPU

    try:
        ConfigManager.console_print(f'Loading model on {device} ({compute_type})...')
        model = WhisperModel(model_name, device=device, compute_type=compute_type)
    except Exception as e:
        ConfigManager.console_print(f'Error initializing WhisperModel on {device}: {e}')
        ConfigManager.console_print('Falling back to CPU (int8).')
        model = WhisperModel(model_name, device='cpu', compute_type='int8')

    ConfigManager.console_print('Local model created.')
    return model

def transcribe_local(audio_data, local_model=None):
    """
    Transcribe an audio file using a local model.
    """
    if not local_model:
        local_model = create_local_model()
    model_options = ConfigManager.get_config_section('model_options')

    # Convert int16 to float32
    audio_data_float = audio_data.astype(np.float32) / 32768.0

    response = local_model.transcribe(audio=audio_data_float,
                                      language=model_options['common']['language'],
                                      initial_prompt=model_options['common']['initial_prompt'],
                                      condition_on_previous_text=model_options['local']['condition_on_previous_text'],
                                      temperature=model_options['common']['temperature'],
                                      vad_filter=model_options['local']['vad_filter'],)
    return ''.join([segment.text for segment in list(response[0])])

def transcribe_api(audio_data):
    """
    Transcribe an audio file using the OpenAI API.
    """
    model_options = ConfigManager.get_config_section('model_options')
    client = OpenAI(
        api_key=os.getenv('OPENAI_API_KEY') or None,
        base_url=model_options['api']['base_url'] or 'https://api.openai.com/v1'
    )

    # Convert numpy array to WAV file
    byte_io = io.BytesIO()
    sample_rate = ConfigManager.get_config_section('recording_options').get('sample_rate') or 16000
    sf.write(byte_io, audio_data, sample_rate, format='wav')
    byte_io.seek(0)

    response = client.audio.transcriptions.create(
        model=model_options['api']['model'],
        file=('audio.wav', byte_io, 'audio/wav'),
        language=model_options['common']['language'],
        prompt=model_options['common']['initial_prompt'],
        temperature=model_options['common']['temperature'],
    )
    return response.text

def post_process_transcription(transcription):
    """
    Apply post-processing to the transcription.
    """
    transcription = transcription.strip()
    post_processing = ConfigManager.get_config_section('post_processing')
    if post_processing['remove_trailing_period'] and transcription.endswith('.'):
        transcription = transcription[:-1]
    if post_processing['add_trailing_space']:
        transcription += ' '
    if post_processing['remove_capitalization']:
        transcription = transcription.lower()

    return transcription

def transcribe(audio_data, local_model=None):
    """
    Transcribe audio date using the OpenAI API or a local model, depending on config.
    """
    if audio_data is None:
        return ''

    if ConfigManager.get_config_value('model_options', 'use_api'):
        transcription = transcribe_api(audio_data)
    else:
        transcription = transcribe_local(audio_data, local_model)

    # WhisperEdge: aprimoramento (LLM clean-up opcional + dicionario + snippets)
    # aplicado ao texto nucleo, antes da formatacao final (espaco/pontuacao).
    from text_processing import enhance_text
    transcription = enhance_text(transcription.strip())

    return post_process_transcription(transcription)

