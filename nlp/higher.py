import json

if __name__ == "__main__":
    with open('data.new.list', 'w') as w_f:
        with open('data.list', 'r') as f:
            lines = f.readlines()
            for line in lines:
                data = json.loads(line)
                data['txt'] = data['txt'].lower()
                w_f.write(json.dumps(data) + '\n')
    with open('text.new', 'w') as w_f:
        with open('text', 'r') as f:
            lines = f.readlines()
            for line in lines:
                key, text = line.split(" ", 1)
                text = text.lower()
                w_f.write(key + ' ' + text)
