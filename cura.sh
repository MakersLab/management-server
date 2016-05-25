A=$(sudo /home/pi/CuraEngine/build/CuraEngine -v ./uploads/temporary.stl -o $1.gcode 2>&1 | tail -3 | head -1 | cut -d" " -f3)
python -c "print round($A/3600.0, 1)*200"
