gif:
	convert -loop 0 \
	-delay 100 setup.png seeds.png neighbors.png predicted.png \
	-delay 10 slides/*.png \
	-delay 50 slides/chset0249.png \
	plant_anim.gif

lowres:
	convert -loop 0 \
	-delay 100 setup.png seeds.png neighbors.png predicted.png \
	-delay 10 slides/*.png \
	-delay 50 slides/chset0249.png \
	-resize 25% plant_anim_lowres.gif

clean:
	rm plant_anim.gif plant_anim_lowres.gif
