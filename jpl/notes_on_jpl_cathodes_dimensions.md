## About the JPL cathodes
Finding consistent dimensions has been difficult and sometimes requires guesswork. I show below data compiled from many different articles. 

Goebel and Katz (2008) mention both the NEXIS and the NSTAR cathodes.
Both cathodes use barium oxide for their insert.
- NEXIS: Nuclear Electric Xenon Ion Thruster System
- NSTAR: NASA Solar Electric Propulsion Technology Applications Readiness

The NSTAR ion engine features TWO different hollow cathodes:
1. The "Discharge" hollow cathode
2. The "Neutralizer" hollow cathode
Their dimensions are different! It is also difficult to find any good information about the size of these cathodes.
Nonetheless, here are some references that set some values of these dimensions...

The JPL also built several LaB6 cathodes, with various insert diameters. The cathodes are mostly 
referred to by the outer diameter of the insert (0.63 cm, 1.5 cm, 2.0 cm), although they
are also sometimes referred to by the outer diameter of the cathode tube (0.8 cm).
The outer diameter of the insert and the outer diameter of the cathode tube are sometimes
used interchangeably (e.g. the "2.0-cm insert diameter cathode" in a given paper also has
a "2.0-cm cathode tube diameter" in a later paper).

---
## Literature review of dimensions 

### NSTAR, NEXIS
#### Mikellides et al. (2008)
- I. G. Mikellides, I. Katz, D. M. Goebel, K. K. Jameson, and J. E. Polk, ''Wear Mechanisms in Electron Sources for Ion Propulsion, I: Neutralizer Hollow Cathode,'' Journal of Propulsion and Power, vol. 24, no. 4, pp. 855–865, 2008.
- I. G. Mikellides, I. Katz, D. M. Goebel, K. K. Jameson, and J. E. Polk, ''Wear Mechanisms in Electron Sources for Ion Propulsion, II: Discharge Hollow Cathode,'' Journal of Propulsion and Power, vol. 24, no. 4, pp. 866–879, 2008.

Mikellides et al. have a table in Ref. [1] that compares the dimensions of the two cathodes. Ref. [2] contains the dimensions of the discharge hollow cathode (see Table 1).
From there, we have:

| Dimension | Neutralizer HC | Discharge HC | Ratio NHC / DHC |
|:---------:|:--------------:|:------------:|:---------------:|
| Orifice radius (mm) | 0.14 | 0.51 | 0.275 |
| Orifice length (mm) | 0.74 | 0.74 | 1 |
| Emitter insert length (cm) | 2.54 | 2.54 | 1 |
| Cathode tube diameter (cm) | 0.635 | 0.635 | 1 |

The cathode tube diameter is _not_ the insert diameter. To get the insert diameter, we have to dig down a bit deeper...

#### Sengupta (2005), Katz (2005)
- A. Sengupta, “Destructive Physical Analysis of Hollow Cathodes from the Deep Space 1 Flight Spare Ion Engine 30,000 Hr Life Test,” 29th IEPC, 2005.
- I. Katz, J. E. Polk, I. G. Mikellides, D. M. Goebel, and S. E. Hornbeck, “Combined Plasma and Thermal Hollow Cathode Insert Model,” 29th IEPC, 2005.

The cathode insert thickness is reported to be 0.769 mm (or 769 micrometers) in Sengupta.
There is a gap between the insert and the cathode tube of about 100 micrometers, as mentioned in Katz.
The insert radius + thickness of the cathode tube would then be

6.35 / 2 - 0.760 - 0.1 = 2.315 mm

Note, however, that the insert radius and thickness reported in Katz paper is different! From the graphs of plasma density and potential, we can get an insert radius of 1.9 mm, as opposed to 2.315 mm. 
The insert thickness is also obtained as 0.295 mm, as opposed to 0.769 mm from Sengupta.

#### Goebel and Katz (2008)
Goebel and Katz have some dimensions written down on various plots. 
There are obviously more references to the NSTAR than the NEXIS, as the latter is more recent with respect to the publication date.

- References to NSTAR:
..p.258: Fig 6.6: 0.38 cm-insert diameter for the NSTAR
..Fig 6.48: 0.38 cm-insert diameter for the NSTAR
.. p.249: 0.38 cm-insert diameter for the NSTAR (so the 2004 paper from JPC is for the NSTAR). 
.. p.274: 0.38 cm-insert diameter, orifice length is 0.75 mm for the NSTAR neutralizer

- References to NEXIS
.. p.246: NEXIS orifice diameter is 2.5 mm ; Goebel JAP 2005 paper suggests 2 to 3 mm, and shows results for 2 and 2.75 mm
.. p.258: Fig 6.6: 1.27 cm-insert diameter for the NEXIS
.. p.271: NEXIS orifice diameter is 2.5 mm

#### Katz et al. (2003)
- I. Katz, J. R. Anderson, J. E. Polk, and J. R. Brophy, “One-Dimensional Hollow Cathode Model,” J. Propuls. Power, vol. 19, no. 4, pp. 595–600, 2003.

Katz et al. model the _neutralizer_ NSTAR hollow cathode. From their plots, we obtain the orifice length. With no chamfer, the orifice length is 0.74 mm.

#### Mikellides et al. (2004)
- I. G. Mikellides, I. Katz, D. M. Goebel, and J. E. Polk, “Model of a Hollow Cathode Insert Plasma,” 40th AIAA/ASME/SAE/ASEE Joint Propulsion Conference and Exhibit, 2004.

Fig. 1 shows the basic dimensions of the NEXIS cathode
- Orifice diameter: 0.15 cm
- Insert length: 2.5 cm
- Insert inner diameter: 1.1 cm
- Insert outer diameter: 1.2 cm

#### Mikellides et al. (2005)
- I. G. Mikellides, I. Katz, D. M. Goebel, and J. E. Polk, “Hollow cathode theory and experiment. II. A two-dimensional theoretical model of the emitter region,” J. Appl. Phys., vol. 98, 2005.

Fig. 1 shows the basic dimensions of the NEXIS cathode. 
- Orifice diameter: 0.15 cm
- Insert length: 2.5 cm
- Insert diameter: 1.2 cm

#### Mikellides et al. (2006)
- I. G. Mikellides, I. Katz, D. M. Goebel, J. E. Polk, and K. K. Jameson, “Plasma processes inside dispenser hollow cathodes,” Phys. Plasmas, vol. 13, 2006.

Mikellides has a table with dimensions (Table 1). The actual orifice of the ``larger'' cathode (read: NEXIS) is 2.79 mm.
Note that different work has the NEXIS orifice size reported to be 2.0 mm, 2.75 mm, 3.0 mm, and ``between 2.0 and 3.0 mm...'' 
The emitter length for the NEXIS is also taken to be 2.54 cm.

The plots seem to suggest the following dimensions

| Cathode | Insert radius (mm) | Insert thickness (mm) |
|:-:|:-:|:-:|
|NSTAR| 1.9 | 0.22 |
|NEXIS| 6.0 | 0.52 |

#### Goebel, Katz, et al. (2004)
- D. M. Goebel, I. Katz, J. E. Polk, I. G. Mikellides, K. K. Jameson, T. Liu, and R. Dougherty, “Extending Hollow Cathode Life for Electric Propulsion in Long-Term Missions,” Sp. 2004 Conf. Exhib., 2004.

Figure 5 shows the dimensions of cathode. It has an insert diameter of 1.2 cm, emitter length of 2.5 cm, and orifice diameter of 0.15 cm. The figure is referenced after Mikellides et al, 2004 ("Theoretical model..."

#### Goebel, Jameson, et al. (2004)
- D. Goebel, K. K. Jameson, R. M. Watkins, and I. Katz, “Hollow Cathode and Keeper-Region Plasma Measurements Using Ultra-Fast Miniature Scanning Probes,” 40th AIAA/ASME/SAE/ASEE Jt. Propuls. Conf. Exhib., 2004.

p.3 last paragraph: the orifice diameter is 2.75 mm.

### LaB6 cathodes
#### Goebel et al (2007) 
- D. Goebel, R. M. Watkins, K. K. Jameson, "LaB6 Hollow Cathodes for Ion and Hall Thrusters," Journal of Propulsion and Power, 23(3), 552-558, 2007

- References to the "0.8 cm cathode"
.. p.555, first col.: cathode tube outer diameter: 0.8 cm
.. p.555, first col.: insert inner diameter: 0.38 cm
.. p.555, first col.: orifice diameter is identical to the inner diameter (it's a tube cathode, essentially)

- References to the "1.5 cm cathode" 
.. p.554, second col.: cathode tube wall thickness: 0.1 cm => insert outer diameter is 1.3 cm
.. p.554, second col.: insert wall thickness: 0.3 cm => insert inner diameter is 0.7 cm 
.. p.554, second col.: insert length: 2.5 cm
.. p.555, first col.: insert inner diameter (I.D.): 0.38 cm

- References to the "2.0 cm cathode"
.. p.555, first col.: cathode (outer?) tube: 2.0 cm 
.. p.555, first col.: "same tube wall and insert thicknesses as the 1.5 cm cathode" => insert outer diameter is 1.8 cm, and inner is 1.2 cm

- All cathodes
.. p.555, first col.: orifice diameter of 0.38 cm and keeper oriﬁce diameters of 0.64 cm

#### Goebel and Watkins (2010)
- D. M. Goebel and R. M. Watkins, "Compact lanthanum hexaboride hollow cathode," Review of Scientific Instruments, 81(2010), 1-7. https://doi.org/10.1063/1.3474921

- References to the "0.8 cm cathode"
.. p.3, second col: insert outer diameter: 0.64 cm
.. p.3, second col: insert inner diameter: 0.38 cm 
.. p.3, second col: insert length: 2.5 cm 
.. p.3, second col: orifice diameter is the same as the insert inner diameter: 0.38 cm

- References to the "1.5 cm cathode"
.. p.4, first col: cathode tube outer diameter: 1.5 cm 
.. p.4, first col: insert inner diameter: 0.7 cm 

- References to the "2.0 cm cathode"
.. p.4, first col: cathode tube outer diameter: 2.0 cm 
.. p.4, first col: insert inner diameter: 1.2 cm  

#### Goebel and Chu (2014)
- D. M. Goebel and E. Chu, "High Current Lanthanum Hexaboride Hollow Cathode for High-Power Hall Thrusters," Journal of Propulsion and Power, 30(1), 2014. https://doi.org/10.2514/1.B34870

- References to the "2.0 cm cathode"
.. p.36, second col.: insert inner diameter: 1.27 cm 
.. p.36, second col.: insert length: 5 cm

The orifice diameter is changed from the original 3.8 mm to 4.8 mm (3/16") and then 6.4 mm (1/4").
I believe that the latter diameter is used for every reference thereafter.

### Goebel et al (2017)
- D. M. Goebel, G. Becatti, S. Reilly, K. Tilley, and S. J. Hall, "High Current Lanthanum Hexaboride Hollow for 20-200 kW Hall Thrusters," 35th International Electric Propulsion Conference, 2017. IEPC-2017-303

- References to the "2.0 cm cathode"
.. p.3: insert outer diameter: 2.0 cm
.. p.3: insert inner diameter: 1.3 cm
.. p.3: insert length: 5.0 cm 

### Becatti et al (2017)
- G. Becatti, D. M. Goebel, J. Polk, and P. Guerrero, "Life Evaluation of a Lanthanum Hexaboride Hollow Cathode for High-Power Hall Thruster," Journal of Propulsion and Power, 34(4), 893-900 (2017) https://doi.org/10.2514/1.b36659

The cathode used in this study is the 1.5 cm cathode, but two other orifice diameters were tested: 3 mm and 5 mm.

- References to the "1.5 cm cathode"
.. p.894, second col.: orifice diameter: 3 and 5 mm 
.. p.894, second col.: insert inner diameter: 0.63 cm 
.. p.894, second col.: insert length: 2.54 cm 

### Becatti et al (2019)
- G. Becatti, D. M. Goebel, C. V. Yoke, A. L. Ortega, I. G. Mikellides, "High Current Hollow Cathode for the X3 100-kW Class Nested Hall Thruster," 36th International Electric Propulsion Conference, 2019. IEPC-2019-371

The cathode used in this study is the 2.0 cm cathode. The dimensions are nominally the same as the
2017 IEPC cathode (IEPC-2017-303).
While the original cathode used a 3.8 mm diameter orifice, the "enlarged orifice plate" now 
seemingly feature a larger orifice diameter as well. The orifice inner diameter is not explicitly 
given but can be deduced (approximately).
I have used GIMP to measure the length in pixels of both the outer plate diameter and orifice diameter
from Figure 4c and obtained 7.0 mm. Using Engauge on the results from the 2D model (Figure 15) 
I got 3.3 mm for the orifice radius. 
Both those values are close to the 6.4 mm (1/4") given in Goebel and Chu 2014. 


---
## Average cathodes

Based on the data used above, we can get the following dimensions for each cathode. If a reference appears more than once, this means that the dimension has been reported with multiple values.

#### NSTAR neutralizer cathode

| Reference | Orifice diameter (mm) | Orifice length (mm) | Insert inner diameter (mm) | Insert outer diameter (mm) | Insert thickness (mm) | Insert length (mm) | Cathode outer diameter (mm) | 
|:---------:|:---------------------:|:-------------------:|:--------------------------:|:--------------------------:|:---------------------:|:------------------:|:---------------------------:|
Katz (2003) 	       |      | 0.74 |      |       |       |      |      |
Goebel et al. (2004)   |      |      | 3.8  |       |       |      |      |
Katz (2005 IEPC)       |      |      | 3.8  | 4.39* | 0.295? |      |      | 
Sengupta (2005)        |      |      |      |       | 0.76  |      |      |
Mikellides et al (2006)|      |      | 3.8  | 4.24* | 0.22?  |      |      |
Goebel and Katz (2008) | 0.28 | 0.75 | 3.8  |       |       |      |      |
Mikellides (2008)      | 0.28 | 0.74 |      |       |       | 25.4 | 6.35 |

*: calculated OD from the thickness
?: these numbers are deduced from plots; not sure how accurate these are.


#### NSTAR discharge cathode

| Reference | Orifice diameter (mm) | Orifice length (mm) | Insert inner diameter (mm) | Insert outer diameter (mm) | Insert thickness (mm) | Insert length (mm) | Cathode outer diameter (mm) | 
|:---------:|:---------------------:|:-------------------:|:--------------------------:|:--------------------------:|:---------------------:|:------------------:|:---------------------------:|
Katz (2003) 	       |      | 0.74 |      |         |       |      |      |
Goebel et al. (2004)   |      |      | 3.8  |         |       |      |      |
Katz (2005 IEPC)       |      |      | 3.8  | 4.39*   | 0.295? |      |      | 
Sengupta (2005)        |      |      |      |         | 0.76  |      |      |
Mikellides et al (2006)|      |      | 3.8  | 4.24*   | 0.22?  |      |      |
Goebel and Katz (2008) |      | 0.75 | 3.8  |         |       |      |      |
Mikellides (2008)      | 1.02 | 0.74 |      |         |       | 25.4 | 6.35 |

*: calculated OD from the thickness
?: these numbers are deduced from plots; not sure how accurate these are.

A more accurate picture of the insert outer diameter would be:
OD = ID + 2*IThickness + 2*gap = 3.8 + 2*0.76 + 2*0.1 = 5.5 mm

#### NEXIS cathode
| Reference | Orifice diameter (mm) | Orifice length (mm) | Insert inner diameter (mm) | Insert outer diameter (mm) | Insert thickness (mm) | Insert length (mm) | Cathode outer diameter (mm) | 
|:---------:|:---------------------:|:-------------------:|:--------------------------:|:--------------------------:|:---------------------:|:------------------:|:---------------------------:|
Goebel, Katz et al (2004)    | 1.5  |      | 12.0 |     |       | 25.0 |        |
Goebel, Jameson et al (2004) | 2.75 |      |      |     |       |      |        |
Mikellides et al (2004)      | 1.5  |      | 11.0 | 12.0|       | 25.0 |  15.0  |
Mikellides et al (2005)      | 1.5  |      | 12.0 |     | 0.22  | 25.4 |  15.0  |
Goebel et al (JAP 2005)      | 2.0  |      |      |     |       |      |  15.0  |
Goebel et al (JAP 2005)      | 2.8  |      |      |     |       |      |  15.0  |
Mikellides et al (2006)      |      |      | 12.0 |     | 0.22  | 25.4 |  15.0  |
Goebel and Katz (2008)       | 2.5  |      | 12.7 |     |       |      |        |
Goebel and Katz (2008)       | 2.8  |      | 12.7 |     |       |      |        |

#### Goebel LaB6 cathodes 
##### 0.8 cm
| Reference | Orifice diameter (mm) | Orifice length (mm) | Insert inner diameter (cm) | Insert outer diameter (cm) | Insert thickness (cm) | Insert length (cm) | Cathode outer diameter (cm) | 
|:---------:|:---------------------:|:-------------------:|:--------------------------:|:--------------------------:|:---------------------:|:------------------:|:---------------------------:|
Goebel et al. (JPP 2007) | 3.8 |  |  0.38  | 0.64  |  |2.5  | 0.8 |
Goebel et al. (Rev. Sci. 2010) | 3.8 |  |  0.38  | 0.64 | 0.13 | 2.5 | 0.8 |

Thickness of Mo tube is deduced (ignoring graphite sleeves): 0.08 cm 



##### 1.5 cm
| Reference | Orifice diameter (mm) | Orifice length (mm) | Insert inner diameter (cm) | Insert outer diameter (cm) | Insert thickness (cm) | Insert length (cm) | Cathode outer diameter (cm) | 
|:---------:|:---------------------:|:-------------------:|:--------------------------:|:--------------------------:|:---------------------:|:------------------:|:---------------------------:|
Goebel et al. (JPP 2007) | 3.8 |  |  0.7  | 1.3 | 0.3 | 2.5 | 1.5 |
Goebel et al. (Rev. Sci. 2010) | 3.8 | | 0.7 |  | | 2.5 | 1.5 |

Thickness of cathode wall is 0.1 cm

##### 2.0 cm
| Reference | Orifice diameter (mm) | Orifice length (mm) | Insert inner diameter (cm) | Insert outer diameter (cm) | Insert thickness (cm) | Insert length (cm) | Cathode outer diameter (cm) | 
|:---------:|:---------------------:|:-------------------:|:--------------------------:|:--------------------------:|:---------------------:|:------------------:|:---------------------------:|
Goebel et al. (JPP 2007)        | 3.8     | | 1.2  | 1.8 | 0.3 | 2.5 | 2.0 |
Goebel et al. (Rev. Sci. 2010)  | 3.8     | | 1.2  | 2.0 |     | 2.5 | 2.0 |
Goebel and Chu (JPP 2014)       | 4.3-6.4 | | 1.27 | 2.0 |     | 5.0 | 2.0 | 
Goebel et al. (IEPC 2017)       |         | | 1.3  | 2.0 |     | 5.0 | 2.0 |
Becatti et al. (IEPC 2019)      | 6.4?    | |      |     |     |     |     |

Thickness of cathode wall is 0.1 cm
