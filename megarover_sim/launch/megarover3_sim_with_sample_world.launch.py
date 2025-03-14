from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_path
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess
from launch.conditions import IfCondition, LaunchConfigurationEquals
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution

from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.actions import Node

from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, LaunchConfiguration

def generate_launch_description():
    # 引数宣言
    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time', default_value='true',
        description='Use simulation (Gazebo) clock if true')
    declare_use_ros2_control = DeclareLaunchArgument(
        'use_ros2_control', default_value='false',
        choices=['true', 'false'],
        description='Use ros2_control (Gazebo) if true, otherwise use gazebo_plugin')
    declare_gui = DeclareLaunchArgument(
        'gui', default_value='true',
        choices=['true', 'false'],
        description='Set to "false" to run headless.')
    declare_gazebo = DeclareLaunchArgument(
        'gazebo', default_value='classic',
        choices=['classic', 'ignition'],
        description='Which gazebo simulator to use')
    declare_world_fname = DeclareLaunchArgument(
        'world_fname', default_value='vmegarover_sample',
        description='gazebo world name (no extension)')

    # LaunchConfigurationの取得
    use_sim_time = LaunchConfiguration('use_sim_time')
    use_ros2_control = LaunchConfiguration('use_ros2_control')
    gui = LaunchConfiguration('gui')
    world_fname = LaunchConfiguration('world_fname')
    gazebo_simulator = LaunchConfiguration('gazebo')



    # パッケージ内のlaunchディレクトリのパス
    launch_file_dir = PathJoinSubstitution([FindPackageShare('megarover_sim'), 'launch'])

    # classic gazebo の起動設定
    classic_gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([launch_file_dir, 'utils', 'classic_gazebo.launch.py'])
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'gui': gui,
            'world_fname': world_fname
        }.items(),
        condition=LaunchConfigurationEquals("gazebo", "classic")
    )

    # ignition gazebo の起動設定
    ignition_gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([launch_file_dir, 'utils', 'gz.launch.py'])
        ),
        launch_arguments={
            'gui': gui,
            'world_fname': world_fname
        }.items(),
        condition=LaunchConfigurationEquals("gazebo", "ignition")
    )


    # ros2_control の起動設定（use_ros2_controlがtrueの場合のみ）
    ros2_control_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([launch_file_dir, 'utils', 'ros2_control.launch.py'])
        ),
        condition=IfCondition(use_ros2_control)
    )



    # メガローバーを召喚
    description_package_path = get_package_share_path('megarover_description')
    default_model_path = description_package_path / 'urdf/mega3.xacro'
    default_rviz_config_path = description_package_path / 'rviz/mega3.rviz'
    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time', default_value='true',
        description='Use simulation (Gazebo) clock if true')
    
    gui_arg = DeclareLaunchArgument(name='gui', default_value='true', choices=['true', 'false'],
                                    description='Flag to enable joint_state_publisher_gui')
    model_arg = DeclareLaunchArgument(name='model', default_value=str(default_model_path),
                                      description='Absolute path to robot urdf file')
    rviz_arg = DeclareLaunchArgument(name='rvizconfig', default_value=str(default_rviz_config_path),
                                     description='Absolute path to rviz config file')

    robot_description = ParameterValue(Command(['xacro ', LaunchConfiguration('model')]),
                                       value_type=str)

    use_sim_time = LaunchConfiguration('use_sim_time')



    print("あほぼけかす",default_model_path)
    robot_description_content = Command(
        ['xacro', ' ', str(default_model_path), ' ',
        'use_ros2_control:=', use_ros2_control, ' ',
        'gazebo:=', gazebo_simulator])


    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'use_sim_time': use_sim_time,
            'robot_description': robot_description
        }]
    )

    # Depending on gui parameter, either launch joint_state_publisher or joint_state_publisher_gui
    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        condition=UnlessCondition(LaunchConfiguration('gui')),
          parameters=[
            {'use_sim_time': use_sim_time}
        ]
    )

    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        condition=IfCondition(LaunchConfiguration('gui'))
    )

    # 好みによってON・OFF
    # rviz_node = Node(
    #     package='rviz2',
    #     executable='rviz2',
    #     name='rviz2',
    #     output='screen',
    #     arguments=['-d', LaunchConfiguration('rvizconfig')],
    # )


    return LaunchDescription([
        declare_use_sim_time,
        declare_use_ros2_control,
        declare_gui,
        declare_gazebo,
        declare_world_fname,
        classic_gazebo_launch,
        ignition_gazebo_launch,
        ros2_control_launch,
        gui_arg,
        model_arg,
        rviz_arg,
        joint_state_publisher_node,
        joint_state_publisher_gui_node,
        robot_state_publisher_node,
        robot_description_content
        # rviz_node
    ])
