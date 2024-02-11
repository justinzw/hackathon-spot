import os
import time
from spot_controller import SpotController

ROBOT_IP = "192.168.50.3"#os.environ['ROBOT_IP']
SPOT_USERNAME = "admin"#os.environ['SPOT_USERNAME']
SPOT_PASSWORD = "2zqa8dgw7lor"#os.environ['SPOT_PASSWORD']


def main():
    #example of using micro and speakers
    print("Start recording audio")
    sample_name = "aaaa.wav"
    cmd = f'arecord -vv --format=cd --device={os.environ["AUDIO_INPUT_DEVICE"]} -r 48000 --duration=10 -c 1 {sample_name}'
    print(cmd)
    os.system(cmd)
    print("Playing sound")
    os.system(f"ffplay -nodisp -autoexit -loglevel quiet {sample_name}")
        
    # Capture image
    import cv2
    camera_capture = cv2.VideoCapture(0)
    rv, image = camera_capture.read()
    print(f"Image Dimensions: {image.shape}")
    camera_capture.release()

    # Use wrapper in context manager to lease control, turn on E-Stop, power on the robot and stand up at start
    # and to return lease + sit down at the end
    with SpotController(username=SPOT_USERNAME, password=SPOT_PASSWORD, robot_ip=ROBOT_IP) as spot:

        # K-pop Dance Routine Start
        time.sleep(2)
        
        # Step 1: Dynamic Entry with a Bow and Head Tilt
        spot.bow(pitch=0.15, body_height=-0.1, sleep_after_point_reached=1)
        spot.move_head_in_points(yaws=[0.2], pitches=[0], rolls=[0.2], sleep_after_point_reached=0.5)
        time.sleep(1)
        
        # Step 2: Quick Side Steps with Head Movements
        for _ in range(2):
            spot.move_by_velocity_control(v_x=0, v_y=0.25, v_rot=0, cmd_duration=1)
            spot.move_head_in_points(yaws=[-0.2], pitches=[0], rolls=[-0.2], sleep_after_point_reached=0.5)
            spot.move_by_velocity_control(v_x=0, v_y=-0.25, v_rot=0, cmd_duration=1)
            spot.move_head_in_points(yaws=[0.2], pitches=[0], rolls=[0.2], sleep_after_point_reached=0.5)
        time.sleep(1)
        
        # Step 3: Rotate with Style
        spot.move_by_velocity_control(v_x=0, v_y=0, v_rot=1, cmd_duration=4)
        time.sleep(1)
        
        # Step 4: Forward and Backward Movements with Pose
        spot.move_to_goal(goal_x=0.5, goal_y=0)
        spot.move_head_in_points(yaws=[0], pitches=[0.1], rolls=[0], sleep_after_point_reached=0.5)
        time.sleep(1)
        spot.move_to_goal(goal_x=-0.5, goal_y=0)
        spot.move_head_in_points(yaws=[0], pitches=[-0.1], rolls=[0], sleep_after_point_reached=0.5)
        time.sleep(1)
        
        # Step 5: Energetic Finale with Fast Spins and a Pose
        spot.move_by_velocity_control(v_x=0, v_y=0, v_rot=-1.5, cmd_duration=5)
        time.sleep(1)
        spot.stand_at_height(body_height=0.2)
        spot.move_head_in_points(yaws=[0], pitches=[0], rolls=[0], sleep_after_point_reached=1)
        
        # K-pop Dance Routine End




if __name__ == '__main__':
    main()
