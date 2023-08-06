import pyclesperanto_prototype as cle

class ClearControlDataset:

    def __init__(self, directory_name : str, dataset_name : str = 'C0opticsprefused'):
        self.directory_name = directory_name
        self.dataset_name = dataset_name

        import json
        fp = open(directory_name + "/" + dataset_name + '.metadata.txt')
        lines = fp.readlines()
        self.metadata = [json.loads(line) for line in lines]
        fp.close()

        fp = open(directory_name + "/" + dataset_name + '.index.txt')
        lines = fp.readlines()
        self.times_in_seconds = []
        self.widths = []
        self.heights = []
        self.depths = []
        for line in lines:
            elements = line.split("\t")

            self.times_in_seconds.append(float(elements[1]))

            third_element = elements[2].split(", ")
            self.widths.append(int(third_element[0]))
            self.heights.append(int(third_element[1]))
            self.depths.append(int(third_element[2]))

    def _handle_index_and_time(self, index, time_in_seconds):
        if index is None and time_in_seconds is None:
            index = 0
        if index is None:
            index = self.get_index_after_time(time_in_seconds)
        return index, time_in_seconds

    def get_image(self, index = None, time_in_seconds = None):
        index, time_in_seconds = self._handle_index_and_time(index, time_in_seconds)

        filename = self.get_image_filename(index)
        from ._imread_raw import imread_raw
        return imread_raw(filename, self.widths[index], self.heights[index], self.depths[index])

    def get_image_filename(self, index = None, time_in_seconds = None):
        index, time_in_seconds = self._handle_index_and_time(index, time_in_seconds)
        from ..utils import index_to_clearcontrol_filename
        return self.directory_name + "/stacks/" + self.dataset_name + "/" + index_to_clearcontrol_filename(index)

    def get_voxel_size_zyx(self, index = None, time_in_seconds = None):
        index, time_in_seconds = self._handle_index_and_time(index, time_in_seconds)
        metadata = self.metadata[index]

        return [
            metadata['VoxelDimZ'],
            metadata['VoxelDimY'],
            metadata['VoxelDimX'],
        ]

    def get_index_after_time(self, after_time_in_seconds : float):
        for i, time in enumerate(self.times_in_seconds):
            if (time >= after_time_in_seconds):
                return i

    def get_duration_in_seconds(self):
        return self.times_in_seconds[-1]

    def get_resampled_image(self, index = None, time_in_seconds = None, resampled_image : cle.Image = None, linear_interpolation : bool = True):
        index, time_in_seconds = self._handle_index_and_time(index, time_in_seconds)

        input_image = cle.push(self.get_image(index))
        voxel_size = self.get_voxel_size_zyx(index)

        resampled_image = cle.scale(input_image, resampled_image, factor_x=voxel_size[2], factor_y=voxel_size[1],
                                       factor_z=voxel_size[0], linear_interpolation=linear_interpolation)

        return resampled_image


