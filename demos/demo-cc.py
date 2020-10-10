import dubins
import matplotlib
import matplotlib.pyplot as plt
import numpy

matplotlib.rcParams['figure.figsize'] = 12, 9

qs = [
	(0.0, 0.0, 0.0),
	(0.0, 0.0, numpy.pi/4),
	(4.0, 4.0, numpy.pi/4),
	(4.0, 0.0, 0.0),
	(-4.0, 0.0, 0.0),
	(4.0, 4.0, 0.0),
	(4.0, -4.0, 0.0),
	(-4.0, 4.0, 0.0),
	(-4.0, -4.0, 0.0),
	(4.0, 4.0, numpy.pi),
	(4.0, -4.0, numpy.pi),
	(0.5, 0.0, numpy.pi),
]

items = [
	(0, 4),
	(0, 5),
	(0, 6),
	(0, 7),
	(0, 8),
	(0, 9),
	(0, 10),
	(0, 11),
	(1, 2),
	(2, 1)
]

def expand_axis(ax, scale, name):
	getter = getattr(ax, 'get_' + name)
	setter = getattr(ax, 'set_' + name)
	a, b = getter()
	mid = (a+b)/2.0
	diff = (b - mid)
	setter(mid - scale*diff, mid + scale*diff)

def expand_plot(ax, scale = 1.1):
	expand_axis(ax, scale, 'xlim')
	expand_axis(ax, scale, 'ylim')

def curvature(A, B, C):
	temp = B[0]**2 + B[1]**2
	bc = (A[0]**2 + A[1]**2 - temp) / 2
	cd = (temp - C[0]**2 - C[1]**2) / 2
	det = (A[0] - B[0]) * (B[1] - C[1]) - (B[0] - C[0]) * (A[1] - B[1])

	if abs(det) < 1.0e-10:
		return(0.0)

	# Center of circle
	cx = (bc*(B[1] - C[1]) - cd*(A[1] - B[1])) / det
	cy = ((A[0] - B[0]) * cd - (B[0] - C[0]) * bc) / det

	return(1 / ((cx - A[0])**2 + (cy - A[1])**2)**.5)

def plot_dubins_path_and (q0, q1, r=1.0, step_size=0.5):
	qs, _ = dubins.path_sample(q0, q1, r, step_size)
	qs = numpy.array(qs)
	xs = qs[:, 0]
	ys = qs[:, 1]
	us = xs + numpy.cos(qs[:, 2])
	vs = ys + numpy.sin(qs[:, 2])

	curvature_points = []

	plt.subplot(1, 2, 1)
	plt.plot(xs, ys, 'b-')
	plt.plot(xs, ys, 'r.')


	for i in range(qs.shape[0]):
		# displacement along the path
		s = i * step_size

		plt.plot(
			[xs[i], us[i]], 
			[ys[i], vs[i]],
			'r-'
		)
		plt.annotate(
			'%0.1f' % (s),
			(xs[i], ys[i]),
			textcoords="offset points",
			xytext=(0,10),
			ha='center',
		)
		if (0 < i < qs.shape[0] - 1):
			k = curvature(
				(xs[i-1], ys[i-1]),
				(xs[i], ys[i]),
				(xs[i+1], ys[i+1]),
			)
			print(s, k)
			curvature_points.append((s, k))

	ax = plt.gca()
	expand_plot(ax)
	ax.set_aspect('equal')

	plt.subplot(1, 2, 2)
	plt.plot(*zip(*curvature_points))
	ax = plt.gca()
	expand_plot(ax)
	#ax.set_aspect('equal')
		
def plot_dubins_table(cols, rho=1.0):
	rows = ((len(items)) / cols)+1
	for i, (a, b) in enumerate(items):
		plt.subplot(rows, cols, i+1)
		plot_dubins_path(qs[a], qs[b], r = rho)

	plt.savefig('samples.png')
	plt.show()

if __name__ == "__main__":
	#plot_dubins_table(3, 1.0)
	plot_dubins_path(qs[0], qs[8], 3.5, 1.0)
	plt.show()


