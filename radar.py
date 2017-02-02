# adapted from matplotlib radar chart api example

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection


# function to convert polar coordinates into cartesian coordinates
def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return x, y


# function to find area of a polygon given its vertices
def area_of_polygon(x, y):
    area = 0.0
    for i in xrange(-1, len(x)-1):
        area += x[i] * (y[i+1] - y[i-1])
    return abs(area) / 2.0


def _radar_factory(num_vars):
    theta = 2 * np.pi * np.linspace(0, 1 - 1. / num_vars, num_vars)
    theta += np.pi / 2

    def unit_poly_verts(theta):
        x0, y0, r = [0.5] * 3
        verts = [(r * np.cos(t) + x0, r * np.sin(t) + y0) for t in theta]
        return verts

    class RadarAxes(PolarAxes):
        name = 'radar'
        RESOLUTION = 2

        def fill(self, *args, **kwargs):
            closed = kwargs.pop('closed', True)
            return super(RadarAxes, self).fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            lines = super(RadarAxes, self).plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

            area = self.area(line)
            return area

        def area(self, line):
            # coordinates are given in pairs of radian value (beginning at 90deg)
            # and outward distance (between 0-100...this is directly from the fed in data)
            angle, radius = line.get_data()
            angle = angle[:-1]
            radius = radius[:-1]
            # print angle, radius
            # print "converting..."
            xx, yy = pol2cart(radius, angle)
            # print xx, yy
            # print "area =", area_of_polygon(xx, yy)
            # print "break..."
            return area_of_polygon(xx, yy)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(theta * 180 / np.pi, labels)

        def _gen_axes_patch(self):
            verts = unit_poly_verts(theta)
            return plt.Polygon(verts, closed=True, edgecolor='k')

        def _gen_axes_spines(self):
            spine_type = 'circle'
            verts = unit_poly_verts(theta)
            verts.append(verts[0])
            path = Path(verts)
            spine = Spine(self, spine_type, path)
            spine.set_transform(self.transAxes)
            return {'polar': spine}

    register_projection(RadarAxes)
    return theta


def radar_graph(header, labels=[], leg=[], case1=[], case2=[], case3=[], case4=[], case5=[]):
    N = len(labels)
    theta = _radar_factory(N)
    fig = plt.figure(figsize=(9, 9))
    fig.subplots_adjust(left=0, wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)
    ax = fig.add_subplot(1, 1, 1, projection='radar')
    # plt.rgrids((1, 2, 3, 4, 5, 6, 7, 8, 9))

    plt1 = ax.plot(theta, case1, color='y')
    plt2 = ax.plot(theta, case2, color='r')
    plt3 = ax.plot(theta, case3, color='g')
    plt4 = ax.plot(theta, case4, color='blue')
    plt5 = ax.plot(theta, case5, color='brown')

    areas = [plt1, plt2, plt3, plt4, plt5]

    ax.fill(theta, case1, color='y', alpha=0.25)
    ax.fill(theta, case2, color='r', alpha=0.25)
    ax.fill(theta, case3, color='g', alpha=0.25)
    ax.fill(theta, case4, color='blue', alpha=0.25)
    ax.fill(theta, case5, color='brown', alpha=0.25)

    ax.set_varlabels(labels)
    ax.set_title(header, weight='bold', size='large', position=(0.5, 1.1),
                 horizontalalignment='center', verticalalignment='center')

    legend = plt.legend(leg, loc=(0.9, .95), labelspacing=0.1)
    plt.setp(legend.get_texts(), fontsize='small')

    plt.savefig(header + ".png", dpi=100)
    plt.show()

    hepta_area = 30705.5
    balance = int(100 * (sum(areas))/(5 * hepta_area))
    print "balance :", balance

    return balance


def stacked_radar(header, labels=[], leg=[], case1=[], case2=[], case3=[], case4=[], case5=[]):
    N = len(labels)
    theta = _radar_factory(N)
    fig = plt.figure(figsize=(9, 9))
    fig.subplots_adjust(left=0, wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)
    ax = fig.add_subplot(1, 1, 1, projection='radar')

    plt1 = ax.plot(theta, [sum(x) for x in zip(case1, case2, case3, case4, case5)], color='#ec644b')
    plt2 = ax.plot(theta, [sum(x) for x in zip(case2, case3, case4, case5)], color='#9b59b6')
    plt3 = ax.plot(theta, [sum(x) for x in zip(case3, case4, case5)], color='#19b5fe')
    plt4 = ax.plot(theta, [sum(x) for x in zip(case4, case5)], color='#2ecc71')
    plt5 = ax.plot(theta, case5, color='#f9bf3b')

    skeleton = ax.plot(theta, [500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500],
                       color='k')

    areas = [plt1]

    ax.fill(theta, [sum(x) for x in zip(case1, case2, case3, case4, case5)], color='#ec644b', alpha=1)
    ax.fill(theta, [sum(x) for x in zip(case2, case3, case4, case5)], color='#9b59b6', alpha=1)
    ax.fill(theta, [sum(x) for x in zip(case3, case4, case5)], color='#19b5fe', alpha=1)
    ax.fill(theta, [sum(x) for x in zip(case4, case5)], color='#2ecc71', alpha=1)
    ax.fill(theta, case5, color='#f9bf3b', alpha=1)

    ax.set_varlabels(labels)
    ax.set_title(header, weight='bold', size='large', position=(0.5, 1.1),
                 horizontalalignment='center', verticalalignment='center')

    legend = plt.legend(leg, loc=(0.9, .95), labelspacing=0.1)
    plt.setp(legend.get_texts(), fontsize='small')

    plt.savefig(header + ".png", dpi=100)
    plt.show()

    hepta_area = 767639
    balance = round(100 * (sum(areas))/hepta_area)
    print "balance :", balance

    return balance
