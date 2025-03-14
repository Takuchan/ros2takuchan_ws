# Overview
僕が作ったROS2のモジュールを集めたリポジトリです。

## megarover_sim
### 事前準備
1. [megarover Ver3.0 公式GitHubn](https://github.com/vstoneofficial/megarover3_ros2)
こちらのReadme.mdに記載されているインストールをすべて行う。
2. ROS2のバージョンに応じたGazeboをインストールする。[Gazebo binaryインストール](https://gazebosim.org/docs/fortress/install_ubuntu/)
2. 本リポジトリをcolcon buildする。
### 実行方法
`robot_state_publisher`のトピックを発行するために以下のプログラムをはじめに実行する。

```
ros2 launch megarover_description mega3_view.launch.py
```
次に、odometryを実行して自己位置推定ができるようにする。

```
ros2 launch megarover3_bringup robot.launch.py
```
最後に以下のローンチファイルを実行する
```
ros2 launch megarover_sim megarover3_sim_with_sample_world.launch.py gazebo:=ignition use_ros2_control:=true

ros2 run teleop_twist_keyboard teleop_twist_keyboard
```
### エラーが出た場合
| The following packages have unmet dependencies:
 gz-tools2 : Conflicts: gazebo (>= 11.0.0) but 11.10.2+dfsg-1 is to be installed
             Conflicts: gazebo (<= 11.14.0) but 11.10.2+dfsg-1 is to be installed
E: Error, pkgProblemResolver::Resolve generated breaks, this may be caused by held packages.

このようなエラーが出た場合は僕は`gz-tools`を消した
```
sudo apt remove gz-tools2
```