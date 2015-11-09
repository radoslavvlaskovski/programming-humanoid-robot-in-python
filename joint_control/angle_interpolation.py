'''In this exercise you need to implement an angle interploation function which makes NAO executes keyframe motion

* Tasks:
    1. complete the code in `AngleInterpolationAgent.angle_interpolation`,
       you are free to use splines interploation or Bezier interploation,
       but the keyframes provided are for Bezier curves, you can simply ignore some data for splines interploation,
       please refer data format below for details.
    2. try different keyframes from `keyframes` folder

* Keyframe data format:
    keyframe := (names, times, keys)
    names := [str, ...]  # list of joint names
    times := [[float, float, ...], [float, float, ...], ...]
    # times is a matrix of floats: Each line corresponding to a joint, and column element to a key.
    keys := [[float, [int, float, float], [int, float, float]], ...]
    # keys is a list of angles in radians or an array of arrays each containing [float angle, Handle1, Handle2],
    # where Handle is [int InterpolationType, float dTime, float dAngle] describing the handle offsets relative
    # to the angle and time of the point. The first Bezier param describes the handle that controls the curve
    # preceding the point, the second describes the curve following the point.
'''


from pid import PIDAgent
from keyframes import hello
from numpy import arange
from keyframes import leftBellyToStand


class AngleInterpolationAgent(PIDAgent):
    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 teamname='DAInamite',
                 player_id=0,
                 sync_mode=True):
        super(AngleInterpolationAgent, self).__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)
        self.keyframes = ([], [], [])
        self.creation_time = self.perception.time
        self.joint_interpolationT = {}
        self.joint_interpolationA = {}
        self.count = 0
        self.keyframes_loaded = False

    def think(self, perception):
        if(self.keyframes_loaded == False and len(self.keyframes) > 0):
            self.joint_interpolationT,self.joint_interpolationA = self.load_interpolations(self.keyframes)
            self.keyframes_loaded = True
        target_joints = self.angle_interpolation(self.keyframes)
        self.target_joints.update(target_joints)
        return super(AngleInterpolationAgent, self).think(perception)

    def angle_interpolation(self, keyframes):
        target_joints = {}
        (names,times,keys) = keyframes
        
        current_time = round(self.perception.time - self.creation_time,2)
        
        for i in range(0,len(names)):
            val = self.joint_interpolationT[names[i]]
            for j,t in enumerate(val):
                if( t == current_time ):
                    target_joints[names[i]] = self.joint_interpolationA[names[i]][j]
                    if( names[i] == 'LHand'):
                        self.count += 1
                             
        return target_joints
    
    def load_interpolations(self,keyframes):
        names,times,keys = keyframes
        end_times = {k: list() for k in names}
        end_angles = {k: list() for k in names}
        
        for i in range(0,len(names)):
            for j in range(0,len(times[i])-1):
                point1 = [times[i][j],keys[i][j][0]]
                point2 = [keys[i][j][1][2],keys[i][j][1][1]]
                point3 = [keys[i][j+1][1][2],keys[i][j+1][1][1]]
                point4 = [times[i][j+1],keys[i][j+1][0]]
                (timesint,anglesint) = self.angle_interpolate(point1,point2,point3,point4)
                end_times[names[i]].extend(timesint)
                end_angles[names[i]].extend(anglesint)
        return end_times,end_angles
    
    def angle_interpolate(self,point0,point1,point2,point3):
        
        times = list()
        angles = list()

        for t in arange(0,1.0,0.01):
            u = 1-t
            tt = t*t
            ttt = tt * t
            uu = u*u
            uuu = uu*u
            x = round((uuu*point0[0]) + (3 * uu * t * point1[0]) + (3 * u * tt * point2[0]) + (ttt * point3[0]),2)
            y = round((uuu*point0[1]) + (3 * uu * t * point1[1]) + (3 * u * tt * point2[1]) + (ttt * point3[1]),2)
            times.append(x)
            angles.append(y)

        return times,angles
        

if __name__ == '__main__':
    agent = AngleInterpolationAgent()
    agent.keyframes = hello()# CHANGE DIFFERENT KEYFRAMES
    agent.run()
