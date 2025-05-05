# XBoolArray

A Python module providing a multidimensional boolean array with annotated dimensions and coordinates.

## Overview

`XBoolArray` is a versatile class that allows you to create and manipulate multidimensional boolean arrays with named dimensions and coordinates. Built on top of `xarray` and `numpy`, it makes it easier to work with complex boolean data structures.

## Key Features

- **Named Dimensions**: Every axis in the array has a meaningful name
- **Dynamic Expansion**: Dimensions and coordinates can be added dynamically at any time
- **Flexible Coordinate Selection**: Select data by coordinate names rather than numeric indices
- **Boolean Operations**: Designed specifically for boolean data with appropriate methods
- **Dimension Reduction**: Sum over specified dimensions to analyze data patterns
- **Intuitive API**: Simple interface for adding data, selecting slices, and performing operations

## Installation

```bash
pip install xboolarray
```

## Dependencies

- numpy
- xarray

## Usage

### Basic Usage

```python
from xboolarray import XBoolArray

# Initialize with some axis names
xboolarray = XBoolArray(["axis1", "axis2"])

# Add data with existing dimensions
xboolarray.add_data({"axis1": "coord1_1", "axis2": "coord2_1"})

# Add data with new coordinates
xboolarray.add_data({"axis1": "coord1_2", "axis2": ["coord2_2", "coord2_3"]})

# Print the current state of the XBoolArray
print(xboolarray)
```

### Dynamic Dimension Addition

```python
# Add data with a new dimension
xboolarray.add_data({"axis1": "coord1_3", "axis2": "coord2_3", "axis3": "coord3_1"})

# Add more data across multiple dimensions
xboolarray.add_data({
    "axis1": "coord1_4", 
    "axis2": ["coord2_1", "coord2_2"], 
    "axis3": ["coord3_1", "coord3_2"]
})
```

### Selecting Slices

```python
# Select a specific slice of the array
slice_result = xboolarray.select({
    "axis1": ["coord1_3", "coord1_4"], 
    "axis2": "coord2_1"
})
print(slice_result)
```

### Summing Over Dimensions

```python
# Sum over one dimension
sum_result = xboolarray.sum("axis2")
print(sum_result)

# Sum over multiple dimensions
sum_result = xboolarray.sum(["axis2", "axis1"])
print(sum_result)

# Select and then sum
sum_selected = xboolarray.sum_selected({"axis1": "coord1_4"}, "axis3")
print(sum_selected)
```

## Complete Example

```python
from xboolarray import XBoolArray

# Initialize with some axis names
xboolarray = XBoolArray(["axis1", "axis2"])

# Add data with existing dimensions
xboolarray.add_data({"axis1": "coord1_1", "axis2": "coord2_1"})

# Add data with new coordinates
xboolarray.add_data({"axis1": "coord1_2", "axis2": ["coord2_2", "coord2_3"]})

# Add data with a new dimension
xboolarray.add_data({"axis1": "coord1_3", "axis2": "coord2_3", "axis3": "coord3_1"})

# Add more data
xboolarray.add_data({"axis1": "coord1_4", "axis2": ["coord2_1", "coord2_2"], "axis3": ["coord3_1", "coord3_2"]})

# Print the current state of the XBoolArray
print(xboolarray)

# Example of selecting a slice
print("\nSelecting axis1=['coord1_3', 'coord1_4'] and axis2='coord2_1':")
slice_result = xboolarray.select({"axis1": ["coord1_3", "coord1_4"], "axis2": "coord2_1"})
print(slice_result)

# Example of summing over one dimension
print("\nSum over 'axis2' dimension:")
sum_result = xboolarray.sum("axis2")
print(sum_result)

# Example of summing over multiple dimensions
print("\nSum over 'axis2' and 'axis1' dimensions:")
sum_result = xboolarray.sum(["axis2", "axis1"])
print(sum_result)

# Example of selecting and then summing
print("\nSelect axis1='coord1_4' then sum over 'axis3':")
sum_selected = xboolarray.sum_selected({"axis1": "coord1_4"}, "axis3")
print(sum_selected)
```

## Use Cases

XBoolArray is particularly useful for:

- Tracking combinations of features/properties in complex systems
- Building truth tables with named dimensions
- Managing boolean flags across multiple categories
- Data filtering and selection based on multiple criteria
- Sparse boolean representation of multidimensional data

## API Reference

### Constructor

- `XBoolArray(axis_names)`: Initialize with a list of axis names

### Methods

- `add_data(coord_dict)`: Add data to the array using coordinates
- `select(selection)`: Select a slice of the array based on coordinates
- `sum(dims=None)`: Sum boolean values over specified dimensions
- `sum_selected(selection, dims=None)`: Select a slice and sum over dimensions
- `get_array()`: Return the underlying xarray DataArray

### Properties

- `shape`: The shape of the underlying data array
- `dims`: The dimension names of the array
- `coords`: Dictionary of coordinates for each dimension