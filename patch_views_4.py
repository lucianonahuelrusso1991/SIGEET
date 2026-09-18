import codecs

with codecs.open('gestion/views.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = -1
for i, line in enumerate(lines):
    if line.startswith("def preinscripcion_publica(request):"):
        if start_idx == -1:
            start_idx = i # first occurrence, keep it
        else:
            # second occurrence, delete from here to return render
            end_idx = i
            for j in range(i, len(lines)):
                if "return render(request, 'gestion/preinscripcion.html', {'form': form})" in lines[j]:
                    end_idx = j
                    break
            lines[i:end_idx+1] = []
            break

with codecs.open('gestion/views.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
