# A Bayesian approach to understanding the Homicide Rate in the City of Rio de Janeiro by administrative regions through their Social Progress Index indicators

## Abstract

This study aims to investigate the relationship between the homicide rate in the city of Rio de Janeiro and the indicators of the Social Progress Index. Our approach involves employing Bayesian methodology to estimate the parameters of three multilevel models and subsequently comparing their performance. The Social Progress Index serves as a measure of the overall quality of life and social well-being of the population, and it has been regularly published by the Pereira Passos Institute for the City of Rio de Janeiro biennially since 2016. Given the well-known issue of violence in Rio de Janeiro, the homicide rate serves as a pertinent indicator of this problem. The city is divided into 33 administrative regions, and we utilize the corresponding data throughout this research.

## Running the code

You should [download the data](https://ips-rio-pcrj.hub.arcgis.com/documents/918dd39478594792a9cfa7080b84c0b5/about) in excel format and save it in the `data` folder named `raw.xlsx`.

Then, you can run the code in the following order:

```bash
pip install -r requirements.txt
python src/create_data.py
```

And, considering you have `rstanarm` and `bayesplot` installed in R, you can run the following code:

```R
source("src/models.R")
```

If you want to get the images used in the report, you can run the following code:

```bash
python src/map_plots.py
```

and (considering you have `GGally` and `ggplot2` installed in R)

```R
source("src/eda.R")
```

Please let me now if you have any questions or suggestions.