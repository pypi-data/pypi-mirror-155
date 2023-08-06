from .BaseSource import BaseSource


class MCPL_source(BaseSource):
    """
    MCPL source for guide_bot

    Use MCPL file, but provide approximate width / height. These are not
    used in the component, but used for e.g. plotting.
    """

    def __init__(self, mcpl_file, repeat_count=1, E_smear=0, pos_smear=0, dir_smear=0, *args, **kwargs):
        """
        Simple example of a guide_bot source inheriting from BaseSource

        Simple rectangular source description with constant intensity as a
        function of wavelength. Uses the McStas component Source_simple.

        Parameters
        ----------

        width : float / list for scan
            Width of the rectangular source in [m]

        height : float / list for scan
            Height of the rectangular source in [m]

        guide_start : float / list for scan
            Given distance from source to start of guide (guides can overwrite)

        min_guide_start : float / list for scan
            Minimum distance from source to guide (guides can overwrite)

        max_guide_start : float / list for scan
            Maximum distance from source to guide (guides can overwrite)

        mcpl_file : str
            Path for mcpl file
        """

        super().__init__(*args, **kwargs)

        self.parameters.add("mcpl_file", mcpl_file, is_filename=True)
        self.parameters.add("E_smear", E_smear)
        self.parameters.add("pos_smear", pos_smear, unit="m")
        self.parameters.add("dir_smear", dir_smear, unit="deg")
        self.parameters.add("repeat_count", repeat_count)

    def add_to_instrument(self, instrument, instrument_parameters, first_element):
        """
        Add to instrument adds McStas code describing the source

        Here adding the Source_simple component after origin with the
        parameters contained in the object and given in the method input.

        Parameters
        ----------

        instrument : McStasScript instr object
            Instrument object which the source should be added to

        instrument_parameters : InstrumentParameterContainer object
            Parameter container where parameters can be added for optimization

        first_element : GuideElement
            The first user provided GuideElement after the source
        """

        src = instrument.add_component("MCPL_source", "MCPL_input", after="Origin")

        src.filename = self["mcpl_file"]
        src.dir_smear = self["dir_smear"]
        src.pos_smear = self["pos_smear"]
        src.E_smear = self["E_smear"]
        src.repeat_count = self["repeat_count"]

        # Wavelength to energy:
        # min / max_wavelength parameters always defined by sample
        # wavelength -> k: 2*pi/wavelength
        src.Emin = "2.0*PI/max_wavelength*2.0*PI/max_wavelength*K2V*K2V*VS2E"
        src.Emax = "2.0*PI/min_wavelength*2.0*PI/min_wavelength*K2V*K2V*VS2E"

