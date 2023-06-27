# This script plots the residuals of the model
# Author: Eduardo Adame

# Imports
import unidecode
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import contextily as cx

# Read geojson file
geodf = gpd.read_file('../data/shapes.json')
geodf = geodf.rename(columns={'nomera': 'administrativeRegion'})
geodf = geodf[['administrativeRegion', 'geometry']]
geodf['administrativeRegion'] = geodf['administrativeRegion'].apply(lambda x: unidecode.unidecode(x.upper()))

# Read residuals file
residuals = pd.read_csv('../data/residuals.csv', index_col=0)

# Merging dataframes
geo_residuals = pd.merge(geodf, residuals, on='administrativeRegion')

# Make a grid plot for each year and r1, r2, r3
fig, ax = plt.subplots(3, 3, figsize=(35, 20))
for year in [2016, 2018, 2020]:
    for i, col in enumerate(['r1', 'r2', 'r3']):
        geo_residuals[geo_residuals['year'] == year].plot(column=col, cmap='RdBu', ax=ax[(year - 2016) // 2][i % 3], legend=True)
        cx.add_basemap(ax = ax[(year - 2016) // 2][i % 3], crs = geo_residuals.crs, source=cx.providers.Stamen.TonerLite)
        ax[(year - 2016) // 2][i % 3].axis('off')
        ax[(year - 2016) // 2][i % 3].set_title(f'Residuals for model M{i + 1} in {year}', fontsize=24)

fig.tight_layout()
plt.savefig('../docs/imgs/residuals.png', dpi=300, bbox_inches='tight')

# Plot administrative regions
fig, ax = plt.subplots(figsize = (10, 8))
geodf.boundary.plot(alpha=0.9, ax=ax)
geodf.plot(alpha=0.1, ax =ax)
ax.set_axis_off()
cx.add_basemap(ax = ax, crs = geodf.crs, source=cx.providers.Stamen.TonerLite)
cx.add_basemap(ax = ax, crs = geodf.crs, source=cx.providers.Stamen.TonerLabels)
ax.set_title('Administrative Regions of Rio de Janeiro', fontsize=12)
fig.savefig('../docs/imgs/ars.jpg', dpi = 200, bbox_inches='tight')