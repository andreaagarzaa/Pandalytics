import pandas as pd
import pyarrow.feather as feather

defects_cols = [
    'Codigo defecto',
    'Defecto',
    'Ubicacion',
    'Es Contencion',
    'Es Prevencion',
    'Es Mejora',
    'Intensidad',
    'Cara',
    'Lado',
    'Linea Origen',
    'Dictamen',
    'Resolución',
    'Calidad Sugerida',
    'Siguiente Accion',
    'Siguiente Proceso',
    'Mts Ini',
    'Mts Fin',
    'Frecuencia',
    'Causa',
    'Accion Preventiva',
    'Accion Correctiva',
    'Observaciones',
    'Fecha Registro',
    'Registro Automatico',
    'Código Equipo',
]


def extract_defects_df(production_df: pd.DataFrame):
    """
    This function aims to extract defects data from a production DataFrame, assuming it has specified columns labeled
    with defect types and corresponding numerical identifiers in brackets like ' (1)', ' (2)', etc. for multiple observations.

    It drops NA values and concatenates the data to form a unified DataFrame that captures all the defects detail.
    The final DataFrame is indexed serially.

    Parameters:
    production_df (DataFrame): pandas DataFrame with production data, expected to include defects_cols with numerical identifiers.

    Returns:
    defects_df: A DataFrame containing the combined defects data from all the identities.
    """
    defects_df_1 = production_df[map(lambda x: x + ' (1)', defects_cols)].dropna(thresh=1)
    defects_df_1.columns = defects_cols
    defects_df_2 = production_df[map(lambda x: x + ' (2)', defects_cols)].dropna(thresh=1)
    defects_df_2.columns = defects_cols
    defects_df_3 = production_df[map(lambda x: x + ' (3)', defects_cols)].dropna(thresh=1)
    defects_df_3.columns = defects_cols
    defects_df_4 = production_df[map(lambda x: x + ' (4)', defects_cols)].dropna(thresh=1)
    defects_df_4.columns = defects_cols
    defects_df_5 = production_df[map(lambda x: x + ' (5)', defects_cols)].dropna(thresh=1)
    defects_df_5.columns = defects_cols

    # the defect ID is the same as the id for its respective production line. As such, we can extract
    # it using reset_index to reference the original production line id in a new column.
    # then, the resulting dfs are concatenated while ignoring the existing index.
    defects_df = pd.concat([
        defects_df_1.reset_index(names='production_id'),
        defects_df_2.reset_index(names='production_id'),
        defects_df_3.reset_index(names='production_id'),
        defects_df_4.reset_index(names='production_id'),
        defects_df_5.reset_index(names='production_id'),
    ], ignore_index=True)

    return defects_df


def remove_defects_cols(production_id: pd.DataFrame):
    """
    Remove defects columns from the given production_id DataFrame.

    :param production_id: The DataFrame containing the production data.
    :return: The DataFrame with defects columns removed.
    """
    columns_to_remove = list(map(lambda x: x + ' (1)', defects_cols)) + list(
        map(lambda x: x + ' (2)', defects_cols)) + list(map(lambda x: x + ' (3)', defects_cols)) + list(
        map(lambda x: x + ' (4)', defects_cols)) + list(map(lambda x: x + ' (5)', defects_cols))
    return production_id.drop(columns=columns_to_remove)


if __name__ == '__main__':
    coating_df_file = ''
    coating_df = pd.concat(pd.read_excel('ternium-data/P12. Pinturas Revestidos Mx Jul20-Ago23_psch.xlsx',
                                         sheet_name=[
                                             'Pintado 1 UNI Abril',
                                             'Pintado 2 UNI Abril',
                                             'Pintado 1 UNI Mayo',
                                             'Pintado 2 UNI Mayo',
                                             'Pintado 1 UNI Junio',
                                             'Pintado 2 UNI Junio',
                                             'Pintado 1 UNI Julio',
                                             'Pintado 2 UNI Julio',
                                             'Pintado 1 UNI Ago',
                                             'Pintado 2 UNI Ago',
                                         ]).values(), ignore_index=True)
    # Análisis de consumo
    paint_analysis_df = pd.read_excel('ternium-data/Exp_2_Pintura_Estructura Analisis de consumo y .xlsx',
                                      sheet_name='Base de datos por pintura')
    paint_square_meters_df = pd.read_excel('ternium-data/Exp_2_Pintura_Estructura Analisis de consumo y .xlsx',
                                           sheet_name='Metros')
    paint_performance_df = pd.read_excel('ternium-data/Exp_2_Pintura_Estructura Analisis de consumo y .xlsx',
                                         sheet_name='Rendimientos INDU')
    # join production summaries
    production_df = pd.concat([
        pd.read_excel(
            'ternium-data/Archivos piso planta reales/ResumenProduccion_AbrilPintado1.xlsx',
            sheet_name='ResumenProduccion'
        ),
        pd.read_excel(
            'ternium-data/Archivos piso planta reales/ResumenProduccion_AbrilPintado2.xlsx',
            sheet_name='ResumenProduccion'
        ),
        pd.read_excel(
            'ternium-data/Archivos piso planta reales/ResumenProduccion_MayoPintado1.xlsx',
            sheet_name='ResumenProduccion'
        ),
        pd.read_excel(
            'ternium-data/Archivos piso planta reales/ResumenProduccion_MayoPintado2.xlsx',
            sheet_name='ResumenProduccion'
        ),
        pd.read_excel(
            'ternium-data/Archivos piso planta reales/ResumenProduccion_JunioPintado1.xlsx',
            sheet_name='ResumenProduccion'
        ),
        pd.read_excel(
            'ternium-data/Archivos piso planta reales/ResumenProduccion_JunioPintado2.xlsx',
            sheet_name='ResumenProduccion'
        ),
        pd.read_excel(
            'ternium-data/Archivos piso planta reales/ResumenProduccion_JulioPintado1.xlsx',
            sheet_name='ResumenProduccion'
        ),
        pd.read_excel(
            'ternium-data/Archivos piso planta reales/ResumenProduccion_JulioPintado2.xlsx',
            sheet_name='ResumenProduccion'
        ),
        pd.read_excel(
            'ternium-data/Archivos piso planta reales/ResumenProduccion_AgostoPintado1.xlsx',
            sheet_name='ResumenProduccion'
        ),
        pd.read_excel(
            'ternium-data/Archivos piso planta reales/ResumenProduccion_AgostoPintado2.xlsx',
            sheet_name='ResumenProduccion'
        )
    ], ignore_index=True)

    # extract defects from production summary
    defects_df = extract_defects_df(production_df)

    # clean up production production dataframe
    production_df.index = production_df.index.astype(str)

    production_df.rename(columns={
        'Material Entrada': 'input_material_code',
        'Material Salida': 'output_material_code',
        'Fecha Inicio': 'start_date',
        'Fecha Fin': 'end_date',
        'Cliente': 'client_name',
        'Código Clear Inf': 'inferior_clear_code',
        'Código Clear Sup': 'superior_clear_code',
        'Ancho 1': 'width1_mm',
        'Ancho 2': 'width2_mm',
        'Ancho 3': 'width3_mm',
        'Ancho': 'width_mm',
        'Espesor 1': 'thickness1_mm',
        'Espesor 2': 'thickness2_mm',
        'Espesor 3': 'thickness3_mm',
        'Espesor': 'thickness_mm',
        'Peso Entrada': 'input_weight_kg',
        'Peso': 'weight_kg',
        'Largo': 'length_m',
        'Color Inferior': 'inferior_color_code',
        'Color Superior': 'superior_color_code',
        'Primer Superior': 'superior_primer_code',
        'Primer Inferior': 'inferior_primer_code',
        'Ruta Teórica': 'route',
    }, inplace=True, errors='raise')

    production_df = production_df[[
        'input_material_code',
        'output_material_code',
        'start_date',
        'end_date',
        'client_name',
        'inferior_clear_code',
        'superior_clear_code',
        'width1_mm',
        'width2_mm',
        'width3_mm',
        'width_mm',
        'thickness1_mm',
        'thickness2_mm',
        'thickness3_mm',
        'thickness_mm',
        'input_weight_kg',
        'weight_kg',
        'length_m',
        'inferior_color_code',
        'superior_color_code',
        'superior_primer_code',
        'inferior_primer_code',
        'route',
    ]]

    # clean up defects dataframe
    defects_df.rename(columns={
        'Codigo defecto': 'defect_code',
        'Defecto': 'defect_name',
        'Ubicacion': 'location',
        'Es Contencion': 'is_containment',
        'Es Prevencion': 'is_preventive',
        'Intensidad': 'intensity',
        'Cara': 'face',
        'Lado': 'side',
        'Frecuencia': 'frequency',
        'Fecha Registro': 'register_date',
    }, inplace=True, errors='raise')

    defects_df = defects_df[[
        'defect_code',
        'defect_name',
        'location',
        'is_containment',
        'is_preventive',
        'intensity',
        'face',
        'side',
        'frequency',
        'register_date',
    ]]

    # clean up paint coating dataframe
    coating_df.rename(columns={
        'Denominación objeto': 'production_line',
        'Material': 'paint_id',
        'Texto breve de material': 'paint_name',
        '    Valor var.': 'monetary_value_usd',
        'Ctd.total reg.': 'total_liters_used',
        'Planta': 'production_plant',
        'Proveedor': 'supplier',
        'Registrado': 'date',
        'Hora': 'hour',
        'Precio': 'price_per_liter'
    }, inplace=True, errors='raise')

    coating_df = coating_df[[
        'production_line',
        'paint_id',
        'paint_name',
        'monetary_value_usd',
        'total_liters_used',
        'production_plant',
        'supplier',
        'date',
        'hour',
        'price_per_liter'
    ]]

    # clean up paint analysis dataframe
    paint_analysis_df.rename(columns={
        'Linea ': 'production_line',
        'Mes': 'month',
        'Mes num': 'month_number',
        'Pintura': 'paint',
        'Real': 'real_consumption',
        'Teo': 'theoretical_consumption',
        'Dif': 'consumption_difference',
        'Rendimeinto Std': 'average_yield',
        'Rendimeinto Real': 'real_yield',
        'Diferencia de Rendimiento': 'yield_difference',
        'Metros cuadrados reales': 'real_produced_square_meters',
    }, inplace=True, errors='raise')

    paint_analysis_df = paint_analysis_df[[
        'production_line',
        'month',
        'month_number',
        'paint',
        'real_consumption',
        'theoretical_consumption',
        'consumption_difference',
        'average_yield',
        'real_yield',
        'yield_difference',
        'real_produced_square_meters'
    ]]

    # clean up paint square meters dataframe
    paint_square_meters_df.rename(columns={
        'Linea': 'production_line',
        'Mes': 'month',
        'Num mes': 'month_number',
        'Pintura': 'paint_name',
        'Metros cuadrados reales (m2)': 'real_square_meters',
    }, inplace=True, errors='raise')

    # clean up paint performance dataframe
    paint_performance_df.rename(columns={
        'Pintura': 'paint_name',
        'Clave': 'paint_code',
        'Rendimiento Canning [m2/L]': 'paint_performance_m2/l'
    }, inplace=True, errors='raise')

    # write all dataframes to disk
    feather.write_feather(coating_df, 'data/pinturas_revestidos_jul20_ago23.feather')

    feather.write_feather(paint_analysis_df, 'data/analisis_consumo_pintura.feather')
    feather.write_feather(paint_square_meters_df, 'data/pintura_metros_cuadrados_reales.feather')
    feather.write_feather(paint_performance_df, 'data/rendimiento_pintura.feather')

    feather.write_feather(production_df, 'data/production.feather')
    feather.write_feather(defects_df, 'data/defects.feather')
