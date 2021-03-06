# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mcosta/Dropbox/SPICE/SPICE_CROSS_MISSION/spiops/spiops/classes/body.py
# Compiled at: 2019-02-26 15:23:34
# Size of source mod 2**32: 16843 bytes
import spiceypy, numpy as np
from spiops.utils import utils
from bokeh.layouts import row
from bokeh.plotting import figure, show, output_notebook
from bokeh.models.glyphs import Ellipse
from bokeh.models import ColumnDataSource, Plot, LinearAxis, Grid

class Body(object):

    def __init__(self, body, time=object(), target=None):
        if isinstance(body, str):
            name = body
            id = spiceypy.bodn2c(body)
        else:
            id = body
            name = spiceypy.bodc2n(body)
        if target:
            self.target = target
        self.name = name
        self.id = id
        self.time = time
        self.previous_tw = []
        self.geometry_flag = False

    def __getattribute__(self, item):
        if item in ('altitude', 'distance', 'zaxis_target_anglemyaxis_target_angle',
                    'groundtrack', 'trajectory'):
            self._Body__Geometry()
            return object.__getattribute__(self, item)
        else:
            if item in ('sa_ang_p', 'sa_ang_n', 'sa_ang', 'saa_sa', 'saa_sc', 'hga_earth',
                        'hga_angles'):
                self._Body__Structures()
                return object.__getattribute__(self, item)
            return object.__getattribute__(self, item)

    def __getattr__(self, item):
        if item in ('state_in_window', ):
            self._Body__StateInWindow()
            return object.__getattribute__(self, item)

    def State(self, target=False, reference_frame=False, current=False):
        if self.target:
            if not target:
                if not reference_frame:
                    target = self.target.name
                    reference_frame = self.target.frame
        else:
            if not self.target:
                if target is False:
                    target = 'J2000'
                if reference_frame is False:
                    reference_frame = 'J2000'
            self.trajectory_reference_frame = reference_frame
            current = current or self.time.current
        state, lt = spiceypy.spkezr(target, current, reference_frame, self.time.abcorr, self.name)
        return state

    def Orientation(self, frame='', target_frame='', current=False, format='msop quaternions'):
        if self.target:
            if not target_frame:
                target_frame = self.target.frame
            else:
                if not self.target:
                    if not target_frame:
                        target_frame = 'J2000'
                    if not frame:
                        frame = self.frame
                    current = current or self.time.current
                else:
                    current = current
            rot_mat = spiceypy.pxform(target_frame, frame, current)
            if format == 'spice quaternions':
                orientation = spiceypy.m2q(rot_mat)
        else:
            if format == 'msop quaternions':
                quaternions = spiceypy.m2q(rot_mat)
                orientation = [-quaternions[1],
                 -quaternions[2],
                 -quaternions[3],
                 quaternions[0]]
            else:
                if format == 'euler angles':
                    orientation = spiceypy.m2eul(rot_mat, 3, 2, 1)
                elif format == 'rotation matrix':
                    orientation = rot_mat
        return orientation

    def __StateInWindow(self, target=False, reference_frame=False, start=False, finish=False):
        state_in_window = []
        for et in self.time.window:
            state_in_window.append(self.State(target, reference_frame, et))

        self.state_in_window = state_in_window

    def __Structures(self):
        if self.structures_flag is True:
            if self.time.window.all() == self.previous_tw.all():
                return
        else:
            time = self.time
            import spiops
            if self.name == 'TGO':
                plus_array = 'TGO_SA+Z'
                minus_array = 'TGO_SA-Z'
            else:
                if self.name == 'MPO':
                    plus_array = 'MPO_SA'
                    minus_array = ''
                else:
                    if self.name == 'MTM':
                        plus_array = 'MTM_SA+X'
                        minus_array = 'MTM_SA-X'
                    else:
                        plus_array = '{}_SA+Y'.format(self.name.upper())
                        minus_array = '{}_SA-Y'.format(self.name.upper())
            sa_ang_p_list = []
            sa_ang_n_list = []
            saa_sa_p_list = []
            saa_sa_n_list = []
            saa_sc_x_list = []
            saa_sc_y_list = []
            saa_sc_z_list = []
            hga_earth = []
            hga_angles_el = []
            hga_angles_az = []
            for et in time.window:
                sa_ang_p = spiops.solar_array_angle(plus_array, et)
                if minus_array:
                    sa_ang_n = spiops.solar_array_angle(minus_array, et)
                saa = spiops.solar_aspect_angles(self.name, et)
                sa_ang_p_list.append(sa_ang_p)
                if minus_array:
                    sa_ang_n_list.append(sa_ang_n)
                    saa_sa_n_list.append(saa[0][1])
                saa_sa_p_list.append(saa[0][0])
                saa_sc_x_list.append(saa[1][0])
                saa_sc_y_list.append(saa[1][1])
                saa_sc_z_list.append(saa[1][2])
                if self.name != 'MTM':
                    hga_angles_ang, hga_earth_ang = spiops.hga_angles(self.name, et)
                    hga_earth.append(hga_earth_ang)
                    hga_angles_el.append(hga_angles_ang[0])
                    hga_angles_az.append(hga_angles_ang[1])

            if minus_array:
                self.sa_ang = [
                 sa_ang_p_list, sa_ang_n_list]
                self.saa_sa = [saa_sa_p_list, saa_sa_n_list]
            else:
                self.sa_ang = sa_ang_p_list
            self.saa_sa = saa_sa_p_list
        self.saa_sc = [saa_sc_x_list, saa_sc_y_list, saa_sc_z_list]
        self.hga_earth = hga_earth
        self.hga_angles = [hga_angles_el, hga_angles_az]
        self.structures_flag = True
        self.previous_tw = self.time.window

    def __Geometry(self):
        import spiops
        distance = []
        altitude = []
        latitude = []
        longitude = []
        subpoint_xyz = []
        subpoint_pgc = []
        subpoint_pcc = []
        zaxis_target_angle = []
        myaxis_target_angle = []
        beta_angle = []
        qs, qx, qy, qz = ([], [], [], [])
        x, y, z = [], [], []
        tar = self.target
        time = self.time
        for et in time.window:
            ptarg, lt = spiceypy.spkpos(tar.name, et, tar.frame, time.abcorr, self.name)
            x.append(ptarg[0])
            y.append(ptarg[1])
            z.append(ptarg[2])
            vout, vmag = spiceypy.unorm(ptarg)
            distance.append(vmag)
            if tar.frame == 'MARSIAU':
                tar_frame = 'IAU_MARS'
            else:
                tar_frame = tar.frame
            spoint, trgepc, srfvec = spiceypy.subpnt(tar.method, tar.name, et, tar_frame, time.abcorr, self.name)
            subpoint_xyz.append(spoint)
            dist = spiceypy.vnorm(srfvec)
            altitude.append(dist)
            spglon, spglat, spgalt = spiceypy.recpgr(tar.name, spoint, tar.radii_equ, tar.flat)
            spglon *= spiceypy.dpr()
            spglat *= spiceypy.dpr()
            subpoint_pgc.append([spglon, spglat, spgalt])
            spcrad, spclon, spclat = spiceypy.reclat(spoint)
            spclon *= spiceypy.dpr()
            spclat *= spiceypy.dpr()
            subpoint_pcc.append([spclon, spclat, spcrad])
            latitude.append(spclat)
            longitude.append(spclon)
            obs_tar, ltime = spiceypy.spkpos(tar.name, et, 'J2000', time.abcorr, self.name)
            obs_zaxis = [0, 0, 1]
            obs_myaxis = [0, -1, 0]
            try:
                matrix = spiceypy.pxform(self.frame, 'J2000', et)
                z_vecout = spiceypy.mxv(matrix, obs_zaxis)
                zax_target_angle = spiceypy.vsep(z_vecout, obs_tar)
                zax_target_angle *= spiceypy.dpr()
                zaxis_target_angle.append(zax_target_angle)
                my_vecout = spiceypy.mxv(matrix, obs_myaxis)
                myax_target_angle = spiceypy.vsep(my_vecout, obs_tar)
                myax_target_angle *= spiceypy.dpr()
                myaxis_target_angle.append(myax_target_angle)
                quat = spiceypy.m2q(spiceypy.invert(matrix))
                qs.append(quat[0])
                qx.append(-1 * quat[1])
                qy.append(-1 * quat[2])
                qz.append(-1 * quat[3])
            except:
                zaxis_target_angle.append(0.0)
                myaxis_target_angle.append(0.0)
                qs.append(0.0)
                qx.append(0.0)
                qy.append(0.0)
                qz.append(0.0)

            beta_angle.append(spiops.beta_angle(self.name, self.target.name, et))

        self.distance = distance
        self.altitude = altitude
        self.latitude = latitude
        self.longitude = longitude
        self.subpoint_xyz = subpoint_xyz
        self.subpoint_pgc = subpoint_pgc
        self.subpoint_pcc = subpoint_pcc
        self.zaxis_target_angle = zaxis_target_angle
        self.myaxis_target_angle = myaxis_target_angle
        self.beta_angle = beta_angle
        self.quaternions = [qx, qy, qz, qs]
        self.trajectory = [x, y, z]
        self.geometry_flag = True
        self.previous_tw = self.time.window

    def Plot(self, yaxis='distance', date_format='TDB', external_data=[], notebook=False):
        self._Body__Geometry()
        self._Body__Structures()
        if yaxis == 'groundtrack':
            utils.plot((self.__getattribute__('longitude')), (self.__getattribute__('latitude')),
              notebook=notebook,
              xaxis_name='Longitude',
              yaxis_name='Latitude',
              mission=(self.name),
              target=(self.target.name),
              background_image=True,
              format='circle_only')
            return
        if yaxis == 'trajectory':
            if notebook:
                output_notebook()
            x = float(self.target.radii[0])
            y = float(self.target.radii[1])
            z = float(self.target.radii[2])
            s1 = figure(width=300, plot_height=300, title='X-Y [KM]')
            s1.ellipse(x=0, y=0, width=x, height=y, color='orange')
            s1.line((self.__getattribute__('trajectory')[0]), (self.__getattribute__('trajectory')[1]),
              color='red')
            s2 = figure(width=300, height=300, title='X-Z [KM]')
            s2.ellipse(x=0, y=0, width=x, height=z, color='orange')
            s2.line((self.__getattribute__('trajectory')[0]), (self.__getattribute__('trajectory')[2]),
              color='green')
            s3 = figure(width=300, height=300, title='Y-Z [KM]')
            s3.ellipse(x=0, y=0, width=y, height=z, color='orange')
            s3.line((self.__getattribute__('trajectory')[1]), (self.__getattribute__('trajectory')[2]),
              color='blue')
            show(row(s1, s2, s3))
            return
        if yaxis == 'sa_ang':
            if self.name != 'MPO':
                yaxis_name = [
                 'sa_ang_p', 'sa_ang_n']
            else:
                yaxis_name = 'sa_ang_p'
        else:
            if yaxis == 'saa_sc':
                yaxis_name = [
                 'saa_sc_x', 'saa_sc_y', 'saa_sc_z']
            else:
                if yaxis == 'saa_sa':
                    if self.name != 'MPO':
                        yaxis_name = [
                         'saa_sa_p', 'saa_sa_n']
                    else:
                        yaxis_name = 'saa_sa'
                else:
                    if yaxis == 'hga_angles':
                        yaxis_name = [
                         'hga_el', 'hga_az']
                    else:
                        if yaxis == 'hga_earth':
                            yaxis_name = 'hga_earth'
                        else:
                            if yaxis == 'quaternions':
                                yaxis_name = [
                                 'qx', 'qy', 'qz', 'qs']
                            else:
                                yaxis_name = yaxis
            utils.plot((self.time.window), (self.__getattribute__(yaxis)), notebook=notebook, external_data=external_data,
              yaxis_name=yaxis_name,
              mission=(self.name),
              target=(self.target.name),
              date_format=date_format)

    def Plot3D(self, data='trajectory', reference_frame=False):
        self._Body__Geometry()
        if not self.state_in_window:
            self._Body__StateInWindow(reference_frame=reference_frame)
        data = self.state_in_window
        utils.plot3d(data, self, self.target)


class Target(Body):

    def __init__(self, body, time=object(), target=False, frame='', method='INTERCEPT/ELLIPSOID'):
        """

        :param body:
        :type body:
        :param time:
        :type time:
        :param target: It no target is provided the default is 'SUN'
        :type target:
        :param frame:
        :type frame:
        :param method:
        :type method:
        """
        if not target:
            target = Target('SUN', time=time, target=(object()))
        else:
            super(Target, self).__init__(body, time=time, target=target)
            if not frame:
                self.frame = 'IAU_{}'.format(self.name)
            else:
                self.frame = frame
        self.method = method
        self._Target__getRadii()

    def __getRadii(self):
        try:
            self.radii = spiceypy.bodvar(self.id, 'RADII', 3)
        except:
            print('Ephemeris object has no radii')
            return
        else:
            self.radii_equ = self.radii[0]
            self.radii_pol = self.radii[2]
            self.flat = (self.radii_equ - self.radii_pol) / self.radii_equ


class Observer(Body):

    def __init__(self, body, time=object(), target=False, frame=''):
        super(Observer, self).__init__(body, time=time, target=target)
        self.frame = frame or '{}_SPACECRAFT'.format(self.name)
        if spiceypy.namfrm(self.frame) == 0:
            self.frame = self.name
        else:
            if spiceypy.namfrm(self.frame) == 0:
                self.frame = '{}_LANDER'.format(self.name)
                print('The frame name has not been able to be built; please introduce it manually')
            else:
                self.frame = frame