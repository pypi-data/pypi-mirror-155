import os
import logging
import shutil
import tempfile
from spython.main import Client as singularity_client


class Elastix:
    def __init__(self, version: str) -> None:
        self.version = version
        self._docker_url = "svdvoort/elastix:" + self.version
        self._singularity_url = "docker://" + self._docker_url

        self._singularity_folder = os.path.join(os.path.expanduser("~"), ".elastixpy")
        self._singularity_container_name = "elastix:" + self.version + ".sif"
        self._singularity_image = os.path.join(self._singularity_folder, self._singularity_container_name)

        self._pull_singularity_image()

        # Default options
        self._fixed_images = []
        self._moving_images = []
        self._output_directory = None
        self._parameter_files = []
        self._fixed_images_mask = []
        self._moving_images_mask = []
        self._initial_transform = None

    def _pull_singularity_image(self) -> None:
        if not os.path.exists(self._singularity_image):
            os.makedirs(self._singularity_folder, exist_ok=True)
            container_file, puller = singularity_client.pull(self._singularity_url,
                                                             stream=True,
                                                             pull_folder=self._singularity_folder)

            for line in puller:
                logging.info("Pulling Elastix container tag %s", self.version)
                logging.info(line)
            shutil.move(container_file, self._singularity_image)

    @property
    def fixed_images(self) -> list:
        return self._fixed_images

    @fixed_images.setter
    def fixed_images(self, fixed_images: list) -> None:
        self._fixed_images = fixed_images

    @property
    def moving_images(self) -> list:
        return self._moving_images

    @moving_images.setter
    def moving_images(self, moving_images: list) -> None:
        self._moving_images = moving_images

    @property
    def output_directory(self) -> str:
        return self._output_directory

    @output_directory.setter
    def output_directory(self, output_directory: str) -> None:
        self._output_directory = output_directory

    @property
    def parameter_files(self) -> list:
        return self._parameter_files

    @parameter_files.setter
    def parameter_files(self, parameter_files: list) -> None:
        self._parameter_files = parameter_files

    @property
    def fixed_images_mask(self) -> list:
        return self._fixed_images_mask

    @fixed_images_mask.setter
    def fixed_images_mask(self, fixed_images_mask: list) -> None:
        self._fixed_images_mask = fixed_images_mask

    @property
    def moving_images_mask(self) -> list:
        return self._moving_images_mask

    @moving_images_mask.setter
    def moving_images_mask(self, moving_images_mask: list) -> None:
        self._moving_images_mask = moving_images_mask

    @property
    def initial_transform(self) -> str:
        return self._initial_transform

    @initial_transform.setter
    def initial_transform(self, initial_transform: str) -> None:
        self._initial_transform = initial_transform

    def run(self):
        command = ["-out", "/out/"]

        if self.output_directory is None:
            self.output_directory = tempfile.mkdtemp()

        if self.initial_transform is not None:
            command.append("-t0")
            command.append(self.initial_transform)



        os.makedirs(self.output_directory, exist_ok=True)

        # TODO requires all fixed images, moving images, parameter files (respectively) to be in the same folder
        fixed_images_folder = os.path.dirname(os.path.normpath(self.fixed_images[0]))
        moving_images_folder = os.path.dirname(os.path.normpath(self.moving_images[0]))
        parameter_folder = os.path.dirname(os.path.normpath(self.parameter_files[0]))


        bindings = [parameter_folder + ":/parameters",
                    fixed_images_folder + ":/fixed",
                    moving_images_folder + ":/moving",
                    self.output_directory + ":/out"]

        for i_parameter_file in self.parameter_files:
            command.append("-p")
            command.append("/parameters/" + os.path.basename(i_parameter_file))

        for i_moving_image in self.moving_images:
            command.append("-m")
            command.append("/moving/" + os.path.basename(i_moving_image))

        for i_fixed_image in self.fixed_images:
            command.append("-f")
            command.append("/fixed/" + os.path.basename(i_fixed_image))

        for i_fixed_mask in self.fixed_images_mask:
            command.append("-fMask")
            command.append("/fixed/" + os.path.basename(i_fixed_mask))

        for i_moving_mask in self.moving_images_mask:
            command.append("-mMask")
            command.append("/moving/" + os.path.basename(i_moving_mask))

        container_output = singularity_client.run(
            self._singularity_image,
            command,
            bind=bindings,
            stream=True
        )

        for line in container_output:
            print(line)

        transformparameter_file = os.path.join(self.output_directory, "TransformParameters." + str(len(self.parameter_files) - 1) + ".txt")
        return transformparameter_file


class RegistrationParameters:
    def __init__(self, parameter_file: str):
        self._parameter_file = parameter_file
        self.parameters = {}

        self.read_registration_parameters()

    def read_registration_parameters(self):
        with open(self._parameter_file, "r") as the_file:
            lines = the_file.readlines()
            for line in lines:
                line.strip()
                if line[0] == "(":
                    # Remove beginning and end bracket:
                    line = line[1:-2]
                    # Split to separate key and value:
                    line = line.split(" ", maxsplit=1)

                    # If there are quotes around the value we will remove them.
                    if line[1][0] == '"' or line[1][0] == "'":
                        line[1] = line[1][1:-1]
                    self.parameters[line[0]] = line[1]

    def write_registration_parameters(self, out_parameter_file):
        with open(out_parameter_file, "w") as the_file:
            for key, value in self.parameters.items():
                if self._parameter_value_is_numeric(value):
                    the_file.write("(" + key + " "  + str(value) + ")\n")
                else:
                    the_file.write("(" + key + " \""  + value + "\")\n")

    @staticmethod
    def _split_parameter_value(parameter_value: str) -> list:
        return parameter_value.split(" ")

    @staticmethod
    def is_number(value: str) -> bool:
        try:
            float(value)
            return True
        except ValueError:
            return False


    def _parameter_value_is_numeric(self, parameter_value: str) -> bool:
        if " " in parameter_value:
            return all(self.is_number(i_entry) for i_entry in self._split_parameter_value(parameter_value))
        else:
            return self.is_number(parameter_value)



class Transformix:
    def __init__(self, version: str) -> None:
        self.version = version

        self._docker_url = "svdvoort/transformix:" + self.version
        self._singularity_url = "docker://" + self._docker_url

        self._singularity_folder = os.path.join(os.path.expanduser("~"), ".elastixpy")
        self._singularity_container_name = "transformix:" + self.version + ".sif"
        self._singularity_image = os.path.join(self._singularity_folder, self._singularity_container_name)

        self._pull_singularity_image()


        # Default options
        self._input_image = None
        self._transform_parameter_file = None
        self._output_directory = None

    def _pull_singularity_image(self) -> None:
        if not os.path.exists(self._singularity_image):
            os.makedirs(self._singularity_folder, exist_ok=True)
            container_file, puller = singularity_client.pull(self._singularity_url,
                                                             stream=True,
                                                             pull_folder=self._singularity_folder)
            for line in puller:
                logging.info("Pulling transformix container tag %s", self.version)
                logging.info(line)
            shutil.move(container_file, self._singularity_image)

    @property
    def input_image(self) -> str:
        return self._input_image

    @input_image.setter
    def input_image(self, input_image) -> None:
        self._input_image = input_image

    @property
    def transform_parameter_file(self) -> str:
        return self._transform_parameter_file

    @transform_parameter_file.setter
    def transform_parameter_file(self, transform_parameter_file) -> None:
        self._transform_parameter_file = transform_parameter_file

    @property
    def output_directory(self) -> str:
        return self._output_directory

    @output_directory.setter
    def output_directory(self, output_directory) -> None:
        self._output_directory = output_directory

    def run(self, output_file_name: str = None) -> str:

        os.makedirs(self.output_directory, exist_ok=True)

        # TODO requires all fixed images, moving images, parameter files (respectively) to be in the same folder
        input_image_folder = os.path.dirname(os.path.normpath(self.input_image))
        parameter_folder = os.path.dirname(os.path.normpath(self.transform_parameter_file))


        bindings = [parameter_folder + ":/parameters",
                    input_image_folder + ":/input",
                    self.output_directory + ":/out"]

        command = ["-in", "/input/" + os.path.basename(os.path.normpath(self.input_image)),
                   "-tp", "/parameters/" + os.path.basename(os.path.normpath(self.transform_parameter_file)),
                   "-out", "/out/"]

        container_output = singularity_client.run(
            self._singularity_image,
            command,
            bind=bindings,
            stream=True
        )

        for line in container_output:
            print(line)

        if output_file_name is not None:
            shutil.move(os.path.join(self.output_directory, "result.nii.gz"), os.path.join(self.output_directory, output_file_name))
        else:
            output_file_name = "result.nii.gz"

        return os.path.join(self.output_directory, output_file_name)

