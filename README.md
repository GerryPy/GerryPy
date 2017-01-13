![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)
[![License](https://img.shields.io/badge/license-MIT%20License-brightgreen.svg)](https://opensource.org/licenses/MIT)


# GerryPy
GerryPy is a geospatial algorithm for building congressional districts.

GerryPy takes census tracts for the state of Colorado and builds the required number of congressional districts.  The algorithm attempts to make districts compact and close to the required population of 711,000.  Each algorithm attempt produces a different result.

# Website
gerrypy.herokuapp.com

# Major Components
GerryPy is built in Python and uses a PostGRES/PostGIS database.  

PostGIS functions and GoogleMaps support and display the spatial data.

Pyramid ORM and Bootstrap for the website.

# Planned features
1) Added criteria for how the algorithm should prefer to group census tracts.

2) Support for all 50 states.

3) Run algorithm multiple times and select the best one.

# License
MIT License

# Team
[Ford Fowler](https://github.com/fordf "Good At Everything")

[Avery Pratt](https://github.com/averyprett "Found Another Edge Case in the Algorithm")

[Patrick Saunders](https://github.com/pasaunders "Legal Mind and Test Master")

[Jordan Schatzman](https://github.com/julienawilson "Database Genius")

[Julien Wilson](https://github.com/julienawilson "The Mapper")
