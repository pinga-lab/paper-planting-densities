Code, Latex source, figures and supplementary material for the article
published in journal [Geophysics](http://library.seg.org/toc/gpysa7/77/4)

Results were generated using open-source software [Fatiando a
Terra](http://fatiando.org).

The method described in the paper is implemented in module
[fatiando.gravmag.harvester](fatiando.readthedocs.org/en/releases/api/gravmag.harvester.html).

The published article is available at
[doi:190/geo2011-0388.1](http://library.seg.org/doi/abs/10.1190/geo2011-0388.1)

A PDF version of the article is also available from
[my personal page](http://fatiando.org/people/uieda/).

Supplementary material on figshare:

* [Animation of the inversion process](http://dx.doi.org/10.6084/m9.figshare.91469)
* [Supplement with results not included in the text](http://dx.doi.org/10.6084/m9.figshare.91574)

Citation:

Uieda, L., and V. C. F. Barbosa (2012), Robust 3D gravity gradient inversion by
planting anomalous densities, Geophysics, 77(4), G55-G66,
doi:10.1190/geo2011-0388.1

# Robust 3D gravity gradient inversion by planting anomalous densities

**Leonardo Uieda and Valéria C. F. Barbosa**

We have developed a new gravity gradient inversion method for estimating a 3D
density-contrast distribution defined on a grid of rectangular prisms. Our
method consists of an iterative algorithm that does not require the solution of
an equation system. Instead, the solution grows systematically around
user-specified prismatic elements, called "seeds," with given density
contrasts. Each seed can be assigned a different density-contrast value,
allowing the interpretation of multiple sources with different density
contrasts and that produce interfering signals. In real world scenarios, some
sources might not be targeted for the interpretation. Thus, we developed a
robust procedure that neither requires the isolation of the signal of the
targeted sources prior to the inversion nor requires substantial prior
information about the nontargeted sources. In our iterative algorithm, the
estimated sources grow by the accretion of prisms in the periphery of the
current estimate. In addition, only the columns of the sensitivity matrix
corresponding to the prisms in the periphery of the current estimate are needed
for the computations. Therefore, the individual columns of the sensitivity
matrix can be calculated on demand and deleted after an accretion takes place,
greatly reducing the demand for computer memory and processing time. Tests on
synthetic data show the ability of our method to correctly recover the geometry
of the targeted sources, even when interfering signals produced by nontargeted
sources are present. Inverting the data from an airborne gravity gradiometry
survey flown over the iron ore province of Quadrilátero Ferrífero, southeastern
Brazil, we estimated a compact iron ore body that is in agreement with geologic
information and previous interpretations.


