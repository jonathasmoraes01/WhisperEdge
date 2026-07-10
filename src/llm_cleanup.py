"""
Limpeza/edicao de texto por LLM (opcional) do WhisperEdge.

Provedores suportados:
- 'openai'  : qualquer endpoint OpenAI-compat (OpenAI, Groq, etc.)
- 'ollama'  : LLM local via endpoint OpenAI-compat (ex.: http://localhost:11434/v1)
- 'anthropic': API de mensagens da Anthropic

Nada e obrigatorio: se estiver desligado ou falhar (rede/timeout/sem chave),
o texto original e devolvido intacto. Nenhuma chave e hardcoded — usa a config
ou as variaveis de ambiente OPENAI_API_KEY / ANTHROPIC_API_KEY.
"""
import os

from utils import ConfigManager


def _cfg(*keys):
    return ConfigManager.get_config_value('llm_post_processing', *keys)


def _resolve_api_key(provider):
    key = _cfg('api_key')
    if key:
        return key
    if provider == 'anthropic':
        return os.getenv('ANTHROPIC_API_KEY')
    return os.getenv('OPENAI_API_KEY')


def _chat_openai(system_prompt, user_content, model, base_url, api_key, timeout):
    from openai import OpenAI
    client = OpenAI(
        api_key=api_key or 'not-needed',  # Ollama/local aceitam qualquer valor
        base_url=base_url or 'https://api.openai.com/v1',
        timeout=timeout,
    )
    resp = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_content},
        ],
    )
    return (resp.choices[0].message.content or '').strip()


def _chat_anthropic(system_prompt, user_content, model, base_url, api_key, timeout):
    import httpx
    base = (base_url or 'https://api.anthropic.com').rstrip('/')
    # Se o usuario deixou a URL padrao da OpenAI, usa a da Anthropic.
    if 'openai.com' in base or base.endswith('/v1') is False:
        if 'anthropic' not in base:
            base = 'https://api.anthropic.com'
    url = base.rstrip('/')
    if not url.endswith('/messages'):
        url = url + '/v1/messages' if not url.endswith('/v1') else url + '/messages'
    headers = {
        'x-api-key': api_key or '',
        'anthropic-version': '2023-06-01',
        'content-type': 'application/json',
    }
    payload = {
        'model': model,
        'max_tokens': 2048,
        'temperature': 0,
        'system': system_prompt,
        'messages': [{'role': 'user', 'content': user_content}],
    }
    with httpx.Client(timeout=timeout) as client:
        r = client.post(url, headers=headers, json=payload)
        r.raise_for_status()
        data = r.json()
        parts = data.get('content') or []
        return ''.join(p.get('text', '') for p in parts if p.get('type') == 'text').strip()


def chat(system_prompt, user_content, timeout=None):
    """Chamada generica ao LLM configurado. Levanta excecao em caso de erro."""
    provider = _cfg('provider') or 'openai'
    model = _cfg('model') or 'gpt-4o-mini'
    base_url = _cfg('base_url')
    timeout = timeout or _cfg('timeout') or 20
    api_key = _resolve_api_key(provider)

    if provider == 'anthropic':
        return _chat_anthropic(system_prompt, user_content, model, base_url, api_key, timeout)
    return _chat_openai(system_prompt, user_content, model, base_url, api_key, timeout)


def clean_up(text):
    """Limpa a transcricao via LLM. Em qualquer falha, devolve o texto original."""
    if not text or not text.strip():
        return text
    system_prompt = _cfg('system_prompt') or 'Corrija pontuacao e remova hesitacoes. Devolva apenas o texto limpo.'

    # WhisperEdge — perfis por app: adapta o estilo conforme a janela ativa
    # (ex.: Discord = casual; IDE = prompt tecnico). Ver data/app_profiles.json.
    try:
        from history import get_active_window_title
        from text_processing import style_for_window
        title = get_active_window_title()
        style = style_for_window(title)
        if style:
            system_prompt += (f"\n\nContexto: o usuario esta ditando na janela "
                              f"'{title[:70]}'. Ajuste o estilo do texto: {style}")
    except Exception:
        pass

    try:
        result = chat(system_prompt, text)
        return result or text
    except Exception as e:
        ConfigManager.console_print(f'[llm_cleanup] falha, usando texto original: {e}')
        return text
