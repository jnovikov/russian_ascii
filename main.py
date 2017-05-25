from jinja2 import Template
from sanic import Sanic
from sanic.response import html

f = open('templates/main.html')
html_temp = f.read()
f.close()

ascii_dict = {str(n): chr(n) for n in range(128)}
ascii_ru = {}
for i in range(0, 66):
    ascii_ru[str(192 + i)] = chr(1040 + i)
ascii_dict.update(ascii_ru)

inverse_dict = {v: k for k, v in ascii_dict.items()}


app = Sanic()
app.static('/static', './static')


def convert(data, method):
    if data == "":
        return ""
    if method == "1":
        output_string = ""
        data = data.split(' ')
        data = list(map(lambda x: x[:-1] if x[-1] == ',' else x, data))
        for key in data:
            if key in ascii_dict.keys():
                output_string += ascii_dict[key]
            else:
                output_string += '×'

        return output_string
    elif method == "2":
        out_list = []
        for letter in data:
            if letter in inverse_dict.keys():
                out_list.append(str(inverse_dict[letter]))
            else:
                out_list.append(str('xx'))
        return ' '.join(out_list)
    else:
        return ""



@app.route("/")
async def test(request):
    # print(request.form)
    #print(request.args)
    method = request.args.get('method', '1')
    data = request.args.get('input', '')
    output = convert(data, method)
    context = {'input':data,'output':output}
    template = Template(html_temp)
    return html(template.render(**context))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9009)
