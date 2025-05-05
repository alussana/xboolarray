#!/usr/bin/env python3

import numpy as np
import xarray as xr
from typing import List, Dict, Any, Union


class XBoolArray:
    """
    A multidimensional boolean array with annotated dimensions and coordinates.
    This class allows for dimensions to be increased dynamically by adding new data.
    """

    def __init__(self, axis_names: List[str]):
        """
        Initialize a XBoolArray with given axis names.

        Parameters:
        -----------
        axis_names : List[str]
            Names of the axes for the multidimensional array.
        """
        self.axis_names = axis_names

        # Create an empty xarray DataArray with the specified dimensions
        coords = {axis: [] for axis in axis_names}
        self.data = xr.DataArray(
            data=np.zeros((0,) * len(axis_names), dtype=bool),
            dims=axis_names,
            coords=coords,
        )

    def add_data(self, coord_dict: Dict[str, Union[str, List[str]]]):
        """
        Add data to the tensor by specifying coordinates for each dimension.

        Parameters:
        -----------
        coord_dict : Dict[str, Union[str, List[str]]]
            Dictionary where keys are dimension names and values are coordinate names.
            Values can be a single coordinate name (str) or a list of coordinate names.
        """
        # First, convert any string values to lists for consistent processing
        for key, value in coord_dict.items():
            if isinstance(value, str):
                coord_dict[key] = [value]

        # Process new dimensions (if any)
        new_dims = [dim for dim in coord_dict.keys() if dim not in self.axis_names]
        if new_dims:
            self.axis_names.extend(new_dims)
            for dim in new_dims:
                # Expand the array to include the new dimension
                self.data = self.data.expand_dims({dim: []})

        # Process new coordinates for each dimension
        for dim, coords in coord_dict.items():
            existing_coords = (
                list(self.data.coords[dim].values) if dim in self.data.coords else []
            )
            new_coords = [c for c in coords if c not in existing_coords]

            if new_coords:
                # Create a larger array that includes the new coordinates
                all_coords = existing_coords + new_coords
                new_shape = list(self.data.shape)
                dim_idx = self.data.dims.index(dim)
                new_shape[dim_idx] = len(all_coords)

                # Create new data array with expanded shape
                new_data = np.zeros(new_shape, dtype=bool)

                # Copy existing data to new array
                if existing_coords:
                    # Create slices for indexing the new array
                    slices = [slice(None)] * len(new_shape)
                    slices[dim_idx] = slice(0, len(existing_coords))
                    new_data[tuple(slices)] = self.data.values

                # Update the DataArray
                new_coords_dict = {
                    d: list(self.data.coords[d].values) for d in self.data.dims
                }
                new_coords_dict[dim] = all_coords

                self.data = xr.DataArray(
                    data=new_data, dims=self.data.dims, coords=new_coords_dict
                )

        # Now set the specified points to True
        # We need to create a mesh of all combinations of the coordinates
        mesh_coords = {}
        for dim, coords in coord_dict.items():
            mesh_coords[dim] = coords

        # Create all combinations of coordinates
        from itertools import product

        for coord_combination in product(*mesh_coords.values()):
            # Create a dictionary mapping each dimension to a specific coordinate
            sel_dict = {
                dim: coord for dim, coord in zip(mesh_coords.keys(), coord_combination)
            }
            # Set the value to True
            self.data.loc[sel_dict] = True

    def __str__(self) -> str:
        """Return a string representation of the XBoolArray."""
        return f"XBoolArray with dimensions: {self.axis_names}\n{str(self.data)}"

    def __repr__(self) -> str:
        """Return a formal string representation of the XBoolArray."""
        return self.__str__()

    @property
    def shape(self) -> tuple:
        """Return the shape of the underlying data array."""
        return self.data.shape

    @property
    def dims(self) -> List[str]:
        """Return the dimension names of the array."""
        return list(self.data.dims)

    @property
    def coords(self) -> Dict[str, List]:
        """Return a dictionary of coordinates for each dimension."""
        return {dim: list(self.data.coords[dim].values) for dim in self.data.dims}

    def get_array(self) -> xr.DataArray:
        """Return the underlying xarray DataArray."""
        return self.data

    def select(self, selection: Dict[str, Union[str, List[str]]]) -> xr.DataArray:
        """
        Select a slice of the array based on coordinate values.

        Parameters:
        -----------
        selection : Dict[str, Union[str, List[str]]]
            Dictionary where keys are dimension names and values are coordinate names to select.
            Values can be a single coordinate name or a list of coordinate names.

        Returns:
        --------
        xr.DataArray
            A slice of the original array matching the selection criteria.
        """
        # Process selection dictionary
        sel_dict = {}
        for dim, coords in selection.items():
            if dim not in self.axis_names:
                raise ValueError(f"Dimension '{dim}' not found in the array")

            if isinstance(coords, str):
                sel_dict[dim] = [coords]
            else:
                sel_dict[dim] = coords

        # Create the selection
        return self.data.sel(sel_dict)

    def sum(self, dims: Union[str, List[str]] = None) -> Union[xr.DataArray, float]:
        """
        Sum boolean values over specified dimensions.

        Parameters:
        -----------
        dims : Union[str, List[str]], optional
            Dimension(s) to sum over. If None, sum over all dimensions.

        Returns:
        --------
        Union[xr.DataArray, float]
            Sum of boolean values. Returns a reduced DataArray if some dimensions remain,
            or a float if summing over all dimensions.
        """
        if dims is None:
            dims = self.axis_names

        # Convert boolean values to integers for summation
        int_data = self.data.astype(int)

        # Sum over the specified dimensions
        return int_data.sum(dim=dims)

    def sum_selected(
        self,
        selection: Dict[str, Union[str, List[str]]],
        dims: Union[str, List[str]] = None,
    ) -> Union[xr.DataArray, float]:
        """
        Select a slice of the array and then sum over specified dimensions.

        Parameters:
        -----------
        selection : Dict[str, Union[str, List[str]]]
            Dictionary where keys are dimension names and values are coordinate names to select.
        dims : Union[str, List[str]], optional
            Dimension(s) to sum over. If None, sum over all dimensions not in selection.

        Returns:
        --------
        Union[xr.DataArray, float]
            Sum of boolean values in the selected slice.
        """
        # Select the slice
        selected = self.select(selection)

        # If dims is None, sum over all dimensions not in the selection
        if dims is None:
            dims = [dim for dim in self.axis_names if dim not in selection]

        # Convert boolean values to integers and sum
        return selected.astype(int).sum(dim=dims)


# Example usage:
if __name__ == "__main__":

    # Initialize with some axis names
    xboolarray = XBoolArray(["axis1", "axis2"])

    # Add data with existing dimensions
    xboolarray.add_data(
        {
            "axis1": "coord1_1",
            "axis2": "coord2_1"
        }
    )

    # Add data with new coordinates
    xboolarray.add_data(
        {
            "axis1": "coord1_2",
            "axis2": ["coord2_2", "coord2_3"]
        }
    )

    # Add data with a new dimension
    xboolarray.add_data(
        {
            "axis1": "coord1_3",
            "axis2": "coord2_3",
            "axis3": "coord3_1"
        }
    )

    # Add more data
    xboolarray.add_data(
        {
            "axis1": "coord1_4",
            "axis2": ["coord2_1", "coord2_2"],
            "axis3": ["coord3_1", "coord3_2"],
        }
    )

    # Print the current state of the XBoolArray
    print(xboolarray)

    # Example of selecting a slice
    print("\nSelecting axis1=['coord1_3', 'coord1_4'] and axis2='coord2_1':")
    slice_result = xboolarray.select(
        {"axis1": ["coord1_3", "coord1_4"], "axis2": "coord2_1"}
    )
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
