import csv
from datetime import datetime
from math import ceil
# from math import floor


def get_data(corona_csv):
    with open(corona_csv, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')

        date_time = []
        cases = []
        deaths = []
        recoveries = []

        for index, row in enumerate(csv_reader):
            cases.append((index, row[0].replace(",", "")))
            deaths.append((index, row[1].replace(",", "")))
            recoveries.append((index, row[2].replace(",", "")))
            date_time.append((index, ' '.join([row[3], row[4]])))

    return {
        'cases': cases,
        'deaths': deaths,
        'recoveries': recoveries,
        'date_time': date_time
    }


def round_dec(number, func):
    dec = 10 ** (len(str(number)) - 1)
    return func(number / dec) * dec


def plot_svg(title, y_label, x_label, data):
    pos = {
        'y': {
            'top': 11,  # margem superior 11
            'left': 5,  # margem esquerda 5
            'right': 0,  # margem direita 0
            'bottom': 95  # margem inferior 5
        },
        'x': {
            'top': 90,  # margem superior 90
            'left': 0,  # margem esquerda 0
            'right': 100,  # maregem direita 0
            'bottom': 0  # margem inferior 0
        },
    }
    _svg = '<svg height="100%" width="100%" viewBox="0 0 100 100" style="background-color:whitesmoke">{}</svg>'

    _title = f'<text text-anchor="middle" x="50" y="4" fill="black" font-size="4">{title}</text>'

    _y_axis = f'<text text-anchor="middle" x="5" y="10" fill="blue" font-size="2">{y_label}</text>' \
              '<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="black" stroke-width=".2" />' \
        .format(**pos['y'])

    _x_axis = f'<text text-anchor="left" x="50" y="100" fill="blue" font-size="2">{x_label}</text>' \
              '<line x1="{left}" y1="{top}" x2="{right}" y2="{top}" stroke="black" stroke-width=".2" />' \
        .format(**pos['x'])

    max_case = int(max([v[1] for v in data['cases']]))
    min_case = int(min([v[1] for v in data['cases']]))

    H_MAX = round_dec(max_case, ceil)
    # H_MIN = round_dec(min_case, floor)
    H_MIN = 0
    D_MAX = '24/04/2020 16:00:03'
    D_MIN = '16/04/2020 16:00:03'
    # print(max_case, H_MAX)

    tmin = datetime.strptime(D_MIN, '%d/%m/%Y %H:%M:%S').timestamp()
    tmax = datetime.strptime(D_MAX, '%d/%m/%Y %H:%M:%S').timestamp()

    polyline = []

    for label, infos in data.items():
        if label == 'date_time':
            continue
        string_result = []
        init_value = pos['x']['top'] - ((int(infos[0][1]) - H_MIN) / (H_MAX - H_MIN) * (100 - pos['y']['top']))
        label_tag = f'<text text-anchor="end" x="4" y="{init_value}" fill="blue" font-size="2">{label}</text>'
        #   # print(f'{label}: {color}')
        for i, value in infos:
            y = pos['x']['top'] - ((int(value) - H_MIN) / (H_MAX - H_MIN) * (
                        100 - pos['y']['top']))  # 90 -> 10 de margem no rodapé
            timestamp = datetime \
                .strptime(data['date_time'][i][1], '%d/%m/%Y %H:%M:%S') \
                .timestamp()
            x = (5 + (int(timestamp) - tmin) / (tmax - tmin) * 100)  # 5 -> margem esquerda
            result = f'{x},{y}'
            string_result.append(result)

        points = ' '.join(string_result)
        color = 'red'
        polyline.append(f'{label_tag}<polyline points="{points}" style="fill:none;stroke:{color};stroke-width:1" />')

    return _svg.format('\n'.join([_title, _y_axis, _x_axis, *polyline]))


data = get_data('world.csv')
svg = plot_svg('Brasil', '', 'Datas', data)

print(svg)
