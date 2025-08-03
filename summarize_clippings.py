import os
import requests

OLLAMA_URL = 'http://localhost:11434/api/generate'
MODEL = 'mistral:7b'
INPUT_DIR = 'organized_clippings'
OUTPUT_DIR = 'summaries'

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


def summarize_text(text, temperature=0.5):
    prompt = (
        "Summarize the following Kindle highlights for use in Apple Notes, meant for quick review and reinforcement, so optimize for *clarity, memorability,* and *ease of skimming*. "
        "Use a mix of short, clear sentences and creative phrasing (even if a bit casual or broken English). "
        "Group related highlights (2–3 at a time) only iff they follow a theme or sequence. "
        "Do NOT explain or interpret quotes. Do not paraphrase them either — quotes must remain exact and separate unless *identical*. "
        "Avoid repetition. If two highlights are the same or nearly identical, keep only one. "
        "Use a mix of paragraphing and bullet points. For structured lists or sequences or collective insights, use sub-bullets. "
        "Add intentional line breaks between distinct ideas to create visual separation. "
        "Do not change quotes or key phrases unless absolutely necessary. Keep important names, models, or phrases intact. "
        "Strictly do not add any new information or external knowledge — only rephrase or format what's already in the text. "
        "Avoid long, dense paragraphs. Do not include personal opinions. "
        "When referring to or incorporating a highlight, insert its original location as a superscript-style tag using the format: (3532–3533)."
        "Write like you're helping someone quickly brush up on key ideas while reading in Apple Notes.\n\n\n"
        +
        text
    )
    data = {
        'model': MODEL,
        'prompt': prompt,
        'stream': False,
        'options': {'temperature': temperature}
    }
    resp = requests.post(OLLAMA_URL, json=data)
    resp.raise_for_status()
    return resp.json()['response'].strip()
    return resp.json()['response'].strip()


for fname in os.listdir(INPUT_DIR):
    print(f"Processing {fname}...")
    if not fname.endswith('.txt'):
        continue
    with open(os.path.join(INPUT_DIR, fname), 'r', encoding='utf-8') as f:
        content = f.read()

    # Chunk the file into groups of 3 highlights (split by '==========')
    blocks = [b.strip() for b in content.split('==========') if b.strip()]
    grouped = ['\n==========\n'.join(blocks[i:i+3]) for i in range(0, len(blocks), 3)]
    summary = ''
    for group in grouped:
        if group.strip():
            summary += summarize_text(group, temperature=0.5) + '\n\n'
    out_path = os.path.join(OUTPUT_DIR, fname.replace('.txt', '_summary.txt'))
    with open(out_path, 'w', encoding='utf-8') as out:
        out.write(summary.strip())
    print(f"Summary for {fname} saved to {out_path}")
