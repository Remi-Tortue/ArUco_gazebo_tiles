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

    # Map input to OpenCV ArUco dictionary
    aruco_dict_map = {
        "4x4": cv2.aruco.DICT_4X4_1000,
        "5x5": cv2.aruco.DICT_5X5_1000,
        "6x6": cv2.aruco.DICT_6X6_1000,
        "7x7": cv2.aruco.DICT_7X7_1000,
    }

    if dict_str not in aruco_dict_map:
        raise ValueError("Supported dictionaries: 4x4, 5x5, 6x6, 7x7")

    aruco_dict = cv2.aruco.getPredefinedDictionary(
        aruco_dict_map[dict_str]
    )

    marker_size_px = int(marker_size * 1000)  # output image size
    marker_img = cv2.aruco.generateImageMarker(
        aruco_dict,
        marker_id,
        marker_size_px
    )

    marker_name = f"aruco_{dict_str}_id{marker_id}_{int(marker_size*1000)}mm"
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
