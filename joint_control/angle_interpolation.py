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


class AngleInterpolationAgent(PIDAgent):
    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 teamname='DAInamite',
                 player_id=0,
                 sync_mode=True):
        super(AngleInterpolationAgent, self).__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)
        self.keyframes = ([], [], [])

    def think(self, perception):
        target_joints = self.angle_interpolation(self.keyframes)
        self.target_joints.update(target_joints)
        return super(PIDAgent, self).think(perception)

    def angle_interpolation(self, keyframes):
        target_joints = {}
        (names,times,keys) = keyframes

        for i in range(0,len(names)):
            target_joints[names[i]] = self.interpolation(i)
        
        return target_joints

    def interpolation(self,joint):
        
        interpolations = list()
        joint_angles = list()
        joint_times = list()
        point_angle1 = list()
        point_angle2 = list()
        joint_points = list()

        (names,times,keys) = self.keyframes

        for x in range(0,len(keys[joint])):
            joint_angles.append(keys[joint][x][0])
            joint_times.append(times[joint][x])
            point_angle1.append(keys[joint][x][1])
            point_angle2.append(keys[joint][x][2])
        
        joint_points = zip(joint_times,joint_angles)
        
        for x in range(0,len(joint_times)-1):            
            interpolations.append(self.angle_interpolate(joint_points[x],point_angle1[x],point_angle2[x+1],joint_points[x+1]))
        
        if( joint == 0 ):
            print interpolations
        
        return interpolations
    
    def angle_interpolate(self,point0,point1,point2,point3):
        
        b = 0.0
        t = 0.5
        
        return b
        
        

if __name__ == '__main__':
    agent = AngleInterpolationAgent()
    agent.keyframes = hello()  # CHANGE DIFFERENT KEYFRAMES
    agent.run()
