

# references

- [creating cascade](https://pyblog.xyz/creating-custom-haar-cascade-python-opencv/)
- [Haar Cascades](http://alereimondo.no-ip.org/OpenCV/34)
- [tutorial create samples](https://answers.opencv.org/question/103431/python-script-with-opencv_createsamples-doesnt-create-samples/)
- [tutorial make cascade](http://acodigo.blogspot.com/2015/12/entrenar-opencv-en-deteccion-de-objetos.html)
- [tutorial make cascade](https://pythonprogramming.net/haar-cascade-object-detection-python-opencv-tutorial/)
- [tool labelImg](https://github.com/tzutalin/labelImg)








opencv_createsamples -img img_0.jpg -bg bg.txt -info info/info.lst -pngoutput info -maxxangle 0.5 -maxyangle 0.5 -maxzangle 0.5 -num 1950

opencv_createsamples -info pos.dat -num 38 -w 80 -h 72 -vec pos.vec

opencv_traincascade -data ./ -vec ./pos.vec -bg ./neg.dat -numPos 38 -numNeg 212 -numStages 2 -w 80 -h 72 -featureType LBP
opencv_traincascade -data ./ -vec ./pos.vec -bg ./neg.dat -numPos 38 -numNeg 212 -numStages 2 -w 80 -h 72