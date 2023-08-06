import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

"""
This is a basic module for basic statistic works.
created by: AmirrezaSoltani
I've created this module for my math homeworks! but I thought it's better to publish this module for my classmates!
But other people may use it; I'm not sure :)
"""


def R(data : np.ndarray):
    """data should be numpy.ndarray :)"""
    return data.max() - data.min()

def length_of_set(R, number_of_classes : int):
    return R / number_of_classes

def class_range(data : np.ndarray, number_of_classes : int, length_of_set : float,
                plenty = False, relative_plenty = False, batch_centres = False, as_frame = False):
    """data should be numpy.ndarray :)"""
    length = data.min() + length_of_set
    class_end = [length]
    classes = [f'{data.min()} ≤ x < {length}']
    classrange = [data.min(), length]
    for i in range(number_of_classes - 2):
        classes.append(f'{class_end[i]} ≤ x < {class_end[i] + length_of_set}')
        class_end.append(class_end[i] + length_of_set)
    classes.append(f'{class_end[-1]} ≤ x ≤ {class_end[-1] + length_of_set}')
    for j in class_end[1:]:
        classrange.append(j)
    classrange.append(classrange[-1] + length_of_set)
    if plenty == True and batch_centres == False:
        pllst = []
        for o in range(len(classrange)-2):
            pllst.append(np.sum(np.where(np.logical_and(data >= classrange[o], data < classrange[o + 1])==True, 1, 0)))
        pllst.append(np.sum(np.where(np.logical_and(data >= classrange[-2], data <= classrange[-1])==True, 1, 0)))
        if relative_plenty:
            rp = []
            for i in pllst:
                rp.append(i / len(data))
            if as_frame:
                df = pd.DataFrame({'Plenty' : pllst, 'Relative plenty' : rp}, index = classes)
                df.index.names = ['Groups ranges']
                return classes, pllst, rp, df
            elif not as_frame:
                return classes, pllst, rp
        elif not relative_plenty:
            if as_frame:
                df = pd.DataFrame({'Plenty' : pllst}, index = classes)
                df.index.names = ['Groups ranges']
                return classes, pllst, df
        else:
            return pllst, classes
    elif batch_centres == True and plenty == False:
        centroid = []
        for p in range(len(classrange)-1):
            centroid.append((classrange[p] + classrange[p+1]) / 2)
        if as_frame == True:
            df = pd.DataFrame({'Batch centers' : centroid}, index = classes)
            df.index.names = ['Groups ranges']
            return classes, centroid, df
        else:
            return classes, centroid
    elif batch_centres == True and plenty == True:
        centroid = []
        for p in range(len(classrange)-1):
            centroid.append((classrange[p] + classrange[p+1]) / 2)
        pllst = []
        for o in range(len(classrange)-2):
            pllst.append(np.sum(np.where(np.logical_and(data >= classrange[o], data < classrange[o + 1])==True, 1, 0)))
        pllst.append(np.sum(np.where(np.logical_and(data >= classrange[-2], data <= classrange[-1])==True, 1, 0)))
        if relative_plenty:
            rp = []
            for i in pllst:
                rp.append(i / len(data))
            if as_frame:
                df = pd.DataFrame({'Plenty' : pllst, 'Relative plenty' : rp, 'Batch centers' : centroid}, index = classes)
                df.index.names = ['Groups ranges']
                return classes, pllst, rp, centroid, df
            elif not as_frame:
                return classes, pllst, rp, centroid
        elif not relative_plenty:
            if as_frame:
                df = pd.DataFrame({'Plenty' : pllst, 'Batch centers' : centroid}, index = classes)
                df.index.names = ['Groups ranges']
                return classes, pllst, centroid, df
    elif plenty == False and batch_centres == False:
        return classes

def linechart(batch_centers : np.ndarray, plenty : np.ndarray, savefig = False, loc = None):
    if savefig:
        if loc == None:
            raise ValueError("You should enter a location for your figure file!")
        else:
            plt.plot(batch_centers, plenty, marker = 'o')
            plt.title("Line chart")
            plt.yticks(plenty)
            plt.xticks(batch_centers)
            plt.savefig(loc)
            plt.show()
    else:
        plt.plot(batch_centers, plenty, marker = 'o')
        plt.title("Line chart")
        plt.yticks(plenty)
        plt.xticks(batch_centers)
        plt.show()

def piechart(rp : np.ndarray, savefig = False, loc = None):
    degrees = []
    classes = []
    j = 1
    if savefig:
        if loc == None:
            raise ValueError("You should enter a location for your figure file!")
        else:
            for i in rp:
                degrees.append(i * 360)
                classes.append(f"{j} = {round(degrees[j-1], 2)}$^\circ$")
                j += 1
            plt.pie(degrees, autopct='%.2f%%')
            plt.title("Pie chart")
            plt.legend(labels = classes, title = 'Classes with degrees:', bbox_to_anchor = (0.85, 0.75))
            plt.savefig(loc)
            plt.show()
    else:
        for i in rp:
            degrees.append(i * 360)
            classes.append(f"{j} = {round(degrees[j-1], 2)}$^\circ$")
            j += 1
            plt.pie(degrees, autopct='%.2f%%')
            plt.title("Pie chart")
            plt.legend(labels = classes, title = 'Classes with degrees:', bbox_to_anchor = (0.85, 0.75))
            plt.show()
def barchart(class_range : list or np.ndarray, plenty : list or np.ndarray, savefig = False, loc = None):
    if savefig:
        if loc == None:
            raise ValueError("You should enter a location for your figure file!")
        else:
            plt.bar(class_range, plenty)
            plt.yticks(plenty)
            plt.xticks(rotation = 0, fontsize = 6.8)
            plt.title("Bar chart")
            plt.savefig(loc)
            plt.show()
    else:
        plt.bar(class_range, plenty)
        plt.yticks(plenty)
        plt.xticks(rotation = 0, fontsize = 6.8)
        plt.title("Bar chart")
        plt.show()

__version__ = "1.0.14"