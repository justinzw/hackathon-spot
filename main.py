import os
import time
from spot_controller import SpotController
import openai


ROBOT_IP = "192.168.50.3"#os.environ['ROBOT_IP']
SPOT_USERNAME = "admin"#os.environ['SPOT_USERNAME']
SPOT_PASSWORD = "2zqa8dgw7lor"#os.environ['SPOT_PASSWORD']


# Access the API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def call_openai(prompt):
    response = openai.create_completion(
        engine="text-davinci-002",  # Update the engine name if needed, based on available models
        prompt=prompt,
        temperature=0.7,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Example usage
prompt = "Write a short story about a space adventure."
response_text = call_openai(prompt)
print(response_text)


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

        time.sleep(2)

        # Move head to specified positions with intermediate time.sleep
        spot.move_head_in_points(yaws=[0.2, 0],
                                 pitches=[0.3, 0],
                                 rolls=[0.4, 0],
                                 sleep_after_point_reached=1)
        time.sleep(3)

        spot.make_stance(10,10)

        time.sleep(3)

        # Make Spot to move by goal_x meters forward and goal_y meters left
        spot.move_to_goal(goal_x=0.5, goal_y=0)
        time.sleep(3)

        # Control Spot by velocity in m/s (or in rad/s for rotation)
        spot.move_by_velocity_control(v_x=-0.3, v_y=0, v_rot=0, cmd_duration=2)
        time.sleep(3)

        # Dance routine start
        time.sleep(2)

        # Step 1: Exciting start with a bow
        spot.bow(pitch=0.2, body_height=0.2, sleep_after_point_reached=1)
        time.sleep(2)

        # Step 2: Spin around with velocity control
        spot.move_by_velocity_control(v_x=0, v_y=0, v_rot=0.5, cmd_duration=5)
        time.sleep(1)

        # Step 3: Side step to the left and then to the right
        spot.move_by_velocity_control(v_x=0, v_y=0.3, v_rot=0, cmd_duration=2)
        time.sleep(2)
        spot.move_by_velocity_control(v_x=0, v_y=-0.3, v_rot=0, cmd_duration=2)
        time.sleep(2)

        # Step 4: Move forward in a zigzag pattern
        for _ in range(2):
            spot.move_by_velocity_control(v_x=0.2, v_y=0.1, v_rot=0, cmd_duration=1)
            time.sleep(1)
            spot.move_by_velocity_control(v_x=0.2, v_y=-0.1, v_rot=0, cmd_duration=1)
            time.sleep(1)

        # Step 5: Final pose with a bow
        spot.bow(pitch=-0.2, body_height=0.1, sleep_after_point_reached=1)
        time.sleep(2)

        # Dance routine end



if __name__ == '__main__':
    main()
