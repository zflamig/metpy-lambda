import os
# override this for pooch and the metpy test data
os.environ['XDG_CACHE_HOME'] = '/tmp'

import json
import boto3

import matplotlib
matplotlib.use('agg')

# change the data path so it downloads to a writeable directory
from cartopy import config as cartopyconfig
cartopyconfig['data_dir'] = '/tmp/'

import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import xarray as xr
import pooch

from metpy.testing import get_test_data

def lambda_handler(event, context):
    ds = xr.open_dataset(get_test_data('narr_example.nc', as_file_obj=False))
    data_var = ds.metpy.parse_cf('Temperature')

    x = data_var.x
    y = data_var.y
    im_data = data_var.isel(time=0).sel(isobaric=1000.)

    fig = plt.figure(figsize=(14, 14))
    ax = fig.add_subplot(1, 1, 1, projection=data_var.metpy.cartopy_crs)

    ax.imshow(im_data, extent=(x.min(), x.max(), y.min(), y.max()),
          cmap='RdBu', origin='lower' if y[0] < y[-1] else 'upper')
    ax.coastlines(color='tab:green', resolution='110m')
    ax.add_feature(cfeature.LAKES.with_scale('110m'), facecolor='none', edgecolor='tab:blue')
    ax.add_feature(cfeature.RIVERS.with_scale('110m'), edgecolor='tab:blue')

    save_path = "/tmp/example.png"
    plt.savefig(save_path)
    
    boto3.resource('s3').meta.client.upload_file(save_path, 'yourdemobucket', 'example.png')

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
