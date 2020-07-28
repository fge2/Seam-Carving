# Seam-Carving
A visualization and GUI of the seam carving algorithm for content aware image resizing. This is a project to explore a real life implementation of dynamic programming and to visualize code using tkinter GUIs in python. Seams are calculated by calculating an energy matrix for each pixel in the image and then using dynamic programming to find the least cost seam down the height of the image before removing the seam. A previous version of the code used Dijkstra's algorithm to find the shortest path, but I find that dynamic programming yields slightly better run times.

## GUI buttons
The GUI preloads a default image but allows users to upload and save custom images after resizing. A slider controls the desired size of resizing as a percentage. "Carve" starts the main algorithm. 

```
python CarveVisualizer.py
```
![Default GUI](HJoceanSmall.png)
