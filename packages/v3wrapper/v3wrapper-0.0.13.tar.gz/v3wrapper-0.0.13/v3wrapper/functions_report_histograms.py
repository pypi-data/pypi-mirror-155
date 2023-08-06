from numpy import isnan
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
plt.rcParams.update({'font.size': 4})
from .functions_aux import chunks

def __histogramDF(df, bins, normed, optimal_min, optimal_max,
              layout,alert_colour='#e74c3c'):
    names = df.columns
    axes = df.hist(bins=bins, density=normed,layout=layout)
    for i, ax in enumerate(axes.reshape(-1)):
        outOfBounds=0
        for rect in ax.patches:
            if ((rect.get_x() + rect.get_width()) > optimal_max) or (rect.get_x() < optimal_min):
                rect.set_color(alert_colour)
                if isnan(rect.get_height()) or isnan(rect.get_width()):
                    pass
                else:
                    outOfBounds += rect.get_height()*rect.get_width()
        ax.set_xticks(bins)
        if i<len(names):
            if isnan(outOfBounds):
                ax.set_title(names[i] + " -- NO INFO AVAILABLE")
            else:
                ax.set_title(names[i]+" -- bad IAQ:"+str(int(round(outOfBounds*100,0)))+"% of the time")

def histogram_charts_pdf(df,
                         names=[],
                         bins = [18, 19, 20, 21, 22, 23, 24, 25, 26, 27],
                         normed=True,
                         optimal_min = 20,
                         optimal_max = 24,
                         filepath = 'multipage_pdf.pdf',
                         chartsPerPage = 4,
                         layout=(2,2),
                         orientation='landscape'):
    '''
    :param df: allSensors type of df
    :param names: list of sensors in the format sensorname_telemetry, for instance [sensor for sensor in sensorNames if v3.parameter_to_return_value[telemetry] in sensor]
    :param bins: [18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
    :param normed: leave as True
    :param optimal_min: 20
    :param optimal_max: 26
    :param filepath: name of file (can include directory) e.g. 'multipage_pdf.pdf'
    :param chartsPerPage: 4
    :param layout: (2,2)
    :param orientation: 'landscape'
    :return: pdf with histogram charts for the specified sensors_telemetry
    '''
    batches = chunks(names,chartsPerPage)
    with PdfPages(filepath) as pdf:
        for batch in batches:
                __histogramDF(df[list(batch)],layout=layout,bins=bins,optimal_min=optimal_min,optimal_max=optimal_max,normed=normed,)
                pdf.savefig(orientation=orientation)
                plt.close()