'''In this exercise you need to implemente inverse kinematics for NAO's legs

* Tasks:
    1. solve inverse kinemtatics for NAO's legs by using analytical or numerical method.
       You may need documentation of NAO's leg:
       http://doc.aldebaran.com/2-1/family/nao_h25/joints_h25.html
       http://doc.aldebaran.com/2-1/family/nao_h25/links_h25.html
    2. use the results of inverse kinemtatics to control NAO's legs (in InverseKinematicsAgent.set_transforms)
       and test your inverse kinemtatics implementation.
'''


from forward_kinematics import ForwardKinematicsAgent
from numpy.matlib import identity
from sympy import sin
from math import atan2


class InverseKinematicsAgent(ForwardKinematicsAgent):

    def inverse_kinematics(self, effector_name, transform):
        '''solve the inverse kinematics

        :param str effector_name: name of end effector, e.g. LLeg, RLeg
        :param transform: 4x4 transform matrix
        :return: list of joint angles
        '''
        joint_angles = []

        joints = self.chains[effector_name]
        print joints
        print transform
        # YOUR CODE HERE
        return joint_angles

    def from_transform(transform):
        # return x,y,z
        x = transform[0][3]
        y = transform[1][3]
        z = transform[2][3]
        if( transform[0][0] == 1 && transform[1][1] == 1 && transform[2][2] ):
            theta = 0;
            return [x,y,z,0,0,0]
        else:
            if( transform[0][0] == 1):
                theta = atan2(transform[2][1],transform[1][1])
                return [x,y,z,theta,0,0]
            if( transform[1][1] == 1):
                theta = atan2(transform[0][2],transform[0][0])
                return [x,y,z,0,theta]
            if( transform[1][1] == 1):
                theta = atan2(trasnform[1][0],transform[0][0])
                return [x,y,z,0,0,theta]

    def set_transforms(self, effector_name, transform):
        '''solve the inverse kinematics and control joints use the results
        '''
        # YOUR CODE HERE
        joint_angles = self.inverse_kinematics(effector_name,transform)
        self.keyframes = ([], [], [])  # the result joint angles have to fill in

if __name__ == '__main__':
    agent = InverseKinematicsAgent()
    # test inverse kinematics
    T = identity(4)
    T[-1, 1] = 0.05
    T[-1, 2] = 0.26
    agent.set_transforms('LLeg', T)
    agent.run()
