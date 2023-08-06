
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
plt.rcParams.update({'font.size': 4})
from .functions_aux import chunks

def line_charts_pdf(df_list,
                    filepath = 'multipage_pdf.pdf',
                    split_plots = True,
                    chartsPerPage = 4,
                    layout=(2,2),
                    orientation='landscape'):
    '''

    :param df_list:
    :param filepath:
    :param split_plots: if False - a df with multiple columns will plot all curves in the same chart. If True - a df with multiple curves will plot one chart per curve.
    :param chartsPerPage:
    :param layout:
    :param orientation:
    :return:
    '''

    batches = chunks(df_list,chartsPerPage)
    with PdfPages(filepath) as pdf:
        for batch in batches:
                for df in batch:
                    axes = df.plot(subplots = split_plots,layout=layout)
                    pdf.savefig(orientation=orientation)
                    plt.close()