import datetime
import matplotlib.pyplot as plt
import numpy as np
from geospacelab import preferences as pref
pref.user_config['visualization']['mpl']['style'] = 'dark'
import geospacelab.visualization.mpl.dashboards as dashboards



def test_swarm_pod():
    dt_fr = datetime.datetime(2016, 1, 30, 0)
    dt_to = datetime.datetime(2016, 2, 4, 23, 59)
    # specify the file full path

    db = dashboards.TSDashboard(dt_fr=dt_fr, dt_to=dt_to, figure_config={'figsize': (12, 8)})

    ds_A = db.dock(datasource_contents=['tud', 'swarm', 'dns_pod'], sat_id='A')
    ds_C = db.dock(datasource_contents=['tud', 'swarm', 'dns_pod'], sat_id='C')

    rho_n_A = db.assign_variable('rho_n', dataset=ds_A)
    rho_n_C = db.assign_variable('rho_n', dataset=ds_C)
    rho_n_A.visual.axis[1].label = r'$\rho$'
    rho_n_A.visual.axis[2].label = 'Swarm-A'
    rho_n_C.visual.axis[2].label = 'Swarm-C'

    glat = db.assign_variable('SC_GEO_LAT', dataset=ds_A)
    glon = db.assign_variable('SC_GEO_LON', dataset=ds_A)

    ds1 = db.dock(datasource_contents=['wdc', 'asysym'])
    sym_h = db.assign_variable('SYM_H', dataset=ds1)

    db.set_layout([[sym_h], [rho_n_A, rho_n_C], [glat], [glon]])
    db.draw()
    # plt.savefig('swarm_example', dpi=300)
    plt.show()


def test_swarm_pod_acc():
    dt_fr = datetime.datetime(2016, 1, 31, 12)
    dt_to = datetime.datetime(2016, 2, 1, 12, 59)
    # specify the file full path

    db = dashboards.TSDashboard(dt_fr=dt_fr, dt_to=dt_to, figure_config={'figsize': (12, 8)})

    ds_pod = db.dock(datasource_contents=['tud', 'swarm', 'dns_pod'], sat_id='C')
    ds_acc = db.dock(datasource_contents=['tud', 'swarm', 'dns_acc'], sat_id='C')

    rho_n_pod = db.assign_variable('rho_n', dataset=ds_pod)
    rho_n_acc = db.assign_variable('rho_n', dataset=ds_acc)
    rho_n_pod.visual.axis[1].label = r'$\rho$'
    rho_n_pod.visual.axis[2].label = 'POD'
    rho_n_acc.visual.axis[2].label = 'ACC'

    glat = db.assign_variable('SC_GEO_LAT', dataset=ds_pod)
    glon = db.assign_variable('SC_GEO_LON', dataset=ds_pod)

    db.set_layout([[rho_n_pod, rho_n_acc], [glat], [glon]])
    db.draw()
    # plt.savefig('swarm_example', dpi=300)
    plt.show()

if __name__ == "__main__":
    test_swarm_pod()
    test_swarm_pod_acc()
