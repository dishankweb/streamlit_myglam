import streamlit as st

def kpi_tile(kpi,tile_text,tile_label,tile_value,delta_value,delta_value_suffix='%',delta_color_inversion='normal',
             tile_height=190,tile_value_suffix='', tile_value_prefix='', integer = False):
    tile = kpi.container(height=tile_height)
    tile.markdown(f'**{tile_text}**', help = 'definition')
    tile_value_updated = [f'{tile_value:,.0f}' if integer else f'{tile_value:,.2f}']
    tile.metric(label=tile_label, value=f"{tile_value_prefix}{tile_value_updated[0]}{tile_value_suffix}",
                delta=f'{delta_value:,.1f}{delta_value_suffix}',delta_color=delta_color_inversion)