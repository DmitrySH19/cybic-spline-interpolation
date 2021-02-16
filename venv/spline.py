import numpy as np
from math import sqrt
import PySimpleGUI as sg
import random
import matplotlib.pyplot as plt
from scipy import interpolate
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
from matplotlib.ticker import NullFormatter

if __name__ == '__main__':

    matplotlib.use("TkAgg")

    cell_size = (4, 2)
    cell_x = sg.Text('x1')
    test = [[sg.Text('x1'), sg.InputText(size=cell_size)]]
    point_count = 0
    x = []
    x_points = ()
    y_points = ()
    is_draw = True
    fig = matplotlib.figure.Figure( figsize=(8, 6), dpi=100, facecolor='w', edgecolor='k')

    for i in range(5):
        num = 'x'+ str(i+1)
        x.append(sg.Text(str))
        x.append(sg.InputText(size=cell_size))

    input_layout = [
        [sg.Text('Input number of points (min: 4, max: 20)'), sg.InputText(size=cell_size, key='text'),
         sg.Button(button_text='ok', key='-IN-'), sg.Button('Exit')],
    ]
    window_input  =  sg.Window('Enter points', input_layout, font='Helvetica 14')
    window = window_input
    while True:  # The Event Loop
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'enter_point':
            input_layout = [
                [sg.Text('Input number of points (min: 4, max: 16)'), sg.InputText(size=cell_size, key='text'),
                 sg.Button(button_text='ok', key='-IN-'), sg.Button('Exit')],
            ]
            window.close()
            is_draw = True
            window = sg.Window('Enter points', input_layout, font='Helvetica 14')
        if event == '-IN-':
            if int(values['text']) >= 4 and int(values['text']) <= 20:
                point_count = int(values['text'])
                window.close()
                layout = []
                layout.append([])
                for i in range(point_count):
                    num = 'x' + str(i + 1)
                    layout[0].append(sg.Text(num))
                    layout[0].append(sg.InputText(size=cell_size,key=num))
                layout.append([])
                for i in range(point_count):
                    num = 'y' + str(i + 1)
                    layout[1].append(sg.Text(num))
                    layout[1].append(sg.InputText(size=cell_size,key=num))

                layout.append([sg.Button(button_text='Draw spline'),sg.Button(button_text='autocomplite'),
                               sg.Button(button_text='other point', key='enter_point'), sg.Button('Exit')])
                layout.append([sg.Canvas(key='-CANVAS-')], )
                window = sg.Window('Draw spline', layout, font='Helvetica 14', finalize=True)
            else:
                sg.Popup('number not in renge')
        if event == 'autocomplite':
            x_points = (random.randint(-1000, 1000) for i in range(point_count))
            x_points = tuple(sorted(x_points))
            y_points = tuple(random.randint(-1000, 1000) for i in range(point_count))
            for i in range(point_count):
                num = 'x' + str(i + 1)
                window.FindElement(num).Update(value=x_points[i])
            for i in range(point_count):
                num = 'y' + str(i + 1)
                window.FindElement(num).Update(value=y_points[i])
        if event == 'Draw spline':

            is_empty = False
            temp = []
            for i in range(point_count):
                num = 'x' + str(i + 1)
                if values[num] == '':
                    is_empty = True
                else:
                     temp.append(int(values[num]))
            x_points = tuple(temp)
            temp.clear()
            for i in range(point_count):
                num = 'y' + str(i + 1)
                if values[num] == '':
                    is_empty = True
                else:
                     temp.append(int(values[num]))
            y_points = tuple(temp)
            points = []
            if not is_empty:
                for i in range(len(x_points)):
                    points.append([x_points[i],y_points[i]])
                print(points)
                points.sort(key=lambda x: x[0])

                print(points)
                temp = []
                for i in range(len(x_points)):
                    temp.append(points[i][0])
                x_points = tuple(temp)
                temp.clear()
                for i in range(len(x_points)):
                    temp.append(points[i][1])
                y_points = tuple(temp)

                for i in range(point_count):
                    num = 'x' + str(i + 1)
                    window.FindElement(num).Update(value=x_points[i])
                for i in range(point_count):
                    num = 'y' + str(i + 1)
                    window.FindElement(num).Update(value=y_points[i])

                temp.clear()
                x = x_points
                y = y_points
                plt.clf()
                fig.clf()
                t = np.arange(0, 3, .01)
                print(x, y)
                ax = fig.add_subplot(111)
                fig.set(facecolor='gray')
                ax.set(facecolor='yellow',
                       title='Cubic spline interpolate',
                       xlabel='X coordinates',
                       ylabel='Y coordinates')
                ax.minorticks_on()

                #  Определяем внешний вид линий основной сетки:
                ax.grid(which='major',
                        color='k',
                        linewidth=1)

                #  Определяем внешний вид линий вспомогательной
                #  сетки:
                ax.grid(which='minor',
                        color='k',
                        linestyle=':')

                data = np.array((x, y), dtype='float64')
                tck, u = interpolate.splprep(data, s=0)
                unew = np.arange(0, 1.01, 0.01)
                out = interpolate.splev(unew, tck)
                ax.plot(out[0], out[1], color='red', label='Line 1', linewidth=2)
                ax.plot(data[0, :], data[1, :], 'ob', color='black', linewidth=0.1)
                ax.legend(['cubic spline', 'points'])

                fig.canvas.draw()
                fig.canvas.flush_events()

                if is_draw:
                    figure_canvas_agg = FigureCanvasTkAgg(fig, window["-CANVAS-"].TKCanvas)
                    figure_canvas_agg.draw_idle()
                    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
                    is_draw = False
            else:
                sg.Popup('which one of the cells is empty')