import os
import re


def organize_clippings(input_file='My Clippings.txt', output_dir='organized_clippings'):
    """Parse the Kindle 'My Clippings.txt' file and write organized per-book files.

    Preserves original formatting, filenames, and encodings.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_file, 'r', encoding='utf-8-sig') as f:
        data = f.read()

    entries = [e.strip() for e in data.split('==========') if e.strip()]
    books = {}

    for entry in entries:
        lines = [l for l in entry.split('\n') if l.strip()]
        if not lines or not lines[0]:
            continue
        title_line = lines[0].replace('\ufeff', '')
        title = re.sub(r'\s*\([^)]*\)$', '', title_line).strip()
        meta = lines[1] if len(lines) > 1 else ''
        if 'Highlight' in meta:
            kind = 'highlights'
        elif 'Note' in meta:
            kind = 'notes'
        else:
            kind = 'other'
        # Extract location
        loc_match = re.search(r'Location ([\d\-]+)', meta)
        location = loc_match.group(1) if loc_match else ''
        # Extract content (skip title/meta, join rest)
        content = '\n'.join(lines[2:]).strip()
        # Format: Location: <location>\n<content>
        formatted = f'Location: {location}\n{content}' if location else content
        if title not in books:
            books[title] = {'highlights': [], 'notes': [], 'other': []}
        books[title][kind].append(formatted)

    for title, kinds in books.items():
        safe_title = re.sub(r'[^\w\- ]', '', title).replace(' ', '_')
        # Merge highlights and notes by location
        loc_map = {}
        # Parse highlights
        for h in kinds['highlights']:
            m = re.match(r'Location: ([\d\-]+)\n([\s\S]*)', h)
            if m:
                loc, content = m.group(1), m.group(2).strip()
                loc_map.setdefault(loc, {})['highlight'] = content
            else:
                loc_map.setdefault('', {})['highlight'] = h
        # Parse notes
        for n in kinds['notes']:
            m = re.match(r'Location: ([\d\-]+)\n([\s\S]*)', n)
            if m:
                loc, content = m.group(1), m.group(2).strip()
                loc_map.setdefault(loc, {})['note'] = content
            else:
                loc_map.setdefault('', {})['note'] = n
        # Sort by location (ignore empty loc)
        def loc_key(x):
            try:
                parts = x.split('-')
                return int(parts[0])
            except:
                return float('inf')
        merged = []
        for loc in sorted(loc_map.keys(), key=loc_key):
            entry = ''
            if loc:
                entry += f'Location: {loc}\n'
            if 'highlight' in loc_map[loc]:
                entry += loc_map[loc]['highlight']
            if 'note' in loc_map[loc]:
                if entry and not entry.endswith('\n'):
                    entry += '\n'
                entry += 'Note: \n' + loc_map[loc]['note']
            merged.append(entry.strip())
        out_path = os.path.join(output_dir, f'{safe_title}.txt')
        with open(out_path, 'w', encoding='utf-8') as out:
            out.write('\n\n==========\n\n'.join(merged))


if __name__ == '__main__':
    organize_clippings()
