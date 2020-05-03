import csv
from datetime import datetime
from math import ceil


def get_data():
    with open('../projeto_04/data_csv/spain.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=' ')

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
    """
    Arredonda o número máximo para o a dezena de milhar
    completa mais próxima.
    number: número a ser arredondado
    func: metodo de arredondamento
    """

    dec = 10 ** (len(str(number)) - 1)

    return func(number / dec) * dec


def plot_svg(title, y_label, x_label):
    pos = {
        'y': {
            'top': 10,  # margem superior 11method
            'left': 5,  # margem esquerda 5
            'right': 1,  # margem direita 0
            'bottom': 95  # margem inferior 5
        },
        'x': {
            'top': 95,  # margem superior 90
            'left': 1,  # margem esquerda 0
            'right': 95,  # maregem direita 0
            'bottom': 1  # margem inferior 0
        },
    }

    _svg = '<svg height="100%" width="100%" viewBox="0 0 100 100" style="background-color:whitesmoke">{}</svg>'

    _title = f'<text text-anchor="middle" x="50%" y="7%" fill="black" font-size="7">{title}</text>'

    _y_axis = f'<text text-anchor="middle" x="6%" y="8%" font-size="3">{y_label}</text>' \
              '<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="black" stroke-width="0.5%" />' \
              '<polygon points="4,12 5,10 6,12" fill="black" stroke="black" />' \
        .format(**pos['y'])

    _x_axis = f'<text text-anchor="middle" x="50%" y="98%" font-size="3">{x_label}</text>' \
              '<line x1="{left}" y1="{top}" x2="{right}" y2="{top}" stroke="black" stroke-width="0.5%" />' \
              '<polygon points="92,96 94,95 92,94" fill="black" stroke="black" />' \
        .format(**pos['x'])

    data = get_data()

    max_case = int(max([v[1] for v in data['cases']]))

    H_MAX = round_dec(max_case, ceil)
    H_MIN = 0
    D_MAX = '24/04/2020 16:00:03'
    D_MIN = '16/04/2020 16:00:03'

    tmin = datetime.strptime(D_MIN, '%d/%m/%Y %H:%M:%S').timestamp()
    tmax = datetime.strptime(D_MAX, '%d/%m/%Y %H:%M:%S').timestamp()

    lines = []

    for label, infos in data.items():
        if label == 'date_time':
            continue

        values = ""
        for i in infos:
            values = values + "{},{}".format(per_x(tmin, tmax, data['date_time'][i[0]][1]),
                                             per_y(pos, i[1], H_MAX)) + " "
        color = 'red'
        lines.append(f'<polyline points="{values[:-1]}" style="fill:none;stroke:{color};stroke-width:1" />')

    return _svg.format("\n".join(lines) + _title + _x_axis + _y_axis)


def per_y(pos, num, H_MAX):
    num = int(num)
    y = pos['x']['top'] - (num / H_MAX * (100 - pos['y']['top']))
    return y


def per_x(tmin, tmax, date):
    timestamp = datetime.strptime(date, '%d/%m/%Y %H:%M:%S').timestamp()
    x = (5 + (int(timestamp) - tmin) / (tmax - tmin) * 100)
    return x


if __name__ == '__main__':
    chart_brazil = plot_svg('Spain', 'Numbers', 'Days')
    print(chart_brazil)

    with open("spain.svg", "w") as f:
        f.write(chart_brazil)
