# clearskydays

# Description 
A simple Python module that determines clear sky days based on solar radiation measurements.

# Installation 
pip install clearskydays

# Authors
- Abel Delgado Villalba. Universidad Nacional de Asuncion, Paraguay. email: <adelgado@pol.una.py>
- Marcelo de Paula Correa. Universidade Federal de Itajuba, Brazil. email: <mpcorrea@unifei.edu.br>

# Example
from clearskydays import Statistics
data = Statistics(time_series) # input data
data.get_statistics()
data.get_clear_sky_days()
data.get_cloudy_days()
