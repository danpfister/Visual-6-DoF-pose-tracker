import cv2
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

def main():
    rospy.init_node('camera_publisher', anonymous=True)
    pub = rospy.Publisher('/camera/image_color', Image, queue_size=10)
    bridge = CvBridge()
    
    # Open the USB camera
    cap = cv2.VideoCapture('/dev/video0')
    
    if not cap.isOpened():
        print("Cannot open camera")
        return
    
    print("starting publishing to /camera/image_color")
    
    while not rospy.is_shutdown():
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        # Convert OpenCV image to ROS Image message
        img_msg = bridge.cv2_to_imgmsg(frame, encoding="bgr8")
        
        # Publish to the topic
        pub.publish(img_msg)
    
    cap.release()

if __name__ == '__main__':
    main()
