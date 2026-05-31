import pandas as pd
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer

@transformer
def transform(df, *args, **kwargs):
    # Clean duplicates and build core row index
    df = df.drop_duplicates().reset_index(drop=True)
    df['trip_id'] = df.index

    # 1. Datetime Dimension
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    
    datetime_dim = pd.DataFrame({
        'datetime_id': df.index,
        'tpep_pickup_datetime': df['tpep_pickup_datetime'],
        'pick_hour': df['tpep_pickup_datetime'].dt.hour,
        'pick_day': df['tpep_pickup_datetime'].dt.day,
        'pick_month': df['tpep_pickup_datetime'].dt.month,
        'pick_year': df['tpep_pickup_datetime'].dt.year,
        'pick_weekday': df['tpep_pickup_datetime'].dt.weekday,
        'tpep_dropoff_datetime': df['tpep_dropoff_datetime'],
        'drop_hour': df['tpep_dropoff_datetime'].dt.hour,
        'drop_day': df['tpep_dropoff_datetime'].dt.day,
        'drop_month': df['tpep_dropoff_datetime'].dt.month,
        'drop_year': df['tpep_dropoff_datetime'].dt.year,
        'drop_weekday': df['tpep_dropoff_datetime'].dt.weekday
    })

    # 2. Passenger Dimension
    passenger_count_dim = pd.DataFrame({
        'passenger_count_id': df.index,
        'passenger_count': df['passenger_count']
    })

    # 3. Trip Distance Dimension
    trip_distance_dim = pd.DataFrame({
        'trip_distance_id': df.index,
        'trip_distance': df['trip_distance']
    })
        
    # 4. Rate Code Dimension
    rate_code_type = {
        1:"Standard rate", 2:"JFK", 3:"Newark",
        4:"Nassau or Westchester", 5:"Negotiated fare", 6:"Group ride"
    }
    rate_code_dim = pd.DataFrame({
        'rate_code_id': df.index,
        'RatecodeID': df['RatecodeID'],
        'rate_code_name': df['RatecodeID'].map(rate_code_type)
    })

    # 5. Pickup Location Dimension
    pickup_location_dim = pd.DataFrame({
        'pickup_location_id': df.index,
        'pickup_latitude': df['pickup_latitude'],
        'pickup_longitude': df['pickup_longitude']
    })

    # 6. Dropoff Location Dimension
    dropoff_location_dim = pd.DataFrame({
        'dropoff_location_id': df.index,
        'dropoff_latitude': df['dropoff_latitude'],
        'dropoff_longitude': df['dropoff_longitude']
    })

    # 7. Payment Type Dimension
    payment_type_name = {
        1:"Credit card", 2:"Cash", 3:"No charge",
        4:"Dispute", 5:"Unknown", 6:"Voided trip"
    }
    payment_type_dim = pd.DataFrame({
        'payment_type_id': df.index,
        'payment_type': df['payment_type'],
        'payment_type_name': df['payment_type'].map(payment_type_name)
    })

    # 8. Fact Table (Constructed instantly via index mapping without .merge())
    fact_table = pd.DataFrame({
        'trip_id': df['trip_id'],
        'VendorID': df['VendorID'],
        'datetime_id': df.index,
        'passenger_count_id': df.index,
        'trip_distance_id': df.index,
        'rate_code_id': df.index,
        'store_and_fwd_flag': df['store_and_fwd_flag'],
        'pickup_location_id': df.index,
        'dropoff_location_id': df.index,
        'payment_type_id': df.index,
        'fare_amount': df['fare_amount'],
        'extra': df['extra'],
        'mta_tax': df['mta_tax'],
        'tip_amount': df['tip_amount'],
        'tolls_amount': df['tolls_amount'],
        'improvement_surcharge': df['improvement_surcharge'],
        'total_amount': df['total_amount']
    })

    # Return pure dataframes. Mage data exporters automatically accept a dictionary of DataFrames.
    return {
        "fact_table": fact_table,
        "passenger_count_dim": passenger_count_dim,
        "trip_distance_dim": trip_distance_dim,
        "rate_code_dim": rate_code_dim,
        "pickup_location_dim": pickup_location_dim,
        "dropoff_location_dim": dropoff_location_dim,
        "datetime_dim": datetime_dim,
        "payment_type_dim": payment_type_dim
    }
