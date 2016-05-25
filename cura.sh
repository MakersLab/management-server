A=$(sudo /home/pi/CuraEngine/build/CuraEngine -v ./uploads/temporary.stl -o $1.gcode 2>&1 | tail -3 | head -1 | cut -d" " -f3)
echo $A
