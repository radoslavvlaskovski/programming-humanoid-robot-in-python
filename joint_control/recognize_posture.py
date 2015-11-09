'''In this exercise you need to use the learned classifier to recognize current posture of robot

* Tasks:
    1. load learned classifier in `PostureRecognitionAgent.__init__`
    2. recognize current posture in `PostureRecognitionAgent.recognize_posture`

* Hints:
    Let the robot execute different keyframes, and recognize these postures.

'''


from angle_interpolation import AngleInterpolationAgent
import keyframes
import pickle
from os import listdir


class PostureRecognitionAgent(AngleInterpolationAgent):
    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 teamname='DAInamite',
                 player_id=0,
                 sync_mode=True):
        super(PostureRecognitionAgent, self).__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)
        self.posture = 'unknown'
        # get the classifier created by learn_posture
        self.posture_classifier = pickle.load(open('robot_pose.pkl'))
        # get list of poses
        self.classes = listdir('robot_pose_data')

    def think(self, perception):
        self.posture = self.recognize_posture(perception)
        return super(PostureRecognitionAgent, self).think(perception)

    def recognize_posture(self, perception):
        posture = 'unknown'
        # store the current data from the perception class in a list
        data = []
        data.extend(perception.imu)
        # as shown in learn_posture get the current angle of all relative
        # joints and store in teh list 
        joints = ['LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch']
        
        for j in joints:
            data.append(perception.joint[j])
        # get the predicted Posture from the classifier and return it
        # Doesnt work properly
        posture = self.classes[self.posture_classifier.predict(data)]
        print posture
        return posture

if __name__ == '__main__':
    agent = PostureRecognitionAgent()
    agent.keyframes = keyframes.wipe_forehead()
    agent.run()
