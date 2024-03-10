#!/bin/bash


function random_float_between() {
    local lower=$1
    local upper=$2

    # Generate a random integer
    local random_integer=$((RANDOM % 10000))  # Adjust the scale as needed

    # Scale the integer to a float between the specified range
    local random_float=$(echo "scale=4; $lower + $random_integer * ($upper - $lower) / 10000" | bc)

    echo $random_float
}


output_file="generated_launchfile.launch"
num_nodes=200

echo "<launch>" > "$output_file"
echo "    <arg name=\"main_turtle_name\" default=\"turtle1\" />" >> "$output_file"
echo "    <node pkg=\"turtlesim\" type=\"turtlesim_node\" name=\"turtle_simulator\" />" >> "$output_file"
echo "    <node pkg=\"turtlesim\" type=\"turtle_teleop_key\" name=\"first_turtle_handler\" />" >> "$output_file"

prev_name="\$(arg main_turtle_name)"

for ((i=2; i<=$num_nodes; i++)); do
    echo "    <node pkg=\"turtle_commander\" type=\"turtle_commander_node.py\" name=\"turtle${i}_node\" output=\"screen\">" >> "$output_file"
    echo "        <param name=\"turtle_coordinates\" value=\"$(random_float_between 0.0 11.0) $(random_float_between 0.0 11.0)\" />" >> "$output_file"
    echo "        <param name=\"turtle_speed\" value=\"1.5\" />" >> "$output_file"
    echo "        <param name=\"turtle_target\" value=\"$prev_name\" />" >> "$output_file"
    echo "        <param name=\"turtle_name\" value=\"turtle$i\" />" >> "$output_file"
    echo "    </node>" >> "$output_file"
    prev_name=turtle$i
done

echo "</launch>" >> "$output_file"

chmod +x "generated_launchfile.launch"
roslaunch "generated_launchfile.launch"
