import cv2
import sys
import pathlib
import os

PKG_PATH = str(pathlib.Path(__file__).parent.parent.resolve())


#


def main():
    if len(sys.argv) != 4:
        print("Usage: python3 main.py <DICT> <ID> <SIZE>")
        print("Example: python3 main.py 7x7 2 0.1")
        sys.exit(1)

    dict_str = sys.argv[1]
    marker_id = int(sys.argv[2])
    marker_size = float(sys.argv[3])  # in meters

    # Map input to OpenCV marker dictionary
    marker_dict_map = {
        "DICT_4X4_50":         cv2.aruco.DICT_4X4_50,
        "DICT_4X4_100":        cv2.aruco.DICT_4X4_100,
        "DICT_4X4_250":        cv2.aruco.DICT_4X4_250,
        "DICT_4X4_1000":       cv2.aruco.DICT_4X4_1000,
        "DICT_5X5_50":         cv2.aruco.DICT_5X5_50,
        "DICT_5X5_100":        cv2.aruco.DICT_5X5_100,
        "DICT_5X5_250":        cv2.aruco.DICT_5X5_250,
        "DICT_5X5_1000":       cv2.aruco.DICT_5X5_1000,
        "DICT_6X6_50":         cv2.aruco.DICT_6X6_50,
        "DICT_6X6_100":        cv2.aruco.DICT_6X6_100,
        "DICT_6X6_250":        cv2.aruco.DICT_6X6_250,
        "DICT_6X6_1000":       cv2.aruco.DICT_6X6_1000,
        "DICT_7X7_50":         cv2.aruco.DICT_7X7_50,
        "DICT_7X7_100":        cv2.aruco.DICT_7X7_100,
        "DICT_7X7_250":        cv2.aruco.DICT_7X7_250,
        "DICT_7X7_1000":       cv2.aruco.DICT_7X7_1000,
        "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
        "DICT_APRILTAG_16h5":  cv2.aruco.DICT_APRILTAG_16h5,
        "DICT_APRILTAG_25h9":  cv2.aruco.DICT_APRILTAG_25h9,
        "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
        "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
    }

    if dict_str not in marker_dict_map:
        raise ValueError("Supported dictionaries:", ", ".join(marker_dict_map.keys()))

    aruco_dict = cv2.aruco.getPredefinedDictionary(
        marker_dict_map[dict_str]
    )

    marker_size_px = int(marker_size * 1000)  # output image size
    marker_img = cv2.aruco.generateImageMarker(
        aruco_dict,
        marker_id,
        marker_size_px
    )

    marker_name = f"marker_{dict_str}_id{marker_id}_{int(marker_size*1000)}mm"
    marker_png_file = PKG_PATH + "/markers/" + marker_name + ".png"
    print(f"Saving marker to: {marker_png_file}")
    cv2.imwrite(marker_png_file, marker_img)

    print(f"Saved: {marker_png_file}")
    print(f"Q to quit and create gazebo tile model...")

    cv2.imshow("Marker", marker_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #

    # creat model folder
    models_dir = os.path.join(PKG_PATH, "models", marker_name)
    os.makedirs(models_dir, exist_ok=True)
    # add material texture
    material_models_dir = os.path.join(models_dir, "materials")
    textures_models_dir = os.path.join(material_models_dir, "textures")
    os.makedirs(textures_models_dir, exist_ok=True)
    marker_png_file = textures_models_dir + '/' + marker_name + ".png"
    cv2.imwrite(marker_png_file, marker_img)
    # add material texture script
    scripts_models_dir = os.path.join(material_models_dir, "scripts")
    os.makedirs(scripts_models_dir, exist_ok=True)
    script = f"""
material {marker_name}/Marker

{{
    technique
    {{
        pass
        {{
            texture_unit
            {{
                texture {marker_name}.png
            }}
        }}
    }}
}}
    """
    material_script_file = scripts_models_dir + '/' + marker_name + '.material'
    with open(material_script_file, 'w') as f:
        f.write(script)

    # create model config files
    model_config = f"""
<?xml version="1.0"?>

<model>
    <name>{marker_name}</name>
    <version>1.0</version>
    <sdf version="1.6">model.sdf</sdf>

    <author>
        <name>Porée Rémi</name>
        <email>remi.poree.pro@protonmail.com</email>
    </author>

    <description>
        A simple marker tile model.
    </description>
</model>
    """
    model_config_file = os.path.join(models_dir, "model.config")
    with open(model_config_file, 'w') as f:
        f.write(model_config)

    # create model sdf file
    model_sdf = f"""
<?xml version="1.0"?>
<sdf version="1.6">
<model name="{marker_name}">
    <pose>0 0 0 0 0 0</pose>
    <static>true</static>
    <link name="link">
    <collision name="collision">
        <geometry>
        <box>
            <size>{marker_size+0.03} {marker_size+0.03} -0.01</size>
        </box>
        </geometry>
    </collision>
    <visual name="visual">
        <geometry>
        <box>
            <size>{marker_size+0.03} {marker_size+0.03} -0.01</size>
        </box>
        </geometry>
    </visual>
    <!-- Marker visual on the front face -->
    <visual name="marker_front">
        <pose>0 0 0.006 0 0 -1.5706</pose>
        <geometry>
            <plane>
                <normal>1 0 0</normal>
                <size>{marker_size} {marker_size}</size>
            </plane>
        </geometry>
        <material>
            <script>
                <uri>model://{marker_name}/materials/scripts</uri>
                <uri>model://{marker_name}/materials/textures</uri>
                <name>{marker_name}/Marker</name>
            </script>
        </material>
    </visual>
    </link>
</model>
</sdf>
    """
    model_sdf_file = os.path.join(models_dir, "model.sdf")
    with open(model_sdf_file, 'w') as f:
        f.write(model_sdf)

    print(f"Tile created !")

if __name__ == "__main__":
    main()
